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
from pydrake.all import (AddMultibodyPlantSceneGraph, DiagramBuilder,
                         FindResourceOrThrow, MeshcatVisualizer, Parser,
                         RigidTransform, RotationMatrix, StartMeshcat)

from manipulation import FindResource, running_as_notebook
from manipulation.scenarios import SetColor


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Compute grasp and pregrasp poses
# 
# Here is a simple example with a floating Schunk gripper and the foam brick.  It defines the grasp pose as described in the notes, and renders it to the 3D visualizer.
# 
# **Check yourself**: Try changing the grasp pose to our pregrasp pose.  Do you like the numbers that I picked in the text?

# In[ ]:


def grasp_poses_example():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step = 0.0)
    parser = Parser(plant, scene_graph)
    grasp = parser.AddModelFromFile(FindResourceOrThrow(
        "drake/manipulation/models/wsg_50_description/sdf/schunk_wsg_50_no_tip.sdf"), "grasp")
    pregrasp = parser.AddModelFromFile(FindResourceOrThrow(
        "drake/manipulation/models/wsg_50_description/sdf/schunk_wsg_50_no_tip.sdf"), "pregrasp")
    brick = parser.AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf"))
    plant.Finalize()

    B_O = plant.GetBodyByName("base_link", brick)
    B_Ggrasp = plant.GetBodyByName("body", grasp)
    B_Gpregrasp = plant.GetBodyByName("body", pregrasp)

    # Set the pregrasp to be green and slightly transparent.
    inspector = scene_graph.model_inspector()
    for body_index in plant.GetBodyIndices(pregrasp):
        SetColor(
            scene_graph, [0, .6, 0, .5], plant.get_source_id(), 
            inspector.GetGeometries(plant.GetBodyFrameIdOrThrow(body_index)))

    meshcat.Delete()
    meshcat.SetProperty("/Background", "visible", False)
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    # TODO(russt): Set a random pose of the object.

    # Get the current object, O, pose
    X_WO = plant.EvalBodyPoseInWorld(plant_context, B_O)

    p_GgraspO = [0, 0.11, 0]
    R_GgraspO = RotationMatrix.MakeXRotation(np.pi/2.0).multiply(
        RotationMatrix.MakeZRotation(np.pi/2.0))
    X_GgraspO = RigidTransform(R_GgraspO, p_GgraspO)
    X_OGgrasp = X_GgraspO.inverse()
    X_WGgrasp = X_WO.multiply(X_OGgrasp)

    # pregrasp is negative y in the gripper frame (see the figure!).
    X_GgraspGpregrasp = RigidTransform([0, -0.08, 0])
    X_WGpregrasp = X_WGgrasp @ X_GgraspGpregrasp

    plant.SetFreeBodyPose(plant_context, B_Ggrasp, X_WGgrasp)
    # Open the fingers, too.
    plant.GetJointByName("left_finger_sliding_joint", grasp).set_translation(plant_context, -0.054)
    plant.GetJointByName("right_finger_sliding_joint", grasp).set_translation(plant_context, 0.054)

    plant.SetFreeBodyPose(plant_context, B_Gpregrasp, X_WGpregrasp)
    # Open the fingers, too.
    plant.GetJointByName("left_finger_sliding_joint", pregrasp).set_translation(plant_context, -0.054)
    plant.GetJointByName("right_finger_sliding_joint", pregrasp).set_translation(plant_context, 0.054)    

    diagram.Publish(context)

grasp_poses_example()


# In[ ]:




