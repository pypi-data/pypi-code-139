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


import os
import time
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from pydrake.all import (AddMultibodyPlantSceneGraph, Box, Cylinder,
                         DiagramBuilder, InverseKinematics, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, Rgba, RigidTransform,
                         RollPitchYaw, RotationMatrix, Solve, Sphere,
                         StartMeshcat)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import (MeshcatPoseSliders,
                                        plot_mathematical_program)
from manipulation.scenarios import (AddIiwa, AddPlanarIiwa, AddShape,
                                    AddTwoLinkIiwa, AddWsg)
from manipulation.utils import FindResource


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Interactive inverse kinematics
# 
# This first cell gives us an interface that is very similar to the differential IK teleop interface that we used before.  See if you can spot any differences.

# In[ ]:


def teleop_inverse_kinematics():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddIiwa(plant)
    wsg = AddWsg(plant, iiwa, welded=True)
    plant.Finalize()

    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, 
        scene_graph, 
        meshcat,
        MeshcatVisualizerParams(delete_prefix_initialization_event=False))

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    q0 = plant.GetPositions(plant_context)
    gripper_frame = plant.GetFrameByName("body", wsg)

    def my_callback(context, pose):
        ik = InverseKinematics(plant, plant_context)
        ik.AddPositionConstraint(
            gripper_frame, [0, 0, 0], plant.world_frame(), 
            pose.translation(), pose.translation())
        ik.AddOrientationConstraint(
            gripper_frame, RotationMatrix(), plant.world_frame(), 
            pose.rotation(), 0.0)
        prog = ik.get_mutable_prog()
        q = ik.q()
        prog.AddQuadraticErrorCost(np.identity(len(q)), q0, q)
        prog.SetInitialGuess(q, q0)
        result = Solve(ik.prog())
        clear_output(wait=True)
        if result.is_success():
            print("IK success")
        else:
            print("IK failure")

    sliders = MeshcatPoseSliders(meshcat)
    sliders.SetPose(plant.EvalBodyPoseInWorld(
        plant_context, plant.GetBodyByName("body", wsg)))
    sliders.Run(visualizer, context, my_callback)

teleop_inverse_kinematics()


# This one has a collision to avoid.  Try moving it in positive $y$.

# In[ ]:


meshcat.Delete()


# In[ ]:


def teleop_inverse_kinematics():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddIiwa(plant, "with_box_collision")
    wsg = AddWsg(plant, iiwa, welded=True)
    box = AddShape(plant, Box(0.1, 0.1, 1.0), "box")
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("box", box), RigidTransform([0.25, 0.0, 0.5]))
    plant.Finalize()

    meshcat.DeleteAddedControls()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, 
        scene_graph, 
        meshcat,
        MeshcatVisualizerParams(delete_prefix_initialization_event=False))

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    q0 = plant.GetPositions(plant_context)
    gripper_frame = plant.GetFrameByName("body", wsg)

    def my_callback(context, pose):
        ik = InverseKinematics(plant, plant_context)
        ik.AddPositionConstraint(
            gripper_frame, [0, 0, 0], plant.world_frame(),
            pose.translation(), pose.translation())
        ik.AddOrientationConstraint(
            gripper_frame, RotationMatrix(), plant.world_frame(),
            pose.rotation(), 0.0)
        ik.AddMinimumDistanceConstraint(0.001, 0.1)
        prog = ik.get_mutable_prog()
        q = ik.q()
        prog.AddQuadraticErrorCost(np.identity(len(q)), q0, q)
        prog.SetInitialGuess(q, q0)
        result = Solve(ik.prog())
        clear_output(wait=True)
        if result.is_success():
            print("IK success")
        else:
            print("IK failure")

    sliders = MeshcatPoseSliders(meshcat)
    sliders.SetPose(plant.EvalBodyPoseInWorld(
        plant_context, plant.GetBodyByName("body", wsg)))
    # set the initial z lower, to make the interaction interesting.
    sliders.SetXyz([0.4, -.2, .35])
    sliders.Run(visualizer, context, my_callback)

teleop_inverse_kinematics()


# This one has the hand tracking a cylinder, but is allowed to touch anywhere along the cylinder.  The sliders are controlling the pose of the cylinder. Or you can set `grasp_cylinder` to `False` and just chase the robot around with a stick.

# In[ ]:


meshcat.Delete()


# In[ ]:


def teleop_inverse_kinematics(grasp_cylinder=True):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddIiwa(plant, "with_box_collision")
    wsg = AddWsg(plant, iiwa, welded=True)
    cylinder = AddShape(plant, Cylinder(0.02, 1.0), "cylinder")
    plant.Finalize()

    meshcat.DeleteAddedControls()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, 
        scene_graph, 
        meshcat,
        MeshcatVisualizerParams(delete_prefix_initialization_event=False))

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    q0 = plant.GetPositions(plant_context)
    gripper_frame = plant.GetFrameByName("body", wsg)
    cylinder_body = plant.GetBodyByName("cylinder", cylinder)
    cylinder_frame = plant.GetFrameByName("cylinder", cylinder)

    def my_callback(context, pose):
        ik = InverseKinematics(plant, plant_context)
        ik.AddPositionConstraint(cylinder_frame, [0, 0, 0], plant.world_frame(), pose.translation(), pose.translation())
        ik.AddOrientationConstraint(cylinder_frame, RotationMatrix(), plant.world_frame(), pose.rotation(), 0.0)
        if grasp_cylinder:
            ik.AddPositionConstraint(
                frameB=gripper_frame, p_BQ=[0, 0.1, -0.02],
                frameA=cylinder_frame,
                p_AQ_lower=[0, 0, -0.5], p_AQ_upper=[0, 0, 0.5])
            ik.AddPositionConstraint(
                frameB=gripper_frame, p_BQ=[0, 0.1, 0.02], 
                frameA=cylinder_frame,
                p_AQ_lower=[0, 0, -0.5], p_AQ_upper=[0, 0, 0.5])
        else:
            ik.AddMinimumDistanceConstraint(0.001, 0.1)
        prog = ik.get_mutable_prog()
        q = ik.q()
        prog.AddQuadraticErrorCost(np.identity(len(q)), q0, q)
        prog.SetInitialGuess(q, q0)
        result = Solve(ik.prog())
        clear_output(wait=True)
        if result.is_success():
            print("IK success")
        else:
            print("IK failure")

    sliders = MeshcatPoseSliders(meshcat)
    sliders.SetPose(RigidTransform(
        RollPitchYaw(np.pi/2.0, 0, 0), [0.5, 0, 0.5]))
    sliders.Run(visualizer, context, my_callback)

# Set grasp_cylinder=False if you just want to antagonize the robot with a stick.
teleop_inverse_kinematics(grasp_cylinder=True)


# # Visualizing the configuration space
# 
# I've got the default sampling resolution set fairly fine; it will take a minute or so to run.

# In[ ]:


meshcat.Delete()
meshcat.DeleteAddedControls()


# In[11]:


def draw_configuration_space(shelves=True):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddPlanarIiwa(plant)
    wsg = AddWsg(plant, iiwa, roll=0.0, welded=True)
    sphere = AddShape(plant, Sphere(0.02), "sphere")
    X_WO = RigidTransform([0.6, 0, 0.65])
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("sphere"), X_WO)

    if shelves:
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
    collision_constraint = ik.AddMinimumDistanceConstraint(0.001, 0.01)
    grasp_constraint = ik.AddPositionConstraint(
        gripper_frame, [0, 0.1, 0], sphere_frame, [0, 0, 0], [0, 0, 0])
    
    prog = ik.get_mutable_prog()
    q = ik.q()
    prog.SetInitialGuess(q, q0)
    result = Solve(ik.prog())
    if not result.is_success():
        print("IK failed")

    diagram.Publish(context)

    def eval(q0, q1, q2, c, tol):
        return float(c.evaluator().CheckSatisfied([q0, q1, q2], tol))

    meshcat.Delete()
    meshcat.SetProperty("/Background", "visible", False)
    meshcat.SetObject("initial_guess", Sphere(0.05), Rgba(.4, 1, 1, 1))
    meshcat.SetTransform("initial_guess", RigidTransform(q0))
    meshcat.SetObject("ik_solution", Sphere(0.05), Rgba(.4, .4, 1, 1))
    meshcat.SetTransform("ik_solution", RigidTransform(result.GetSolution(q)))

    low = plant.GetPositionLowerLimits()
    up = plant.GetPositionUpperLimits()
    N = 70 if running_as_notebook else 5
    vertices, triangles = mcubes.marching_cubes_func(
        tuple(low), tuple(up), N, N, N, 
        partial(eval, c=grasp_constraint, tol=0.05), 0.5)
    meshcat.SetTriangleMesh("grasp_constraint", vertices.T, triangles.T,
        Rgba(.5, .9, .5))

    if shelves:
        vertices, triangles = mcubes.marching_cubes_func(
            tuple(low), tuple(up), N, N, N, 
            partial(eval, c=collision_constraint, tol=0.0), 0.5)
        meshcat.SetTriangleMesh("collision_constraint", 
                                vertices.T, triangles.T, Rgba(.9, .5, .5, 1))

# I've made pymcubes optional (it's a heavy dependency)
try:
    import mcubes
    draw_configuration_space(shelves=True)
except ImportError:
    pass


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


# # Basic RRT
# 
# Note that I've inserted a `sleep` command in the visualization to slow things down so you can watch the tree grow.
# 
# TODO(russt): Consider adding the voronoi visualization, but it would add a dependency on scipy.  (That's a big dependency for a little example!)

# In[ ]:


def basic_rrt():
    N = 10000 if running_as_notebook else 3
    Q = np.empty((N,2))
    rng = np.random.default_rng()
    Q[0] = rng.random((1,2))

    meshcat.Delete()
    meshcat.Set2dRenderMode(xmin=0, xmax=1, ymin=0, ymax=1)

    start = np.empty((N,3))
    end = np.empty((N,3))
    id = 0
    for n in range(1,N):
        q_sample = rng.random((1,2))[0]
        distance_sq = np.sum((Q[:n] - q_sample)**2, axis=1)
        closest = np.argmin(distance_sq)
        distance = np.sqrt(distance_sq[closest])
        if (distance > .1):
            q_sample = (Q[closest]+(.1/distance)*(q_sample - Q[closest]))
        start[n] = [Q[closest, 0], 0, Q[closest,1]]
        end[n] = [q_sample[0], 0, q_sample[1]]
        if (n < 1000 and n % 100 == 1) or n % 1000 == 1:
            meshcat.SetLineSegments("rrt", start[:n+1].T, end[:n+1].T)
            time.sleep(0.1)  # sleep to slow things down.
        Q[n] = q_sample

basic_rrt()


# # RRT Bug trap
# 
# For bonus points, I'll use SceneGraph for the collision checking.
# 
# TODO(russt):
# - Take bigger steps, but check collisions at subsamples along an edge.
# - Add a goal + goal-bias
# - Make a version where the robot has geometry, and the collision checks call `plant.SetPosition()`, then `query.HasCollisions()`

# In[ ]:


def rrt_bugtrap():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    thickness = .05
    MITred = [.6, .2, .2, 1]
    wall = AddShape(plant, Box(.8, 1.0, thickness), "bottom", color=MITred)
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("bottom", wall),
                     RigidTransform([0.5, 0, 0.1+thickness/2]))
    wall = AddShape(plant, Box(0.8, 1.0, thickness), "top", color=MITred)
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("top", wall),
                     RigidTransform([0.5, 0, 0.9-thickness/2]))
    wall = AddShape(plant,
                    Box(thickness, 1.0, .8 - thickness),
                    "left",
                    color=MITred)
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("left", wall),
                     RigidTransform([0.1+thickness/2, 0, 0.5]))
    wall = AddShape(plant, Box(thickness, 1.0, .34), "right_top", color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("right_top", wall),
                     RigidTransform([0.9 - thickness / 2, 0, 0.9 - .17]))
    wall = AddShape(plant,
                    Box(thickness, 1.0, .34),
                    "right_bottom",
                    color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("right_bottom", wall),
                     RigidTransform([0.9 - thickness / 2, 0, 0.1 + .17]))
    wall = AddShape(plant, Box(0.36, 1.0, thickness), "trap_top", color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("trap_top", wall),
                     RigidTransform([0.9 - .18, 0, .9 - thickness / 2 - .33]))
    wall = AddShape(plant, Box(0.36, 1.0, thickness), "trap_bottom", color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("trap_bottom", wall),
                     RigidTransform([0.9 - .18, 0, .1 + thickness / 2 + .33]))
    plant.Finalize()

    meshcat.Delete()
    meshcat.Set2dRenderMode(xmin=0, xmax=1, ymin=0, ymax=1)

    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    diagram.Publish(context)
    query = scene_graph.get_query_output_port().Eval(
        scene_graph.GetMyContextFromRoot(context))

    q_init = [.3, .3]

    N = 10000 if running_as_notebook else 3
    Q = np.empty((N,2))
    rng = np.random.default_rng()
    Q[0] = q_init

    start = np.empty((N,3))
    end = np.empty((N,3))

    max_length = thickness/4
    n = 1
    while n < N:
        q_sample = rng.random((1,2))[0]
        distance_sq = np.sum((Q[:n] - q_sample)**2, axis=1)
        closest = np.argmin(distance_sq)
        distance = np.sqrt(distance_sq[closest])
        if (distance > max_length):
            q_sample = (Q[closest]+(max_length/distance)*(q_sample - Q[closest]))
        if query.ComputeSignedDistanceToPoint([q_sample[0], 0, q_sample[1]], 0.0):
            # Then the sample point is in collision...
            continue
        start[n] = [Q[closest, 0], 0, Q[closest,1]]
        end[n] = [q_sample[0], 0, q_sample[1]]
        if (n < 1000 and n % 100 == 1) or n % 1000 == 1:
            meshcat.SetLineSegments("rrt", start[:n+1].T, end[:n+1].T)
            time.sleep(0.1)  # sleep to slow things down.

        Q[n] = q_sample
        n += 1


rrt_bugtrap()


# In[ ]:




