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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/trajectories.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import numpy as np
from pydrake.all import (AddMultibodyPlantSceneGraph, DiagramBuilder,
                         InverseKinematics, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, RigidTransform,
                         Solve, Sphere, StartMeshcat)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import plot_mathematical_program
from manipulation.scenarios import AddShape, AddTwoLinkIiwa, AddWsg
from manipulation.utils import FindResource


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Visualizing the costs and constraints
# 
# Here is another view.  Notice that at the optimal solution of the iiwa reaching into the shelf, the last joint was almost zero.  I've gone ahead and welded it to zero, so that we are now down to just a two degree of freedom IK problem.  Now we can plot the entire cost and constraint landscape.  Let's do it.
# 
# There is a lot going on in the second meshcat window.  Use the controls to turn on and off different costs/constraints.  The constraints are blue where they are feasible and red where they are infeasible.  Which constraint is the horribly ugly one?

# In[ ]:


def draw_ik_prog(zoom=True):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddTwoLinkIiwa(plant)
    wsg = AddWsg(plant, iiwa, roll=0.0, welded=True)
    sphere = AddShape(plant, Sphere(0.02), "sphere")
    X_WO = RigidTransform([0.6, 0, 0.65])
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("sphere"), X_WO)

    parser = Parser(plant)
    bin = parser.AddModelFromFile(FindResource("models/shelves.sdf"))
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("shelves_body", bin), RigidTransform([0.6,0,0.4]))

    plant.Finalize()

#    visualizer = MeshcatVisualizer.AddToBuilder(
#        builder, 
#        scene_graph, 
#        meshcat,
#        MeshcatVisualizerParams(delete_prefix_initialization_event=False))

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    q0 = plant.GetPositions(plant_context)
    gripper_frame = plant.GetFrameByName("body", wsg)
    sphere_frame = plant.GetFrameByName("sphere", sphere)

    ik = InverseKinematics(plant, plant_context)
    collision_constraint = ik.AddMinimumDistanceConstraint(0.001, 0.1)
    grasp_constraint = ik.AddPositionConstraint(
        gripper_frame, [0, 0.1, 0], sphere_frame, 
        [-0.001, -0.001, -0.001], [0.001, 0.001, 0.001])
    
    prog = ik.get_mutable_prog()
    q = ik.q()
    prog.AddQuadraticErrorCost(np.identity(len(q)), q0, q)
    prog.SetInitialGuess(q, q0)
    result = Solve(ik.prog())
    if not result.is_success():
        print("IK failed")

    diagram.Publish(context)

    meshcat.Delete()
    meshcat.SetProperty("/Background", "visible", False)
    if zoom:
        qstar = result.GetSolution(q)
        X, Y = np.meshgrid(np.linspace(qstar[0]-0.2, qstar[0]+0.2, 75), np.linspace(qstar[1]-0.2, qstar[1]+0.2, 75))
        point_size=0.01
    else:        
        low = plant.GetPositionLowerLimits()
        up = plant.GetPositionUpperLimits()
        X, Y = np.meshgrid(np.linspace(low[0], up[0], 175),
                           np.linspace(low[1], up[1], 175))
        point_size=0.05
    plot_mathematical_program(meshcat, "ik", prog, X, Y, result,
                              point_size=point_size)
    
draw_ik_prog(zoom=True)

