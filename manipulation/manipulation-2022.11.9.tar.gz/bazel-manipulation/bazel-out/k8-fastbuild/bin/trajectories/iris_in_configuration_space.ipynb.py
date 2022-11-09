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

# # Finding large collision-free configuration-space regions with IRIS
# 
# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/trajectories.html).  I recommend having both windows open, side-by-side!
# 

# In[ ]:


import time

import numpy as np
from pydrake.all import (AddMultibodyPlantSceneGraph, BsplineTrajectory,
                         DiagramBuilder, InverseKinematics,
                         IrisInConfigurationSpace, IrisOptions,
                         MathematicalProgram, MeshcatVisualizer,
                         MeshcatVisualizerParams, MinimumDistanceConstraint,
                         Parser, PositionConstraint, Rgba, RigidTransform,
                         Role, Solve, StartMeshcat)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import (PublishPositionTrajectory,
                                        model_inspector)
from manipulation.scenarios import AddIiwa, AddPlanarIiwa, AddShape, AddWsg
from manipulation.utils import AddPackagePaths, FindResource


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# ## Reaching into the shelves
# 
# Note that I'm using the original collision geometry (not replacing the hand geometry with the spheres, like we did to help kinematic trajectory optimization).

# In[ ]:


def AnimateIris(root_context, plant, visualizer, region, speed):
    """
    A simple hit-and-run-style idea for visualizing the IRIS regions:
    1. Start at the center. Pick a random direction and run to the boundary.
    2. Pick a new random direction; project it onto the current boundary, and run along it. Repeat
    """

    plant_context = plant.GetMyContextFromRoot(root_context)
    visualizer_context = visualizer.GetMyContextFromRoot(root_context)

    q = region.ChebyshevCenter()
    plant.SetPositions(plant_context, q)
    visualizer.Publish(visualizer_context)
    active_face = None

    print("Press the 'Stop Animation' button in Meshcat to continue.")
    meshcat.AddButton("Stop Animation", "Escape")

    rng = np.random.default_rng()
    nq = plant.num_positions()
    prog = MathematicalProgram()
    qvar = prog.NewContinuousVariables(nq, "q")
    prog.AddLinearConstraint(region.A(), 0 * region.b() - np.inf, region.b(),
                             qvar)
    cost = prog.AddLinearCost(np.ones((nq, 1)), qvar)

    while meshcat.GetButtonClicks("Stop Animation")<1:
        direction = rng.standard_normal(nq)
        cost.evaluator().UpdateCoefficients(direction)

        result = Solve(prog)
        assert result.is_success()

        q_next = result.GetSolution(qvar)

        # Animate between q and q_next (at speed):
        # TODO: normalize step size to speed... e.g. something like
        # 20 * np.linalg.norm(q_next - q) / speed)
        for t in np.append(np.arange(0, 1, .05), 1):
            qs = t * q_next + (1 - t) * q
            plant.SetPositions(plant_context, qs)
            visualizer.Publish(visualizer_context)
            if running_as_notebook:
                time.sleep(.05)

        q = q_next

        if not running_as_notebook:
            break

    meshcat.DeleteButton("Stop Animation")

def animate_iris_region():
    meshcat.Delete()
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddIiwa(plant)
    wsg = AddWsg(plant, iiwa, welded=True, sphere=False)
    p_TopShelf = [0.95, 0, 0.65]

    parser = Parser(plant)
    bin = parser.AddModelFromFile(
        FindResource("models/shelves.sdf"))
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("shelves_body", bin),
                     RigidTransform([0.88, 0, 0.4]))

    plant.Finalize()

    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat,
        MeshcatVisualizerParams(role=Role.kIllustration))
    collision_visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat,
        MeshcatVisualizerParams(prefix="collision", role=Role.kProximity))
    meshcat.SetProperty("collision", "visible", False)

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    num_q = plant.num_positions()
    q0 = plant.GetPositions(plant_context)
    gripper_frame = plant.GetFrameByName("body", wsg)

    # First seed should just be the home position.
    options = IrisOptions()
    options.num_collision_infeasible_samples = 2 if running_as_notebook else 1
    options.require_sample_point_is_contained = True
    region = IrisInConfigurationSpace(plant, plant_context, options)

    # Add a seed for reaching into the top shelf.
    ik = InverseKinematics(plant, plant_context)
    collision_constraint = ik.AddMinimumDistanceConstraint(0.001, 0.01)
    grasp_constraint = ik.AddPositionConstraint(gripper_frame, [0, 0.1, 0],
                                                plant.world_frame(), p_TopShelf,
                                                p_TopShelf)

    q = ik.q()
    prog = ik.get_mutable_prog()
    prog.SetInitialGuess(q, q0)
    result = Solve(ik.prog())
    if not result.is_success():
        print("IK failed")
    plant.SetPositions(plant_context, result.GetSolution(q))
    diagram.Publish(context)
    print(region.PointInSet(result.GetSolution(q)))

    options.configuration_obstacles = [region]
    shelf_region = IrisInConfigurationSpace(plant, plant_context, options)
    print(shelf_region.PointInSet(result.GetSolution(q)))
    AnimateIris(context, plant, visualizer, shelf_region, speed=.1)

animate_iris_region()


# In[ ]:




