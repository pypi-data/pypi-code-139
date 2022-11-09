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

# ## Pose Estimation with ICP

# In[ ]:


import numpy as np
from manipulation import running_as_notebook
from manipulation.icp import IterativeClosestPoint
from manipulation.scenarios import AddMultibodyTriad, AddRgbdSensors, AddShape
from pydrake.all import (AddMultibodyPlantSceneGraph, BaseField, Box,
                         DepthImageToPointCloud, DiagramBuilder, Fields,
                         FindResourceOrThrow, MeshcatPointCloudVisualizer,
                         MeshcatVisualizer, Parser, PixelType, PointCloud,
                         Rgba, RigidTransform, RollPitchYaw, RotationMatrix,
                         Simulator, SpatialInertia, StartMeshcat)


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# ## Problem Description
# Last lecture, we designed pick and place trajectories **assuming** that the object pose ${}^W X^O$ was known. With all the tools we have learned for goemetric perception, it is time to relax this assumption and finally do pose estimation from sensor data. 
# 
# The goal of the exercise is to give you some real-world experience into what dealing with depth cameras, and what it takes to go from a real depth image to the clean ICP formulation we learned.
# 
# **These are the main steps of the exercise:**
# 1. Perform Segmentation on the raw pointcloud of the scene to extract pointcloud from the object.
# 2. Tune an off-the-shelf ICP solver and estimate the pose of the object.

# Before jumping into the main exercise, how should we computationally represent a pointcloud? If we say that pointcloud has $N$ points, then each point has a position in 3D, ${}^Cp^i$, as well as an associated color. Throughout this exercise, we will tend to store them as separate arrays of:
# - `3xN` numpy array where each row stores the XYZ position of the point in meters.
# - `3xN` numpy array where each row stores the RGB information of the point in `uint8` format. 
# 
# Unfortunately, numpy prefers a rowwise representation, so you might find yourself using the `.T` transpose operator to make numpy operations more natural/efficient.

# In[ ]:


def ToPointCloud(xyzs, rgbs=None):
    if rgbs:
        cloud = PointCloud(xyzs.shape[1], BaseField.kXYZs | BaseField.kRGBs)
        cloud.mutable_rgbs()[:] = rgbs
    else:
        cloud = PointCloud(xyzs.shape[1])
    cloud.mutable_xyzs()[:] = xyzs
    return cloud


# ## Getting a Pointcloud of the Model ##
# 
# Before taking a pointcloud of the **scene**, we will need a pointcloud of the **model** to compare against. Generally, this can be done by using existing tools that convert 3D representations (meshes, signed distance functions, etc.) into pointclouds.  
# 
# Since our red foam brick is of rectangular shape, we'll cheat a bit and generate the points procedurally. When you click the cell below, you should be able to see the red brick and our pointcloud representation of the brick as blue dots. 
# 
# We will save the model pointcloud in the variable `model_pcl_np`. 

# In[ ]:


def visualize_red_foam_brick():
    """
  Visualize red foam brick in Meshcat.
  """
    builder = DiagramBuilder()
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0)
    parser = Parser(plant)
    parser.AddModelFromFile(FindResourceOrThrow(
          "drake/examples/manipulation_station/models/061_foam_brick.sdf"))
    AddMultibodyTriad(plant.GetFrameByName("base_link"), scene_graph)
    plant.Finalize()

    # Setup Meshcat
    MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)
    builder.Build()

def generate_model_pointcloud(xrange, yrange, zrange, res):
    """
  Procedurally generate pointcloud of a rectangle for each side. 
  """
    # Decide on how many samples
    x_lst = np.linspace(xrange[0], xrange[1], int((xrange[1] - xrange[0]) / res))
    y_lst = np.linspace(yrange[0], yrange[1], int((yrange[1] - yrange[0]) / res))
    z_lst = np.linspace(zrange[0], zrange[1], int((zrange[1] - zrange[0]) / res))

    pcl_lst = []
    # Do XY Plane
    for x in x_lst:
        for y in y_lst:
            pcl_lst.append([x, y, zrange[0]])
            pcl_lst.append([x, y, zrange[1]])

    # Do YZ Plane
    for y in y_lst:
        for z in z_lst:
            pcl_lst.append([xrange[0], y, z])
            pcl_lst.append([xrange[1], y, z])

    # Do XZ Plane
    for x in x_lst:
        for z in z_lst:
            pcl_lst.append([x, yrange[0], z])
            pcl_lst.append([x, yrange[1], z])


    return np.array(pcl_lst).T

visualize_red_foam_brick()
model_pcl_np = generate_model_pointcloud([-0.0375, 0.0375], [-0.025, 0.025], [0., 0.05], 0.002)
meshcat.SetObject("pcl_model",
                  ToPointCloud(model_pcl_np),
                  rgba=Rgba(0, 0, 1, 1))


# ## Getting the Scene Pointcloud
# 
# Now let's set up the ClutteringStation from last lecture and actually take a pointcloud snapshot of the scene with the `red_foam_brick`. We'll place the camera where we have good coverage of the bin. We'll also take a pointcloud snapshot without the `red_foam_brick` so that we can use it for segmentation later.
# 
# NOTE: There are around `3e7` points that are trying to be published to the visualizer, so things might load slowly, and occasionally the Colab session might crash. Keep calm and run the cells from the beginning! 

# In[ ]:


meshcat.Delete()

def setup_clutter_station(X_WO, X_WC):
  builder = DiagramBuilder()
  
  plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0)
  parser = Parser(plant)

  # Add the foam brick. 
  if (X_WO is not None):
    brick = parser.AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf"))
    plant.WeldFrames(plant.world_frame(),
                    plant.GetFrameByName("base_link", brick),
                    X_WO)
  
  bin1 = parser.AddModelFromFile(FindResourceOrThrow(
      "drake/examples/manipulation_station/models/bin.sdf"), "bin1")
  plant.WeldFrames(plant.world_frame(),
                   plant.GetFrameByName("bin_base", bin1),
                   RigidTransform(RollPitchYaw(0, 0, np.pi/2), [-0.145, -0.63, 0.075]))

  bin2 = parser.AddModelFromFile(FindResourceOrThrow(
      "drake/examples/manipulation_station/models/bin.sdf"), "bin2")
  plant.WeldFrames(plant.world_frame(),
                   plant.GetFrameByName("bin_base", bin2),
                   RigidTransform(RollPitchYaw(0, 0, np.pi), [0.5, -0.1, 0.075]))

  # Add a mock camera model  
  camera_instance = AddShape(plant, Box(
      width=.1, depth=.02, height=.02), "camera", color=[.4, .4, .4, 1.])
  plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("camera"), X_WC) 
  AddMultibodyTriad(plant.GetFrameByName("camera"), scene_graph)
  plant.Finalize() 

  MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)

  AddRgbdSensors(builder, plant, scene_graph)

  # Send the point cloud to meshcat for visualization, too.
#  meshcat_pointcloud = builder.AddSystem(MeshcatPointCloudVisualizer(meshcat, X_WP=X_WC, draw_period=1./5.))
#  builder.Connect(to_point_cloud.point_cloud_output_port(), meshcat_pointcloud.get_input_port())

  diagram = builder.Build()
  diagram.set_name("depth_camera_demo_system")
  return diagram 

# Set pose of the brick 
X_WO = RigidTransform(RollPitchYaw(0, 0, np.pi/5).ToRotationMatrix(), np.array([-0.1, -0.6, 0.09]))

# Setup CameraPose
X_WC = RigidTransform(
    RollPitchYaw(0, 0, 0).ToRotationMatrix().multiply(
        RollPitchYaw(-np.pi/2. - np.pi/3, 0, 0).ToRotationMatrix()),
    [-.1, -.8, .5])

# Take a pointcloud snapshot of the background to use for subtraction 
diagram = setup_clutter_station(None, X_WC)
simulator = Simulator(diagram)
simulator.AdvanceTo(0.01)
context = simulator.get_context()
# Note: Use PointCloud here to make a copy of the data, since the diagram that
# owns it will be garbage collected.
scene_pcl_drake_background = PointCloud(diagram.GetOutputPort(
    "camera_point_cloud").Eval(context))

# Take a pointcloud snapshot of the scene with the brick. 
diagram = setup_clutter_station(X_WO, X_WC)
simulator = Simulator(diagram)
simulator.AdvanceTo(0.01)
context = simulator.get_context()
scene_pcl_drake = diagram.GetOutputPort("camera_point_cloud").Eval(context)


# ## Visualizing the Problem ##
# 
# That was a lot of work, but if you run the below cell, Meshcat will finally show you a clean formulation of the main problem. We have 3 pointcloud objects in Meshcat:
# 
# - `pcl_model`: Pointcloud of models
# - `pcl_scene`: Raw pointcloud of the foam-brick scene obtained from a RGBD camera.
# - `pcl_scene_background`: Raw pointcloud of the background obtained from a RGBD camera. 
# 
# In case you forgot, In Meshcat's menu you can go into the `meshcat` tab and turn different objects on and off so that you can see what the background pointcloud looks like as well. 
# 
# NOTE: You might have to wait a bit until the bin pointcloud shows up.
# 
# 

# In[ ]:


meshcat.Delete()

meshcat.SetObject("pcl_model",
                  ToPointCloud(model_pcl_np),
                  rgba=Rgba(0, 0, 1, 1))
meshcat.SetObject("pcl_scene", scene_pcl_drake)
meshcat.SetObject("pcl_scene_background", scene_pcl_drake_background)


# If we simply run ICP with `pcl_model` and `pcl_scene`, we might get a terrible result because there might be features in the background that the model is trying to run correspondence with. So we'd like to vet the problem a bit and perform **segmentation**: which parts of the scene pointcloud corresponds to an actual point on the `red_foam_brick`? 
# 
# 
# **Now it's your turn to code!**
# 
# Below, you will implement a function `segment_scene_pcl` that takes in a pointcloud of the scene and return the relevant points that are actually on the `red_foam_brick`. But here are the rules of the game:
# - You **may** use color data, the background pointcloud, and any outlier detection algorithm that you can write to perform segmentation.
# - You may **not** explicitly impose conditions on the position to filter out the data. Remember that our goal is to estimate the pose in the first place, so using position will be considered cheating.
# - You may **not** use external libraries that are not in this notebook already. 
# 
# In order to get full score for this assignment, you need to satisfy both criteria:
# - The number of false outliers (points which are not on the red brick but was caught by segmentation) must not exceed 80 points.
# - The number of missed inliers (points that are on the red brick but was not caught by segmentation) must not exceed 80 points. 
# 
# You will be able to visualize your segmented pointclouds on Meshcat by running the cell.

# In[ ]:


def segment_scene_pcl(scene_pcl_np, scene_rgb_np, scene_pcl_np_background,
                      scene_rgb_np_background):
    """
    Inputs: 
    scene_pcl_np: 3xN np.float32 array of pointclouds, each row containing xyz 
                    position of each point in meters. 
    scene_rgb_np: 3xN np.uint8   array of pointclouds, each row containing rgb 
                    color data of each point.
    scene_pcl_np_background: 3xN np.float32 array of pointclouds, each row 
                    containing xyz position of each point in meters. 
    scene_rgb_np_background: 3xN np.uint8   array of pointclouds, each row 
                    containing rgb color data of each point.

    Outputs:
    scene_pcl_np_filtered: 3xM np.float32 array of pointclouds that are on the 
                    foam brick. 
    """
    ####################
    # Fill your code here.

    scene_pcl_np_filtered = scene_pcl_np
    ####################

    return scene_pcl_np_filtered


scene_pcl_np_filtered = segment_scene_pcl(
    scene_pcl_drake.xyzs(),
    scene_pcl_drake.rgbs(),
    scene_pcl_drake_background.xyzs(),
    scene_pcl_drake_background.rgbs())
meshcat.SetObject("pcl_scene_filtered",
                  ToPointCloud(scene_pcl_np_filtered),
                  rgba=Rgba(0, 1, 0, 1))


# ## ICP for Pose Estimation
# 
# Now that we have a subset of scene points that we want to use to estimate the pose, let's do ICP to figure out what ${}^W X^O$ is. Instead of implementing your own ICP this time, we will use the version we developed in the chapter notes.
# 
# We know that ICP can't work very well without even a rough initialization. Let's assume that we at least know that the `red_foam_brick` is inside the bin, so that we can initialize the ${}^W X^O$ to be at the center of the bin with an identity rotation. 

# In[ ]:


initial_guess = RigidTransform()
initial_guess.set_translation([-0.145, -0.63, 0.09])
initial_guess.set_rotation(RotationMatrix.MakeZRotation(np.pi/2))


# Let's run the algorithm on your processed point cloud and see how we do!
# 

# In[ ]:


X_MS_hat, chat = IterativeClosestPoint(
    p_Om=model_pcl_np,
    p_Ws=scene_pcl_np_filtered,
    X_Ohat=initial_guess,
    meshcat=meshcat,
    meshcat_scene_path='icp',
    max_iterations=None if running_as_notebook else 2)
meshcat.SetObject("pcl_estimated",
                  ToPointCloud(model_pcl_np),
                  rgba=Rgba(1, 0, 1, 1))
meshcat.SetTransform("pcl_estimated", X_MS_hat)

np.set_printoptions(precision=3, suppress=True)
X_OOhat = X_MS_hat.inverse().multiply(X_WO)

rpy = RollPitchYaw(X_OOhat.rotation()).vector()
xyz = X_OOhat.translation()

print("RPY Error: " + str(rpy))
print("XYZ Error: " + str(xyz))


# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do as follows:. 
# - Download and submit the notebook `pick_and_place_perception.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [4 pts] `segment_scene_pcl` correctly segments the scene by having less than 80 missed inliers and 80 false outliers.
# 
# Below is our autograder where you can check your score!

# In[ ]:


from manipulation.exercises.pose.test_pose_estimation import TestPoseEstimation
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestPoseEstimation], [locals()], 'results.json')
Grader.print_test_results('results.json')


# In[ ]:




