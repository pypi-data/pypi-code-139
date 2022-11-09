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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/pose.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import matplotlib.pyplot as plt
import mpld3
import numpy as np
import pydot
from IPython.display import HTML, SVG, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, BaseField,
                         ConstantValueSource, DepthImageToPointCloud,
                         DiagramBuilder, FindResourceOrThrow,
                         MeshcatPointCloudVisualizer, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, PointCloud,
                         RigidTransform, RollPitchYaw, RotationMatrix,
                         StartMeshcat)

from manipulation import running_as_notebook
from manipulation.scenarios import (AddMultibodyTriad, AddRgbdSensor,
                                    MakeManipulationStation)
from manipulation.utils import FindResource

if running_as_notebook:
    mpld3.enable_notebook()


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Simulating an RGB-D camera
# 
# 

# In[ ]:


def DepthCameraDemoSystem():
    builder = DiagramBuilder()

    # Create the physics engine + scene graph.
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0)
    # Add a single object into it.
    X_Mustard = RigidTransform(RollPitchYaw(-np.pi/2., 0, -np.pi/2.), [0, 0, 0.09515])
    parser = Parser(plant)
    mustard = parser.AddModelFromFile(FindResourceOrThrow(
        "drake/manipulation/models/ycb/sdf/006_mustard_bottle.sdf"))
    plant.WeldFrames(plant.world_frame(), 
                     plant.GetFrameByName("base_link_mustard", mustard), 
                     X_Mustard)

    # Add a box for the camera in the environment.
    X_Camera = RigidTransform(
        RollPitchYaw(0, -0.2, 0.2).ToRotationMatrix().multiply(
            RollPitchYaw(-np.pi/2.0, 0, np.pi/2.0).ToRotationMatrix()),
        [.5, .1, .2])
    camera_instance = parser.AddModelFromFile(FindResource("models/camera_box.sdf"))
    camera_frame = plant.GetFrameByName("base", camera_instance)    
    plant.WeldFrames(plant.world_frame(), camera_frame, X_Camera)
    AddMultibodyTriad(camera_frame, scene_graph, length=.1, radius=0.005)
    plant.Finalize()

    params = MeshcatVisualizerParams()
#    params.delete_on_initialization_event = False
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat, params)

    camera = AddRgbdSensor(builder, scene_graph, X_PC=RigidTransform(),
                           parent_frame_id=plant.GetBodyFrameIdOrThrow(
                               camera_frame.body().index()))
    camera.set_name("rgbd_sensor")

    # Export the camera outputs
    builder.ExportOutput(camera.color_image_output_port(), "color_image")
    builder.ExportOutput(camera.depth_image_32F_output_port(), "depth_image")

    # Add a system to convert the camera output into a point cloud
    to_point_cloud = builder.AddSystem(
        DepthImageToPointCloud(camera_info=camera.depth_camera_info(),
                               fields=BaseField.kXYZs | BaseField.kRGBs))
    builder.Connect(camera.depth_image_32F_output_port(),
                    to_point_cloud.depth_image_input_port())
    builder.Connect(camera.color_image_output_port(),
                    to_point_cloud.color_image_input_port())

    # Send the point cloud to meshcat for visualization, too.
    point_cloud_visualizer = builder.AddSystem(
        MeshcatPointCloudVisualizer(meshcat, "cloud"))
    builder.Connect(to_point_cloud.point_cloud_output_port(),
                    point_cloud_visualizer.cloud_input_port())
    camera_pose = builder.AddSystem(
        ConstantValueSource(AbstractValue.Make(X_Camera)))
    builder.Connect(camera_pose.get_output_port(),
                    point_cloud_visualizer.pose_input_port())

    # Export the point cloud output.
    builder.ExportOutput(to_point_cloud.point_cloud_output_port(),
                         "point_cloud")

    diagram = builder.Build()
    diagram.set_name("depth_camera_demo_system")
    return diagram


# In[ ]:


def plot_camera_images():
    system = DepthCameraDemoSystem()

    # Evaluate the camera output ports to get the images.
    context = system.CreateDefaultContext()
    system.Publish(context)
    color_image = system.GetOutputPort("color_image").Eval(context)
    depth_image = system.GetOutputPort("depth_image").Eval(context)

    # Plot the two images.
    plt.subplot(121)
    plt.imshow(color_image.data)
    plt.title('Color image')
    plt.subplot(122)
    plt.imshow(np.squeeze(depth_image.data))
    plt.title('Depth image')
    #mpld3.display()
    plt.show()

plot_camera_images()


# In[ ]:


def draw_diagram():
    system = DepthCameraDemoSystem()
    display(SVG(pydot.graph_from_dot_data(system.GetGraphvizString(max_depth=1))[0].create_svg()))

draw_diagram()


# In[ ]:


def plot_manipulation_station_camera_images():
    station = MakeManipulationStation(
        filename=FindResource("models/clutter_mustard.dmd.yaml"))
    context = station.CreateDefaultContext()

    index = 1
    plt.figure(figsize=(6, 12))
    for camera_num in range(6):
        color_image = station.GetOutputPort(
            f"camera{camera_num}_rgb_image").Eval(context)
        depth_image = station.GetOutputPort(
            f"camera{camera_num}_depth_image").Eval(context)

        plt.subplot(6, 2, index)
        plt.imshow(color_image.data)
        index += 1
        plt.title('Color image')
        plt.subplot(6, 2, index)
        plt.imshow(np.squeeze(depth_image.data))
        index += 1
        plt.title('Depth image')

    plt.show()

plot_manipulation_station_camera_images()

