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


# Let's do all of our imports here, too.
import numpy as np
from pydrake.all import (AddMultibodyPlantSceneGraph, AngleAxis,
                         DiagramBuilder, FindResourceOrThrow, Integrator,
                         JacobianWrtVariable, LeafSystem, MeshcatVisualizer,
                         MultibodyPlant, MultibodyPositionToGeometryPose,
                         Parser, PiecewisePolynomial, PiecewiseQuaternionSlerp,
                         Quaternion, RigidTransform, RollPitchYaw,
                         RotationMatrix, SceneGraph, Simulator, StartMeshcat,
                         TrajectorySource)

from manipulation.scenarios import AddMultibodyTriad


# In[ ]:


meshcat = StartMeshcat()


# In[ ]:


builder = DiagramBuilder()

plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step = 0.0)
parser = Parser(plant, scene_graph)
grasp = parser.AddModelFromFile(FindResourceOrThrow(
    "drake/manipulation/models/wsg_50_description/sdf/schunk_wsg_50_no_tip.sdf"), "grasp")
# TODO(russt): Draw the pregrasp gripper, too, as transparent (drake #13970).
#pregrasp = parser.AddModelFromFile(FindResourceOrThrow(
#    "drake/manipulation/models/wsg_50_description/sdf/schunk_wsg_50_no_tip.sdf"), "pregrasp")
brick = parser.AddModelFromFile(FindResourceOrThrow(
    "drake/examples/manipulation_station/models/061_foam_brick.sdf"), "brick")
AddMultibodyTriad(plant.GetFrameByName("body", grasp), scene_graph)
AddMultibodyTriad(plant.GetFrameByName("base_link", brick), scene_graph)
plant.Finalize()

MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)

diagram = builder.Build()
context = diagram.CreateDefaultContext()
plant_context = plant.GetMyContextFromRoot(context)

# TODO(russt): Set a random pose of the object.

# Get the current object, O, pose
B_O = plant.GetBodyByName("base_link", brick)
X_WO = plant.EvalBodyPoseInWorld(plant_context, B_O)

B_Ggrasp = plant.GetBodyByName("body", grasp)
p_GgraspO = [0, 0.11, 0]
R_GgraspO = RotationMatrix.MakeXRotation(np.pi/2.0).multiply(
    RotationMatrix.MakeZRotation(np.pi/2.0))
# Useful for a better image:
p_GgraspO = [0, 0.3, 0.1]
R_GgraspO = R_GgraspO.multiply(RotationMatrix.MakeYRotation(0.5))
X_GgraspO = RigidTransform(R_GgraspO, p_GgraspO)
X_OGgrasp = X_GgraspO.inverse()
X_WGgrasp = X_WO.multiply(X_OGgrasp)

print(f"p_GO_W = {X_WGgrasp.rotation().multiply(X_GgraspO.translation())}")
print(f"p_GO_G = {X_GgraspO.translation()}")
print(f"p_OG_O = {X_OGgrasp.translation()}")

plant.SetFreeBodyPose(plant_context, B_Ggrasp, X_WGgrasp)
# Open the fingers, too.
plant.GetJointByName("left_finger_sliding_joint", grasp).set_translation(plant_context, -0.054)
plant.GetJointByName("right_finger_sliding_joint", grasp).set_translation(plant_context, 0.054)

diagram.Publish(context)


# In[ ]:




