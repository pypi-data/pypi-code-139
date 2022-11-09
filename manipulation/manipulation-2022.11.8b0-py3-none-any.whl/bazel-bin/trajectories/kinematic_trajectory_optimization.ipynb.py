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

# # Kinematic Trajectory Optimization
# 
# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/trajectories.html).  I recommend having both windows open, side-by-side!
# 

# In[ ]:


import time

import numpy as np
from pydrake.all import (AddMultibodyPlantSceneGraph, BsplineTrajectory,
                         DiagramBuilder, KinematicTrajectoryOptimization,
                         MeshcatVisualizer, MeshcatVisualizerParams,
                         MinimumDistanceConstraint, Parser, PositionConstraint,
                         Rgba, RigidTransform, Role, Solve, Sphere,
                         StartMeshcat)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import (PublishPositionTrajectory,
                                        model_inspector)
from manipulation.scenarios import AddIiwa, AddPlanarIiwa, AddShape, AddWsg
from manipulation.utils import AddPackagePaths, FindResource


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# ## Reaching into the shelves

# In[ ]:


def trajopt_shelves_demo():
    meshcat.Delete()
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddPlanarIiwa(plant)
    wsg = AddWsg(plant, iiwa, roll=0.0, welded=True, sphere=True)
    X_WStart = RigidTransform([0.8, 0, 0.65])
    meshcat.SetObject("start", Sphere(0.02), rgba=Rgba(.9, .1, .1, 1))
    meshcat.SetTransform("start", X_WStart)
    X_WGoal = RigidTransform([0.8, 0, 0.4])
    meshcat.SetObject("goal", Sphere(0.02), rgba=Rgba(.1, .9, .1, 1))
    meshcat.SetTransform("goal", X_WGoal)

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

    trajopt = KinematicTrajectoryOptimization(plant.num_positions(), 10)
    prog = trajopt.get_mutable_prog()
    trajopt.AddDurationCost(1.0)
    trajopt.AddPathLengthCost(1.0)
    trajopt.AddPositionBounds(plant.GetPositionLowerLimits(),
                              plant.GetPositionUpperLimits())
    trajopt.AddVelocityBounds(plant.GetVelocityLowerLimits(),
                              plant.GetVelocityUpperLimits())

    trajopt.AddDurationConstraint(.5, 5)

    # start constraint
    start_constraint = PositionConstraint(plant, plant.world_frame(),
                                          X_WStart.translation(),
                                          X_WStart.translation(), gripper_frame,
                                          [0, 0.1, 0], plant_context)
    trajopt.AddPathPositionConstraint(start_constraint, 0)
    prog.AddQuadraticErrorCost(np.eye(num_q), q0,
                               trajopt.control_points()[:, 0])

    # goal constraint
    goal_constraint = PositionConstraint(plant, plant.world_frame(),
                                         X_WGoal.translation(),
                                         X_WGoal.translation(), gripper_frame,
                                         [0, 0.1, 0], plant_context)
    trajopt.AddPathPositionConstraint(goal_constraint, 1)
    prog.AddQuadraticErrorCost(np.eye(num_q), q0,
                               trajopt.control_points()[:, -1])

    # start and end with zero velocity
    trajopt.AddPathVelocityConstraint(np.zeros((num_q, 1)), np.zeros(
        (num_q, 1)), 0)
    trajopt.AddPathVelocityConstraint(np.zeros((num_q, 1)), np.zeros(
        (num_q, 1)), 1)

    # Solve once without the collisions and set that as the initial guess for
    # the version with collisions.
    result = Solve(prog)
    if not result.is_success():
        print("Trajectory optimization failed, even without collisions!")
        print(result.get_solver_id().name())
    trajopt.SetInitialGuess(trajopt.ReconstructTrajectory(result))

    # collision constraints
    collision_constraint = MinimumDistanceConstraint(plant, 0.001,
                                                     plant_context, None, 0.01)
    evaluate_at_s = np.linspace(0, 1, 25)
    for s in evaluate_at_s:
        trajopt.AddPathPositionConstraint(collision_constraint, s)

    def PlotPath(control_points):
        traj = BsplineTrajectory(trajopt.basis(),
                                 control_points.reshape((3, -1)))
        meshcat.SetLine('positions_path',
                         traj.vector_values(np.linspace(0, 1, 50)))

    prog.AddVisualizationCallback(PlotPath,
                                  trajopt.control_points().reshape((-1,)))
    result = Solve(prog)
    if not result.is_success():
        print("Trajectory optimization failed")
        print(result.get_solver_id().name())

    PublishPositionTrajectory(trajopt.ReconstructTrajectory(result), context,
                              plant, visualizer)
    collision_visualizer.Publish(
        collision_visualizer.GetMyContextFromRoot(context))


trajopt_shelves_demo()


# ## Moving between bins (without hitting the cameras!)

# In[ ]:


def trajopt_bins_demo():
    meshcat.Delete()
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)

    parser = Parser(plant)
    AddPackagePaths(parser)
    bin = parser.AddAllModelsFromFile(
        FindResource("models/two_bins_w_cameras.dmd.yaml"))
    iiwa = AddIiwa(plant, collision_model="with_box_collision")
    wsg = AddWsg(plant, iiwa, welded=True, sphere=True)
    X_WStart = RigidTransform([0.5, 0, 0.15])
    meshcat.SetObject("start", Sphere(0.02), rgba=Rgba(.9, .1, .1, 1))
    meshcat.SetTransform("start", X_WStart)
    X_WGoal = RigidTransform([0, -0.6, 0.15])
    meshcat.SetObject("goal", Sphere(0.02), rgba=Rgba(.1, .9, .1, 1))
    meshcat.SetTransform("goal", X_WGoal)

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

    trajopt = KinematicTrajectoryOptimization(plant.num_positions(), 10)
    prog = trajopt.get_mutable_prog()

    q_guess = np.tile(q0.reshape((7,1)), (1, trajopt.num_control_points()))
    q_guess[0,:] = np.linspace(0, -np.pi/2, trajopt.num_control_points())
    path_guess = BsplineTrajectory(trajopt.basis(), q_guess)
    trajopt.SetInitialGuess(path_guess)

    # Uncomment this to see the initial guess:
    # PublishPositionTrajectory(path_guess, context, plant, visualizer)

    trajopt.AddDurationCost(1.0)
    trajopt.AddPathLengthCost(1.0)
    trajopt.AddPositionBounds(plant.GetPositionLowerLimits(),
                              plant.GetPositionUpperLimits())
    trajopt.AddVelocityBounds(plant.GetVelocityLowerLimits(),
                              plant.GetVelocityUpperLimits())

    trajopt.AddDurationConstraint(.5, 50)

    # start constraint
    start_constraint = PositionConstraint(plant, plant.world_frame(),
                                          X_WStart.translation(),
                                          X_WStart.translation(), gripper_frame,
                                          [0, 0.1, 0], plant_context)
    trajopt.AddPathPositionConstraint(start_constraint, 0)
    prog.AddQuadraticErrorCost(np.eye(num_q), q0,
                               trajopt.control_points()[:, 0])

    # goal constraint
    goal_constraint = PositionConstraint(plant, plant.world_frame(),
                                         X_WGoal.translation(),
                                         X_WGoal.translation(), gripper_frame,
                                         [0, 0.1, 0], plant_context)
    trajopt.AddPathPositionConstraint(goal_constraint, 1)
    prog.AddQuadraticErrorCost(np.eye(num_q), q0,
                               trajopt.control_points()[:, -1])

    # start and end with zero velocity
    trajopt.AddPathVelocityConstraint(np.zeros((num_q, 1)), np.zeros(
        (num_q, 1)), 0)
    trajopt.AddPathVelocityConstraint(np.zeros((num_q, 1)), np.zeros(
        (num_q, 1)), 1)

    # collision constraints
    collision_constraint = MinimumDistanceConstraint(plant, 0.001,
                                                     plant_context, None, 0.01)
    evaluate_at_s = np.linspace(0, 1, 50)
    for s in evaluate_at_s:
        trajopt.AddPathPositionConstraint(collision_constraint, s)

    result = Solve(prog)
    if not result.is_success():
        print("Trajectory optimization failed")
        print(result.get_solver_id().name())

    PublishPositionTrajectory(trajopt.ReconstructTrajectory(result), context,
                              plant, visualizer)
    collision_visualizer.Publish(
        collision_visualizer.GetMyContextFromRoot(context))


trajopt_bins_demo()


# In[ ]:




