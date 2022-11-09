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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/pick.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import numpy as np
from IPython.display import clear_output, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph,
                         DiagramBuilder, JacobianWrtVariable, JointSliders,
                         LeafSystem, MeshcatVisualizer, Parser, RigidTransform,
                         RollPitchYaw, StartMeshcat)

from manipulation import FindResource, running_as_notebook
from manipulation.scenarios import AddPackagePaths


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Kinematic Jacobians for pick and place
# 
# Let's set up the same iiwa + wsg example, with sliders (but without the frames), that we used above.  But this time I'll display the value of the Jacobian $J^G(q)$.

# In[ ]:


class PrintJacobian(LeafSystem):
    def __init__(self, plant, frame):
        LeafSystem.__init__(self)
        self._plant = plant
        self._plant_context = plant.CreateDefaultContext()
        self._frame = frame
        self.DeclareVectorInputPort("state", plant.num_multibody_states())
        self.DeclareForcedPublishEvent(self.Publish)

    def Publish(self, context):
        state = self.get_input_port().Eval(context)
        self._plant.SetPositionsAndVelocities(self._plant_context, state)
        W = self._plant.world_frame()
        J_G = self._plant.CalcJacobianSpatialVelocity(
            self._plant_context, JacobianWrtVariable.kQDot, self._frame,
            [0, 0, 0], W, W)  ## This is the important line

        print("J_G:")
        print(np.array2string(J_G, formatter={
              'float': lambda x: "{:5.1f}".format(x)}))
        print(
            f"smallest singular value(J_G): {np.min(np.linalg.svd(J_G, compute_uv=False))}")
        clear_output(wait=True)

def pick_and_place_jacobians_example():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0)
    parser = Parser(plant)
    AddPackagePaths(parser)
    parser.AddAllModelsFromFile(FindResource("models/iiwa_and_wsg.dmd.yaml"))
    plant.Finalize()

    meshcat.Delete()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph.get_query_output_port(), meshcat)

    G = plant.GetBodyByName("body").body_frame()
    print_jacobian = builder.AddSystem(PrintJacobian(plant, G))
    builder.Connect(plant.get_state_output_port(),
                    print_jacobian.get_input_port())

    # If you want to set the initial positions manually, use this:
    #plant.SetPositions(plant.GetMyContextFromRoot(context),
    #                   plant.GetModelInstanceByName("iiwa"),
    #                   [0, 0, 0, 0, 0, 0, 0])

    default_interactive_timeout = None if running_as_notebook else 1.0
    sliders = builder.AddSystem(JointSliders(meshcat, plant))
    diagram = builder.Build()
    sliders.Run(diagram, default_interactive_timeout)
    meshcat.DeleteAddedControls()

meshcat.DeleteAddedControls()
pick_and_place_jacobians_example()


# In[ ]:




