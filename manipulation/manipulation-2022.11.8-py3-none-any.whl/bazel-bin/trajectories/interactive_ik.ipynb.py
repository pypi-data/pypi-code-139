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
from IPython.display import clear_output
from pydrake.all import (AddMultibodyPlantSceneGraph, Box, Cylinder,
                         DiagramBuilder, InverseKinematics, MeshcatVisualizer,
                         MeshcatVisualizerParams, RigidTransform, Role,
                         RollPitchYaw, RotationMatrix, Solve, StartMeshcat)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import MeshcatPoseSliders
from manipulation.scenarios import AddIiwa, AddShape, AddWsg


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
        if result.is_success():
            print("IK success")
        else:
            print("IK failure")
        clear_output(wait=True)

    meshcat.DeleteAddedControls()
    sliders = MeshcatPoseSliders(meshcat)
    sliders.SetPose(plant.EvalBodyPoseInWorld(
        plant_context, plant.GetBodyByName("body", wsg)))
    sliders.Run(visualizer, context, my_callback)

teleop_inverse_kinematics()


# This one has a collision to avoid.  Try moving it in positive $y$.

# In[ ]:


def teleop_inverse_kinematics():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddIiwa(plant, "with_box_collision")
    wsg = AddWsg(plant, iiwa, welded=True)
    box = AddShape(plant, Box(0.1, 0.1, 1.0), "box")
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("box", box), RigidTransform([0.25, 0.0, 0.5]))
    plant.Finalize()

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, 
        scene_graph, 
        meshcat,
        MeshcatVisualizerParams())
    collision = MeshcatVisualizer.AddToBuilder(
        builder, 
        scene_graph, 
        meshcat,
        MeshcatVisualizerParams(prefix="collision", role=Role.kProximity))
    meshcat.SetProperty("collision", "visible", False)

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
        if result.is_success():
            print("IK success")
        else:
            print("IK failure")
        clear_output(wait=True)

    sliders = MeshcatPoseSliders(meshcat)
    sliders.SetPose(plant.EvalBodyPoseInWorld(
        plant_context, plant.GetBodyByName("body", wsg)))
    # set the initial z lower, to make the interaction interesting.
    sliders.SetXyz([0.4, -.2, .35])
    sliders.Run(diagram, context, my_callback)

teleop_inverse_kinematics()


# This one has the hand tracking a cylinder, but is allowed to touch anywhere along the cylinder.  The sliders are controlling the pose of the cylinder. Or you can set `grasp_cylinder` to `False` and just chase the robot around with a stick.

# In[ ]:


def teleop_inverse_kinematics(grasp_cylinder=True):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddIiwa(plant, "with_box_collision")
    wsg = AddWsg(plant, iiwa, welded=True)
    cylinder = AddShape(plant, Cylinder(0.02, 1.0), "cylinder")
    plant.Finalize()

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, 
        scene_graph, 
        meshcat,
        MeshcatVisualizerParams())

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
        if result.is_success():
            print("IK success")
        else:
            print("IK failure")
        clear_output(wait=True)

    sliders = MeshcatPoseSliders(meshcat)
    sliders.SetPose(RigidTransform(
        RollPitchYaw(np.pi/2.0, 0, 0), [0.5, 0, 0.5]))
    sliders.Run(visualizer, context, my_callback)

# Set grasp_cylinder=False if you just want to antagonize the robot with a stick.
teleop_inverse_kinematics(grasp_cylinder=True)


# In[ ]:




