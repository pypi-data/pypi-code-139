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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/clutter.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML, display
from pydrake.all import (AddMultibodyPlantSceneGraph, Box,
                         ConnectPlanarSceneGraphVisualizer, CoulombFriction,
                         DiagramBuilder, DrakeVisualizer, FindResourceOrThrow,
                         FixedOffsetFrame, JointIndex, Parser, PlanarJoint,
                         RandomGenerator, RigidTransform, RollPitchYaw,
                         RotationMatrix, Simulator,
                         UniformlyRandomRotationMatrix)

from manipulation import running_as_notebook
from manipulation.scenarios import (AddFloatingRpyJoint, AddRgbdSensor,
                                    AddShape, ycb)


# # Falling things (in 2D)
# 

# In[ ]:


def clutter_gen():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)

    # Add the ground.
    ground = AddShape(plant,
                      Box(10., 10., 10.),
                      "ground",
                      color=[.9, .9, .9, 1.0])
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("ground", ground),
                     RigidTransform([0, 0, -5]))

    # Add the bricks, each attached to the world via a planar joint.
    parser = Parser(plant)
    sdf = FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf")
    planar_joint_frame = plant.AddFrame(FixedOffsetFrame("planar_joint_frame", plant.world_frame(), RigidTransform(RotationMatrix.MakeXRotation(np.pi/2))))
    for i in range(20 if running_as_notebook else 2):
        instance = parser.AddModelFromFile(sdf, f"object{i}")
        plant.AddJoint(
            PlanarJoint(f"joint{i}",
                        planar_joint_frame,
                        plant.GetFrameByName("base_link", instance),
                        damping=[0, 0, 0]))

    plant.Finalize()

    vis = ConnectPlanarSceneGraphVisualizer(
        builder,
        scene_graph,
        xlim=[-.6, .6],
        ylim=[-.1, 0.5],
        show=False,
    )

    diagram = builder.Build()
    simulator = Simulator(diagram)
    plant_context = plant.GetMyContextFromRoot(simulator.get_mutable_context())

    rs = np.random.RandomState()
    z = 0.1
    for i in range(plant.num_joints()):
        joint = plant.get_joint(JointIndex(i))
        if (isinstance(joint, PlanarJoint)):
            joint.set_pose(plant_context, [rs.uniform(-.4, .4), z], rs.uniform(-np.pi/2.0, np.pi/2.0))
            z += 0.1

    vis.start_recording()
    simulator.AdvanceTo(1.5 if running_as_notebook else 0.1)
    vis.stop_recording()
    ani = vis.get_recording_as_animation(repeat=False)
    display(HTML(ani.to_jshtml()))

clutter_gen()


# # Falling things (in 3D)
# 
# I had to decide how to visualize the results of this one for you. The mesh and
# texture map files for the YCB objects are very large, so downloading many of
# them to your browser from an online notebook felt a bit too painful. If you've
# decided to run the notebooks from source on your local machine, then go ahead
# and run 
# ```
# bazel run //tools:drake_visualizer
# ```
# before running this test to see the live simulation (`drake visualizer` will load
# the mesh files directly from your disk, so avoids the download). For the cloud
# notebooks, I've decided to add a camera to the scene and take a picture after
# simulating for a few seconds.  After all, that's perhaps the data that we're
# actually looking for.
# 
# [Note](https://stackoverflow.com/questions/73873885/meshcat-fails-to-import-png-for-cracker-box-in-drake-planar-force-control-demo) that Drake's pip installation doesn't currently include the texture maps for the YCB objects, because they're too big to fit in the `pip` wheel 100MB limit. 

# In[ ]:


def clutter_gen():
    rs = np.random.RandomState()  # this is for python
    generator = RandomGenerator(rs.randint(1000))  # this is for c++

    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0005)

    parser = Parser(plant)

    parser.AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/bin.sdf"))
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("bin_base"))

    for i in range(10 if running_as_notebook else 2):
        object_num = rs.randint(len(ycb))
        sdf = FindResourceOrThrow("drake/manipulation/models/ycb/sdf/"
                                  + ycb[object_num])
        parser.AddModelFromFile(sdf, f"object{i}")

    plant.Finalize()

    camera = AddRgbdSensor(builder, scene_graph, RigidTransform(
        RollPitchYaw(np.pi, 0, np.pi / 2.0), [0, 0, .8]))
    builder.ExportOutput(camera.color_image_output_port(), "color_image")

    vis = DrakeVisualizer.AddToBuilder(builder, scene_graph)

    diagram = builder.Build()
    simulator = Simulator(diagram)
    context = simulator.get_mutable_context()
    plant_context = plant.GetMyContextFromRoot(context)

    z = 0.1
    for body_index in plant.GetFloatingBaseBodies():
        tf = RigidTransform(
                UniformlyRandomRotationMatrix(generator),
                [rs.uniform(-.15,.15), rs.uniform(-.2, .2), z])
        plant.SetFreeBodyPose(plant_context,
                              plant.get_body(body_index),
                              tf)
        z += 0.1

    simulator.AdvanceTo(1.0 if running_as_notebook else 0.1)
    color_image = diagram.GetOutputPort("color_image").Eval(context)
    plt.figure()
    plt.imshow(color_image.data)
    plt.axis('off')

clutter_gen()


# In[ ]:




