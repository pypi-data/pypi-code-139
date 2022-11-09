from pydrake.common.deprecation import DrakeDeprecationWarning
import warnings
warnings.simplefilter("error", DrakeDeprecationWarning)

try:
    from manipulation.utils import set_running_as_test
    set_running_as_test(True)

except ModuleNotFoundError:
    pass
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time

import numpy as np
from IPython.display import clear_output
from pydrake.all import (AddMultibodyPlantSceneGraph, DiagramBuilder,
                         JacobianWrtVariable, MathematicalProgram,
                         MeshcatVisualizer, PiecewisePolynomial, Solve,
                         StartMeshcat)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import plot_mathematical_program
from manipulation.scenarios import AddTwoLinkIiwa


# This one is specific to this notebook, but I'm putting it in the header to make it less distracting.
def Visualizer(MakeMathematicalProgram):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0)
    twolink = AddTwoLinkIiwa(plant, q0=[0.0, 0.0])
    hand = plant.GetFrameByName("iiwa_link_ee")
    plant.Finalize()

    MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)
    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    meshcat.Delete()
    meshcat.SetProperty("/Background", 'top_color', [0, 0, 0])
    meshcat.SetProperty("/Background", 'bottom_color', [0, 0, 0])
    meshcat.SetProperty("/Grid", 'visible', False)

    X, Y = np.meshgrid(np.linspace(-5, 5, 35), np.linspace(-5, 5, 31))

    def visualize(q, v_Gdesired=[1.0, 0.0], t=None):
        if t:
            context.SetTime(t)
        plant.SetPositions(plant_context, q)
        diagram.Publish(context)

        J_G = plant.CalcJacobianTranslationalVelocity(plant_context,
                                                      JacobianWrtVariable.kQDot,
                                                      hand, [0, 0, 0],
                                                      plant.world_frame(),
                                                      plant.world_frame())
        J_G = J_G[[0,2],:]  # Ignore Y.
        print("J_G = ")
        print(
            np.array2string(J_G,
                            formatter={'float': lambda x: "{:5.2f}".format(x)}))

        prog = MakeMathematicalProgram(q, J_G, v_Gdesired)
        result = Solve(prog)
        plot_mathematical_program(meshcat, "QP", prog, X, Y, result=result)
        # TODO: Add set_object to meshcat.Animation
        if False: # meshcat._is_recording:
            with meshcat._animation.at_frame(
                    v, meshcat._recording_frame_num) as m:
                plot_mathematical_program(m, prog, X, Y, result=result)
        clear_output(wait=True)

    return visualize


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Differential Inverse Kinematics as a Quadratic Program
# 
# ## Define your mathematical program here.
# 

# In[ ]:


def MakeMathematicalProgram(q, J_G, v_Gdesired):
    prog = MathematicalProgram()
    v = prog.NewContinuousVariables(2, 'v')
    v_max = 3.0 

    error = J_G @ v - np.asarray(v_Gdesired)
    prog.AddCost(error.dot(error))
    prog.AddBoundingBoxConstraint(-v_max, v_max, v)

    return prog


# ## Visualize a particular joint angle

# In[ ]:


visualize = Visualizer(MakeMathematicalProgram)

q = [-np.pi/2.0+0.5, 1.0]
v_Gdesired = [0.5, 0.]
visualize(q, v_Gdesired)


# ## Animated joint trajectory (passing through the singularity)

# In[ ]:


visualize = Visualizer(MakeMathematicalProgram)

v_Gdesired = [1.0, 0.0]
T = 2.
q = PiecewisePolynomial.FirstOrderHold(
    [0, T, 2 * T],
    np.array([[-np.pi / 2.0 + 1., -np.pi / 2.0 - 1., -np.pi / 2.0 + 1.],
              [2., -2., 2]]))

nx = 35
ny = 31
X, Y = np.meshgrid(np.linspace(-5, 5, nx), np.linspace(-5, 5, ny))
D = np.vstack((X.reshape(1,-1), Y.reshape(1,-1)))
for i in range(2):
    for t in np.linspace(0, 2*T, num=100):
        visualize(q.value(t), v_Gdesired, t=t)
        if not running_as_notebook: break
        time.sleep(0.05)


# ## Trajectory slider
# 
# TODO(russt): I can remove this once I'm able to save the plotted surfaces in the meshcat animation.

# In[ ]:


visualize = Visualizer(MakeMathematicalProgram)

v_Gdesired = [1.0, 0.0]
T = 2.
qtraj = PiecewisePolynomial.FirstOrderHold(
    [0, T], np.array([[-np.pi / 2.0 + 1., -np.pi / 2.0 - 1.], [2., -2.]]))
visualize(qtraj.value(0), v_Gdesired)

meshcat.AddSlider("time", min=0, max=T, step=0.05, value=0)
meshcat.AddButton("Stop Interaction Loop")
while meshcat.GetButtonClicks("Stop Interaction Loop") < 1:
    t = meshcat.GetSliderValue("time")
    visualize(qtraj.value(t), v_Gdesired)
    if not running_as_notebook: break
    time.sleep(0.05)
meshcat.DeleteAddedControls()


# ## Joint Sliders

# In[ ]:


visualize = Visualizer(MakeMathematicalProgram)

q = [-np.pi/2.0 + 0.5, 1.0]
v_Gdesired = [1.0, 0.0]
visualize(q, v_Gdesired)

def _q_callback(change, index):
    q[index] = change.new
    visualize(q, v_Gdesired)
def _vG_callback(change, index):
    v_Gdesired[index] = change.new
    visualize(q, v_Gdesired)

meshcat.AddSlider("q0", value=q[0], min=-np.pi, max=np.pi, step=0.1)
meshcat.AddSlider("q1", value=q[1], min=-np.pi, max=np.pi, step=0.1)
meshcat.AddSlider("v_G_W0", value=v_Gdesired[0], min=-4, max=4, step=0.1)
meshcat.AddSlider("v_G_W1", value=v_Gdesired[1], min=-4, max=4, step=0.1)

meshcat.AddButton("Stop Interaction Loop")
while meshcat.GetButtonClicks("Stop Interaction Loop") < 1:
    q = [meshcat.GetSliderValue("q0"), meshcat.GetSliderValue("q1")]
    v_Gdesired = [meshcat.GetSliderValue("v_G_W0"),
                  meshcat.GetSliderValue("v_G_W1")]
    visualize(q, v_Gdesired)
    if not running_as_notebook: break
    time.sleep(0.05)
meshcat.DeleteAddedControls()


# In[ ]:




