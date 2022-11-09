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
                         DiagramBuilder, JointSliders, LeafSystem,
                         MeshcatVisualizer, Parser, RigidTransform,
                         RollPitchYaw, StartMeshcat)

from manipulation import FindResource, running_as_notebook
from manipulation.scenarios import AddMultibodyTriad, AddPackagePaths


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Forward kinematics of the gripper frame
# 
# Here is a simple example that let's you visualize the frames on the iiwa and the gripper.  If you click on the "Open Controls" menu in the MeshCat visualizer, and dig into the menu `meshcat->drake->Source` then you will see elements for each of the models in the `SceneGraph`: one for the iiwa, another for the WSG, and others for the clutter bins.  You can enable/disable their visualization.  Give it a spin!

# In[ ]:


class PrintPose(LeafSystem):
    def __init__(self, body_index):
        LeafSystem.__init__(self)
        self._body_index = body_index
        self.DeclareAbstractInputPort("body_poses",
                                    AbstractValue.Make([RigidTransform()]))
        self.DeclareForcedPublishEvent(self.Publish)

    def Publish(self, context):
        pose = self.get_input_port().Eval(context)[self._body_index]
        print(pose)
        print("gripper position (m): " + np.array2string(
            pose.translation(), formatter={
                'float': lambda x: "{:3.2f}".format(x)}))
        print("gripper roll-pitch-yaw (rad):" + np.array2string(
            RollPitchYaw(pose.rotation()).vector(),
                         formatter={'float': lambda x: "{:3.2f}".format(x)}))
        clear_output(wait=True)

def gripper_forward_kinematics_example():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0)
    parser = Parser(plant)
    AddPackagePaths(parser)
    parser.AddAllModelsFromFile(FindResource("models/iiwa_and_wsg.dmd.yaml"))
    plant.Finalize()

    # Draw the frames
    for body_name in ["iiwa_link_1", "iiwa_link_2", "iiwa_link_3", "iiwa_link_4", "iiwa_link_5", "iiwa_link_6", "iiwa_link_7", "body"]:
        AddMultibodyTriad(plant.GetFrameByName(body_name), scene_graph)

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph.get_query_output_port(), meshcat)

    wsg = plant.GetModelInstanceByName("wsg")
    gripper = plant.GetBodyByName("body", wsg)
    print_pose = builder.AddSystem(PrintPose(gripper.index()))
    builder.Connect(plant.get_body_poses_output_port(),
                    print_pose.get_input_port())

    default_interactive_timeout = None if running_as_notebook else 1.0
    sliders = builder.AddSystem(JointSliders(meshcat, plant))
    diagram = builder.Build()
    sliders.Run(diagram, default_interactive_timeout)
    meshcat.DeleteAddedControls()

gripper_forward_kinematics_example()


# In[ ]:




