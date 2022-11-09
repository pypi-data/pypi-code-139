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


# Let's do all of our imports here, too.
import os

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import open3d as o3d
import pydot
from IPython.display import HTML, SVG, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, AngleAxis,
                         BaseField, ConstantValueSource, CsdpSolver,
                         DepthImageToPointCloud, DiagramBuilder,
                         DifferentialInverseKinematicsIntegrator,
                         DifferentialInverseKinematicsParameters, EventStatus,
                         FindResourceOrThrow, LeafSystem,
                         MakePhongIllustrationProperties, MathematicalProgram,
                         MeshcatPointCloudVisualizer, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, PiecewisePolynomial,
                         PiecewisePose, PointCloud, RigidTransform,
                         RollPitchYaw, RotationMatrix, Simulator, StartMeshcat,
                         ge)
from pydrake.examples.manipulation_station import ManipulationStation

from manipulation import running_as_notebook
from manipulation.meshcat_utils import (AddMeshcatTriad,
                                            draw_open3d_point_cloud)
from manipulation.mustard_depth_camera_example import MustardPointCloud
from manipulation.open3d_utils import create_open3d_point_cloud
from manipulation.scenarios import (AddMultibodyTriad, AddRgbdSensor,
                                    MakeManipulationStation)
from manipulation.utils import AddPackagePaths, FindResource

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
    station = ManipulationStation()
    station.SetupManipulationClassStation()
    # station.SetupClutterClearingStation()
    station.Finalize()
    context = station.CreateDefaultContext()

    camera_names = station.get_camera_names()
    index = 1
    for name in camera_names:
        color_image = station.GetOutputPort("camera_" + name +
                                            "_rgb_image").Eval(context)
        depth_image = station.GetOutputPort("camera_" + name +
                                            "_depth_image").Eval(context)

        plt.subplot(len(camera_names), 2, index)
        plt.imshow(color_image.data)
        index += 1
        plt.title('Color image')
        plt.subplot(len(camera_names), 2, index)
        plt.imshow(np.squeeze(depth_image.data))
        index += 1
        plt.title('Depth image')

    plt.show()

plot_manipulation_station_camera_images()    


# # Point cloud registration with known correspondences

# In[ ]:


def MakeRandomObjectModelAndScenePoints(
    num_model_points=20, 
    noise_std=0, 
    num_outliers=0, 
    yaw_O=None,
    p_O=None, 
    num_viewable_points=None, 
    seed=None):
    """ Returns p_Om, p_s """
    random_state = np.random.RandomState(seed)

    # Make a random set of points to define our object in the x,y plane
    theta = np.arange(0, 2.0*np.pi, 2.0*np.pi/num_model_points)
    l = 1.0 + 0.5*np.sin(2.0*theta) + 0.4*random_state.rand(1, num_model_points)
    p_Om = np.vstack((l * np.sin(theta), l * np.cos(theta), 0 * l))

    # Make a random object pose if one is not specified, and apply it to get the scene points.
    if p_O is None:
        p_O = [2.0*random_state.rand(), 2.0*random_state.rand(), 0.0]
    if len(p_O) == 2:
        p_O.append(0.0)
    if yaw_O is None:
        yaw_O = 0.5*random_state.random()
    X_O = RigidTransform(RotationMatrix.MakeZRotation(yaw_O), p_O)
    if num_viewable_points is None:
        num_viewable_points = num_model_points
    assert num_viewable_points <= num_model_points
    p_s = X_O.multiply(p_Om[:,:num_viewable_points])
    p_s[:2, :]  += random_state.normal(scale=noise_std, size=(2, num_viewable_points))
    if num_outliers:
        outliers = random_state.uniform(low=-1.5, high=3.5, size=(3, num_outliers))
        outliers[2,:] = 0
        p_s = np.hstack((p_s, outliers))

    return p_Om, p_s, X_O

def MakeRectangleModelAndScenePoints(
    num_points_per_side=7,
    noise_std=0, 
    num_outliers=0, 
    yaw_O=None,
    p_O=None, 
    num_viewable_points=None, 
    seed=None):
    random_state = np.random.RandomState(seed)
    if p_O is None:
        p_O = [2.0*random_state.rand(), 2.0*random_state.rand(), 0.0]
    if len(p_O) == 2:
        p_O.append(0.0)
    if yaw_O is None:
        yaw_O = 0.5*random_state.random()
    X_O = RigidTransform(RotationMatrix.MakeZRotation(yaw_O), p_O)
    if num_viewable_points is None:
        num_viewable_points = 4*num_points_per_side
    
    x = np.arange(-1, 1, 2/num_points_per_side)
    half_width = 2
    half_height = 1
    top = np.vstack((half_width*x, half_height + 0*x))
    right = np.vstack((half_width + 0*x, -half_height*x))
    bottom = np.vstack((-half_width*x, -half_height + 0*x))
    left = np.vstack((-half_width + 0*x, half_height*x))
    p_Om = np.vstack((np.hstack((top, right, bottom, left)), np.zeros((1, 4*num_points_per_side))))
    p_s = X_O.multiply(p_Om[:,:num_viewable_points])
    p_s[:2, :]  += random_state.normal(scale=noise_std, size=(2, num_viewable_points))
    if num_outliers:
        outliers = random_state.uniform(low=-1.5, high=3.5, size=(3, num_outliers))
        outliers[2,:] = 0
        p_s = np.hstack((p_s, outliers))

    return p_Om, p_s, X_O


def PlotEstimate(p_Om, p_s, Xhat_O=RigidTransform(), chat=None, X_O=None, ax=None):
    p_m = Xhat_O.multiply(p_Om)
    if ax is None:
        ax = plt.subplot()
    Nm = p_Om.shape[1]
    artists = ax.plot(p_m[0, :], p_m[1, :], 'bo')
    artists += ax.fill(p_m[0, :], p_m[1, :], 'lightblue', alpha=0.5)
    artists += ax.plot(p_s[0, :], p_s[1, :], 'ro')
    if chat is not None:
        artists += ax.plot(np.vstack((p_m[0, chat], p_s[0, :])), np.vstack((p_m[1, chat], p_s[1, :])), 'g--')
    if X_O:
        p_s = X_O.multiply(p_Om)
    artists += ax.fill(p_s[0, :Nm], p_s[1, :Nm], 'lightsalmon')
    ax.axis('equal')
    return artists

def PrintResults(X_O, Xhat_O):
    p = X_O.translation()
    aa = X_O.rotation().ToAngleAxis()
    print(f"True position: {p}")
    print(f"True orientation: {aa}")
    p = Xhat_O.translation()
    aa = Xhat_O.rotation().ToAngleAxis()
    print(f"Estimated position: {p}")
    print(f"Estimated orientation: {aa}")

def PoseEstimationGivenCorrespondences(p_Om, p_s, chat):
    """ Returns optimal X_O given the correspondences """
    # Apply correspondences, and transpose data to support numpy broadcasting
    p_Omc = p_Om[:, chat].T
    p_s = p_s.T

    # Calculate the central points
    p_Ombar = p_Omc.mean(axis=0)
    p_sbar = p_s.mean(axis=0)

    # Calculate the "error" terms, and form the data matrix
    merr = p_Omc - p_Ombar
    serr = p_s - p_sbar
    W = np.matmul(serr.T, merr)

    # Compute R
    U, Sigma, Vt = np.linalg.svd(W)
    R = np.matmul(U, Vt)
    if np.linalg.det(R) < 0:
       print("fixing improper rotation")
       Vt[-1, :] *= -1
       R = np.matmul(U, Vt)

    # Compute p
    p = p_sbar - np.matmul(R, p_Ombar)

    return RigidTransform(RotationMatrix(R), p)


p_Om, p_s, X_O = MakeRandomObjectModelAndScenePoints(num_model_points=20)
#p_Om, p_s, X_O = MakeRectangleModelAndScenePoints()
Xhat = RigidTransform()
c = range(p_Om.shape[1])  # perfect, known correspondences
fig, ax = plt.subplots(1, 2)
PlotEstimate(p_Om, p_s, Xhat, c, ax=ax[0])
Xhat = PoseEstimationGivenCorrespondences(p_Om, p_s, c)
ax[1].set_xlim(ax[0].get_xlim())
ax[1].set_ylim(ax[0].get_ylim());
PlotEstimate(p_Om, p_s, Xhat, c, ax=ax[1])
ax[0].set_title('Original Data')
ax[1].set_title('After Registration')
PrintResults(X_O, Xhat)


# # Iterative Closest Point (ICP)

# In[ ]:


def FindClosestPoints(point_cloud_A, point_cloud_B):
    """
    Finds the nearest (Euclidean) neighbor in point_cloud_B for each
    point in point_cloud_A.
    @param point_cloud_A A 3xN numpy array of points.
    @param point_cloud_B A 3xN numpy array of points.
    @return indices An (N, ) numpy array of the indices in point_cloud_B of each
        point_cloud_A point's nearest neighbor.
    """
    indices = np.empty(point_cloud_A.shape[1], dtype=int)

    # TODO(russt): Replace this with a direct call to flann
    # https://pypi.org/project/flann/
    kdtree = o3d.geometry.KDTreeFlann(point_cloud_B)
    for i in range(point_cloud_A.shape[1]):
        nn = kdtree.search_knn_vector_3d(point_cloud_A[:,i], 1)
        indices[i] = nn[1][0]

    return indices


def IterativeClosestPoint(p_Om,
                          p_s,
                          X_O=None,
                          animate=True,
                          meshcat_scene_path=None):
    Xhat = RigidTransform()
    Nm = p_s.shape[1]
    chat_previous = np.zeros(Nm)-1 # Set chat to a value that FindClosePoints will never return.

    if animate:
        fig, ax = plt.subplots()
        frames = []
        frames.append(PlotEstimate(p_Om=p_Om, p_s=p_s, Xhat_O=Xhat, chat=None, X_O=X_O, ax=ax))

    while True:
        chat = FindClosestPoints(p_s, Xhat.multiply(p_Om))
        if np.array_equal(chat, chat_previous):
            # Then I've converged.
            break
        chat_previous = chat
        if animate:
            frames.append(PlotEstimate(p_Om=p_Om, p_s=p_s, Xhat_O=Xhat, chat=chat, X_O=X_O, ax=ax))
        Xhat = PoseEstimationGivenCorrespondences(p_Om, p_s, chat)
        if animate:
            frames.append(PlotEstimate(p_Om=p_Om, p_s=p_s, Xhat_O=Xhat, chat=None, X_O=X_O, ax=ax))
        if meshcat_scene_path:
            meshcat.SetTransform(meshcat_scene_path, Xhat.inverse())

    if animate:
        ani = animation.ArtistAnimation(fig, frames, interval=400, repeat=False)

        display(HTML(ani.to_jshtml()))
        plt.close()

    if X_O:
        PrintResults(X_O, Xhat)

    return Xhat, chat


p_Om, p_s, X_O = MakeRandomObjectModelAndScenePoints(num_model_points=20)
IterativeClosestPoint(p_Om, p_s, X_O);


# Try increasing the standard deviation on yaw in the example above.  At some point, the performance can get pretty poor!
# 
# # ICP with messy point clouds
# 
# Try changing the amount of noise, the number of outliers, and/or the partial views.  There are not particularly good theorems here, but I hope that a little bit of play will get you a lot of intuition.

# In[ ]:


#p_Om, p_s, X_O = MakeRandomObjectModelAndScenePoints(
p_Om, p_s, X_O = MakeRectangleModelAndScenePoints(
    yaw_O=0.1,
#    noise_std=0.2,
#    num_outliers=3,
    num_viewable_points=14)
IterativeClosestPoint(p_Om, p_s, X_O);


# # Non-penetration constraints with nonlinear optimization

# In[ ]:


from pydrake.all import Solve
from functools import partial

def ConstrainedKnownCorrespondenceNonlinearOptimization(p_Om, p_s, chat):
    """ This version adds a non-penetration constraint (x,y >= 0) """

    p_Omc = p_Om[:2, chat]
    p_s = p_s[:2, :]
    Ns = p_s.shape[1]

    prog = MathematicalProgram()
    p = prog.NewContinuousVariables(2, 'p')
    theta = prog.NewContinuousVariables(1, 'theta')

    def position_model_in_world(vars, i):
        [p, theta] = np.split(vars, [2])
        R = np.array([[np.cos(theta[0]), -np.sin(theta[0])],
                      [np.sin(theta[0]), np.cos(theta[0])]])
        p_Wmci = p + R @ p_Omc[:,i]
        return p_Wmci

    def squared_distance(vars, i):
        p_Wmci = position_model_in_world(vars, i)
        err = p_Wmci - p_s[:,i]
        return err.dot(err)

    for i in range(Ns):
        prog.AddCost(partial(squared_distance, i=i),
                     np.concatenate([p[:], theta]))
        # forall i, p + R*mi >= 0.  
        prog.AddConstraint(partial(position_model_in_world, i=i), 
                           vars=np.concatenate([p[:], theta]),
                           lb=[0, 0], ub=[np.inf, np.inf])
    
    result = Solve(prog)
    
    theta_sol = result.GetSolution(theta[0])
    Rsol = np.array([[np.cos(theta_sol), -np.sin(theta_sol), 0],
                     [np.sin(theta_sol), np.cos(theta_sol), 0], 
                     [0, 0, 1]])
    psol = np.zeros(3)
    psol[:2] = result.GetSolution(p)

    return RigidTransform(RotationMatrix(Rsol), psol)

p_Om, p_s, X_O = MakeRectangleModelAndScenePoints(
    yaw_O=0.2,
    p_O = [1.5, 1.2],
)
c = range(p_Om.shape[1])  # perfect, known correspondences
Xhat_O = ConstrainedKnownCorrespondenceNonlinearOptimization(p_Om, p_s, c)
PlotEstimate(p_Om=p_Om, p_s=p_s, Xhat_O=Xhat_O, chat=c, X_O=X_O)
PrintResults(X_O, Xhat_O)
plt.gca().plot([0,0], [0, 2.5], 'g-', linewidth=3)
plt.gca().plot([0,4], [0, 0], 'g-', linewidth=3);


# # Non-penetration (half-plane) constraints with convex optimization

# In[ ]:


def ConstrainedKnownCorrespondenceConvexRelaxation(p_Om, p_s, chat):
    """ This version adds a non-penetration constraint (x,y >= 0) """

    p_Omc = p_Om[:2, chat]
    p_s = p_s[:2, :]
    Ns = p_s.shape[1]

    prog = MathematicalProgram()
    [a,b] = prog.NewContinuousVariables(2)
    # We use the slack variable as an upper bound on the cost of each point to make the objective linear.
    slack = prog.NewContinuousVariables(Ns)
    p = prog.NewContinuousVariables(2)
    prog.AddBoundingBoxConstraint(0,1,[a,b])  # This makes Csdp happier
    R = np.array([[a, -b],[b, a]])
    prog.AddLorentzConeConstraint([1.0, a, b])

    # Note: Could do this more efficiently, exploiting trace.  But I'm keeping it simpler here.
    prog.AddCost(np.sum(slack))
    for i in range(Ns):
        c = p + np.matmul(R,p_Omc[:,i]) - p_s[:,i]
        # forall i, slack[i]^2 >= |c|^2 
        prog.AddLorentzConeConstraint([slack[i], c[0], c[1]])
        # forall i, p + R*mi >= 0.  
        prog.AddConstraint(ge(p + np.matmul(R, p_Omc[:,i]), [0, 0]))
    
    result = CsdpSolver().Solve(prog)
    
    [a,b] = result.GetSolution([a,b])
    Rsol = np.array([[a, -b, 0],[b, a, 0], [0,0,1]])
    psol = np.zeros(3)
    psol[:2] = result.GetSolution(p)

    return RigidTransform(RotationMatrix(Rsol), psol)

p_Om, p_s, X_O = MakeRectangleModelAndScenePoints(
    yaw_O=0.2,
    p_O = [1.5, 1.2],
)
c = range(p_Om.shape[1])  # perfect, known correspondences
Xhat_O = ConstrainedKnownCorrespondenceConvexRelaxation(p_Om, p_s, c)
PlotEstimate(p_Om=p_Om, p_s=p_s, Xhat_O=Xhat_O, chat=c, X_O=X_O)
PrintResults(X_O, Xhat_O)
plt.gca().plot([0,0], [0, 2.5], 'g-', linewidth=3)
plt.gca().plot([0,4], [0, 0], 'g-', linewidth=3);


# In[ ]:


meshcat.Delete()


# # Putting it all together
# 
# In the code above, we worked with a point cloud using functions.  To assemble this into a full-stack manipulation system, we need to specify the timing semantics of when those functions are called.  That's precisely what Drake's systems framework provides.  I've introduced two systems below: 
# - `MustardIterativeClosestPoint` system that takes the camera inputs and outputs the pose estimate using ICP, and 
# - `PickAndPlaceTrajectory` system that takes this pose estimate (and the state of the robot), computes the trajectory, and stores that trajectory in its Context so that it can output the instantaneous command.  
# 
# We don't use a `TrajectorySource` here, because the trajectory is not known when we first build the Diagram... the information we need to plan the trajectory requires reading sensors at runtime.

# In[ ]:


model_directives = """
directives:
- add_directives:
    file: package://manipulation/clutter_w_cameras.dmd.yaml
- add_model:
    name: mustard
    file: package://drake/manipulation/models/ycb/sdf/006_mustard_bottle.sdf
    default_free_body_pose:
        base_link_mustard:
            translation: [.55, 0.1, 0.09515]
            rotation: !Rpy { deg: [-90, 0, 45] }
"""

# Takes 3 point clouds (in world coordinates) as input, and outputs and estimated pose for the mustard bottle.
class MustardIterativeClosestPoint(LeafSystem):
    def __init__(self):
        LeafSystem.__init__(self)
        model_point_cloud = AbstractValue.Make(PointCloud(0))
        self.DeclareAbstractInputPort("cloud0", model_point_cloud)
        self.DeclareAbstractInputPort("cloud1", model_point_cloud)
        self.DeclareAbstractInputPort("cloud2", model_point_cloud)

        self.DeclareAbstractOutputPort(
            "X_WO", lambda: AbstractValue.Make(RigidTransform()),
            self.EstimatePose)

        self.mustard = MustardPointCloud()
        meshcat.SetObject("icp_scene", self.mustard)

    def EstimatePose(self, context, output):
        # Note: The point cloud processing we do here will be described in more detail in the next chapter.
        pcd = []
        for i in range(3):
            point_cloud = self.get_input_port(i).Eval(context)
            cloud = create_open3d_point_cloud(point_cloud)
            # Crop to region of interest.
            pcd.append(cloud.crop(
                o3d.geometry.AxisAlignedBoundingBox(min_bound=[.4, -.2, 0.001],
                                                    max_bound=[.6, .3, .3])))
        # Merge point clouds.
        merged_pcd = pcd[0] + pcd[1] + pcd[2]
        # Down-sample.
        down_sampled_pcd = merged_pcd.voxel_down_sample(voxel_size=0.005)
        draw_open3d_point_cloud(meshcat, "icp_observations", down_sampled_pcd)

        X_ModelScene, chat = IterativeClosestPoint(
            np.asarray(down_sampled_pcd.points).T,
            self.mustard.xyzs(),
            animate=False,
            meshcat_scene_path="icp_scene")

        output.set_value(X_ModelScene.inverse())

class PickAndPlaceTrajectory(LeafSystem):
    def __init__(self, plant):
        LeafSystem.__init__(self)
        self._gripper_body_index = plant.GetBodyByName("body").index()
        self.DeclareAbstractInputPort(
            "body_poses", AbstractValue.Make([RigidTransform()]))
        #            plant.get_body_poses_output_port().Allocate())
        self.DeclareAbstractInputPort("X_WO",
                                      AbstractValue.Make(RigidTransform()))

        self.DeclareInitializationUnrestrictedUpdateEvent(self.Plan)
        self._X_G_traj_index = self.DeclareAbstractState(
            AbstractValue.Make(PiecewisePose()))
        self._wsg_traj_index = self.DeclareAbstractState(
            AbstractValue.Make(PiecewisePolynomial()))

        self.DeclareAbstractOutputPort(
            "X_WG", lambda: AbstractValue.Make(RigidTransform()),
            self.CalcGripperPose)
        self.DeclareVectorOutputPort("wsg_position", 1, self.CalcWsgPosition)

    def Plan(self, context, state):
        X_Ginitial = self.get_input_port(0).Eval(context)[
            int(self._gripper_body_index)]
        X_Oinitial = self.get_input_port(1).Eval(context)
        X_Ogoal = RigidTransform([0, -.6, 0])
        X_GgraspO = RigidTransform(RollPitchYaw(np.pi / 2, 0, 0),
                                   [0, 0.22, 0])
        X_GgraspGpregrasp = RigidTransform([0, -0.08, 0])
        X_OGgrasp = X_GgraspO.inverse()

        X_Gpick = X_Oinitial @ X_OGgrasp
        X_Gprepick = X_Gpick @ X_GgraspGpregrasp
        X_Gplace = X_Ogoal @ X_OGgrasp
        X_Gpreplace = X_Gplace @ X_GgraspGpregrasp

        # I'll interpolate a halfway orientation by converting to axis angle
        # and halving the angle.
        X_GprepickGpreplace = X_Gprepick.inverse() @ X_Gpreplace
        angle_axis = X_GprepickGpreplace.rotation().ToAngleAxis()
        X_GprepickGclearance = RigidTransform(
            AngleAxis(angle=angle_axis.angle()/2.0, axis=angle_axis.axis()),
            X_GprepickGpreplace.translation()/2.0 + np.array([0, -0.3, 0]))
        X_Gclearance = X_Gprepick @ X_GprepickGclearance

        if False:  # Useful for debugging
            AddMeshcatTriad(meshcat, "X_Oinitial", X_PT=X_Oinitial)
            AddMeshcatTriad(meshcat, "X_Gprepick", X_PT=X_Gprepick)
            AddMeshcatTriad(meshcat, "X_Gpick", X_PT=X_Gpick)
            AddMeshcatTriad(meshcat, "X_Gplace", X_PT=X_Gplace)

        # Construct the trajectory.  This is a condensed version of the logic
        # from the previous chapter, adapted to the mustard bottle.
        times = [0]
        poses = [X_Ginitial]
        def add_pose_segment(duration, X_G):
            times.append(times[-1] + duration)
            poses.append(X_G)
        wsg_times = []
        wsg_commands = []
        def wsg_opened():
            wsg_times.append(times[-1])
            wsg_commands.append([0.107])
        def wsg_closed():
            wsg_times.append(times[-1])
            wsg_commands.append([0])

        wsg_opened()
        add_pose_segment(
            10.0 * np.linalg.norm(X_Gprepick.translation() - X_Ginitial.translation()), X_Gprepick)
        add_pose_segment(2, X_Gpick)
        wsg_opened()
        add_pose_segment(2, X_Gpick)  # while the gripper closes
        wsg_closed()
        add_pose_segment(2, X_Gprepick)
        time_to_from_clearance = 10.0*np.linalg.norm(X_GprepickGclearance.translation())
        add_pose_segment(time_to_from_clearance, X_Gclearance)
        add_pose_segment(time_to_from_clearance, X_Gpreplace)
        add_pose_segment(2, X_Gplace)
        wsg_closed()
        add_pose_segment(2, X_Gplace)  # while the gripper opens
        wsg_opened()
        add_pose_segment(2, X_Gpreplace)
        wsg_opened()

        X_G_traj = PiecewisePose.MakeLinear(times, poses)
        state.get_mutable_abstract_state(int(self._X_G_traj_index)).set_value(
            X_G_traj)
        state.get_mutable_abstract_state(int(self._wsg_traj_index)).set_value(
            PiecewisePolynomial.FirstOrderHold(
                wsg_times,
                np.asarray(wsg_commands).reshape(1, -1)))
        print(X_G_traj.end_time())
        return EventStatus.Succeeded()

    def start_time(self, context):
        return context.get_abstract_state(
            int(self._X_G_traj_index)).get_value().start_time()

    def end_time(self, context):
        return context.get_abstract_state(
            int(self._X_G_traj_index)).get_value().end_time()

    def CalcGripperPose(self, context, output):
        # Evaluate the trajectory at the current time, and write it to the
        # output port.
        output.set_value(context.get_abstract_state(int(
            self._X_G_traj_index)).get_value().GetPose(context.get_time()))

    def CalcWsgPosition(self, context, output):
        # Evaluate the trajectory at the current time, and write it to the
        # output port.
        output.SetFromVector(
            context.get_abstract_state(int(
                self._wsg_traj_index)).get_value().value(context.get_time()))


def icp_pick_and_place_demo():
    builder = DiagramBuilder()

    station = builder.AddSystem(
        MakeManipulationStation(model_directives, time_step=0.002))
    plant = station.GetSubsystemByName("plant")

    icp = builder.AddSystem(MustardIterativeClosestPoint())
    builder.Connect(station.GetOutputPort("camera3_point_cloud"),
                    icp.get_input_port(0))
    builder.Connect(station.GetOutputPort("camera4_point_cloud"),
                    icp.get_input_port(1))
    builder.Connect(station.GetOutputPort("camera5_point_cloud"),
                    icp.get_input_port(2))

    plan = builder.AddSystem(PickAndPlaceTrajectory(plant))
    builder.Connect(station.GetOutputPort("body_poses"),
                    plan.GetInputPort("body_poses"))
    builder.Connect(icp.GetOutputPort("X_WO"), plan.GetInputPort("X_WO"))

    robot = station.GetSubsystemByName(
        "iiwa_controller").get_multibody_plant_for_control()
    diff_ik_params = DifferentialInverseKinematicsParameters(
        robot.num_positions(), robot.num_velocities())

    time_step = 0.005
    diff_ik_params.set_timestep(time_step)
    iiwa14_velocity_limits = np.array([1.4, 1.4, 1.7, 1.3, 2.2, 2.3, 2.3])
    diff_ik_params.set_joint_velocity_limits((-iiwa14_velocity_limits,
                                    iiwa14_velocity_limits))
    diff_ik_params.set_end_effector_velocity_gain([.1]*6)
    diff_ik = builder.AddSystem(
        DifferentialInverseKinematicsIntegrator(
            robot, robot.GetFrameByName("body"), time_step,
            diff_ik_params))
    builder.Connect(diff_ik.get_output_port(),
                    station.GetInputPort("iiwa_position"))
    builder.Connect(plan.GetOutputPort("X_WG"),
                    diff_ik.get_input_port())

    builder.Connect(plan.GetOutputPort("wsg_position"),
                    station.GetInputPort("wsg_position"))

    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, station.GetOutputPort("query_object"), meshcat)
    diagram = builder.Build()

    simulator = Simulator(diagram)
    context = simulator.get_context()
    plant_context = plant.GetMyContextFromRoot(context)
    diff_ik_context = diff_ik.GetMyMutableContextFromRoot(context)

    q0 = plant.GetPositions(plant_context, plant.GetModelInstanceByName("iiwa"))
    diff_ik.get_mutable_parameters().set_nominal_joint_position(q0)
    diff_ik.SetPositions(diff_ik_context, q0)

    simulator.Initialize()
    if False: # draw the trajectory triads
        X_G_traj = plan.GetMyContextFromRoot(context).get_abstract_state(
            0).get_value()
        for t in np.linspace(X_G_traj.start_time(), X_G_traj.end_time(), 40):
            AddMeshcatTriad(meshcat,
                            f"X_G/({t})",
                            X_PT=X_G_traj.GetPose(t),
                            length=.1,
                            radius=0.004)

    if running_as_notebook:
        meshcat.Flush()
        visualizer.StartRecording()
        simulator.AdvanceTo(plan.end_time(plan.GetMyContextFromRoot(context)))
        visualizer.PublishRecording()
    else:
        simulator.AdvanceTo(0.1)

icp_pick_and_place_demo()


# In[ ]:




