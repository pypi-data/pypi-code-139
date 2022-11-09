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


# Imports
import os
import sys
import time
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML, clear_output, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, Box,
                         Capsule, ConnectPlanarSceneGraphVisualizer,
                         ContactResults, ContactVisualizer,
                         ContactVisualizerParams, CoulombFriction, Cylinder,
                         DiagramBuilder, DrakeVisualizer, Ellipsoid,
                         EventStatus, FindResourceOrThrow, FixedOffsetFrame,
                         JointIndex, JointSliders, LeafSystem,
                         LoadModelDirectives, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, PlanarJoint,
                         PointCloud, ProcessModelDirectives, RandomGenerator,
                         Rgba, RigidTransform, RollPitchYaw, RotationMatrix,
                         Simulator, SpatialInertia, Sphere, StartMeshcat,
                         UniformlyRandomRotationMatrix, UnitInertia)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import AddMeshcatTriad, draw_open3d_point_cloud
from manipulation.scenarios import (AddFloatingRpyJoint, AddRgbdSensor,
                                    AddRgbdSensors)
from manipulation.utils import AddPackagePaths, FindResource

ycb = [("cracker", "003_cracker_box.sdf"),
        ("sugar", "004_sugar_box.sdf"),
        ("soup", "005_tomato_soup_can.sdf"),
        ("mustard", "006_mustard_bottle.sdf"),
        ("gelatin", "009_gelatin_box.sdf"),
        ("meat", "010_potted_meat_can.sdf")]


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Falling things (in 2D)
# 

# In[ ]:


def clutter_gen():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)

    box = Box(10., 10., 10.)
    X_WBox = RigidTransform([0, 0, -5])
    mu = 1.0
    plant.RegisterCollisionGeometry(plant.world_body(), X_WBox, box, "ground", CoulombFriction(mu, mu))
    plant.RegisterVisualGeometry(plant.world_body(), X_WBox, box, "ground", [.9, .9, .9, 1.0])
    planar_joint_frame = plant.AddFrame(FixedOffsetFrame("planar_joint_frame", plant.world_frame(), RigidTransform(RotationMatrix.MakeXRotation(np.pi/2))))

    parser = Parser(plant)

    sdf = FindResourceOrThrow("drake/examples/manipulation_station/models/061_foam_brick.sdf")

    for i in range(20 if running_as_notebook else 2):
        instance = parser.AddModelFromFile(sdf, f"object{i}")
        plant.AddJoint(PlanarJoint(f"joint{i}", planar_joint_frame, plant.GetFrameByName("base_link", instance), damping=[0,0,0]))

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

# In[ ]:


def clutter_gen():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0005)

    parser = Parser(plant)

    parser.AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/bin.sdf"))
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("bin_base"))


    rs = np.random.RandomState()  # this is for python
    generator = RandomGenerator(rs.randint(1000))  # this is for c++
    for i in range(10 if running_as_notebook else 2):
        object_num = rs.randint(len(ycb))
        sdf = FindResourceOrThrow("drake/manipulation/models/ycb/sdf/" + ycb[object_num][1])
        parser.AddModelFromFile(sdf, f"object{i}")

    plant.Finalize()

    camera = AddRgbdSensor(builder, scene_graph, RigidTransform(
        RollPitchYaw(np.pi, 0, np.pi / 2.0), [0, 0, .8]))
    builder.ExportOutput(camera.color_image_output_port(), "color_image")

    # Note: if you're running this on a local machine, then you can 
    # use drake_visualizer to see the simulation.  (It's too slow to 
    # show the meshes on meshcat).
    vis = DrakeVisualizer.AddToBuilder(
        builder, 
        scene_graph
    )

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


# # Contact force "inspector"
# 

# In[ ]:


class PrintContactResults(LeafSystem):
    def __init__(self):
        LeafSystem.__init__(self)
        self.DeclareAbstractInputPort("contact_results",
                                      AbstractValue.Make(ContactResults()))
        self.DeclareForcedPublishEvent(self.Publish)

    def Publish(self, context):
        formatter = {'float': lambda x: '{:5.2f}'.format(x)}
        results = self.get_input_port().Eval(context)

        clear_output(wait=True)
        if results.num_point_pair_contacts()==0:
            print("no contact")
        for i in range(results.num_point_pair_contacts()):
            info = results.point_pair_contact_info(i)
            pair = info.point_pair()
            force_string = np.array2string(
                info.contact_force(), formatter=formatter)
            print(
              f"slip speed:{info.slip_speed():.4f}, "
              f"depth:{pair.depth:.4f}, "
              f"force:{force_string}\n")
        return EventStatus.Succeeded()

def contact_force_inspector(slope=0.0, mu=1.0, second_brick=False):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.01)

    box = Box(10., 10., 10.)
    X_WBox = RigidTransform(RotationMatrix.MakeYRotation(slope), [0, 0, -5.05])
    plant.RegisterCollisionGeometry(plant.world_body(), X_WBox, box, "ground",
                                    CoulombFriction(mu, mu))
    plant.RegisterVisualGeometry(plant.world_body(), X_WBox, box, "ground",
                                 [.9, .9, .9, 1.0])

    parser = Parser(plant)
    brick_sdf = FindResource("models/planar_foam_brick_collision_as_visual.sdf")
    parser.AddModelFromFile(brick_sdf)
    frame = plant.AddFrame(
        FixedOffsetFrame(
            "planar_joint_frame", plant.world_frame(),
            RigidTransform(RotationMatrix.MakeXRotation(np.pi / 2))))
    plant.AddJoint(
        PlanarJoint("brick",
                    frame,
                    plant.GetFrameByName("base_link"),
                    damping=[0, 0, 0]))

    if second_brick:
        brick2 = parser.AddModelFromFile(brick_sdf, "brick2")
        plant.AddJoint(
            PlanarJoint("brick2",
                        frame,
                        plant.GetFrameByName("base_link", brick2),
                        damping=[0, 0, 0]))

    plant.Finalize()

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)
    meshcat.Set2dRenderMode(xmin=-.2, xmax=.2, ymin=-.2, ymax=0.3)

    cparams = ContactVisualizerParams()
    cparams.force_threshold = 1e-6
    cparams.newtons_per_meter = 1.0
    cparams.radius = 0.002
    contact_visualizer = ContactVisualizer.AddToBuilder(builder, plant, meshcat,
                                                        cparams)

    print_contact_results = builder.AddSystem(PrintContactResults())
    builder.Connect(plant.get_contact_results_output_port(),
                    print_contact_results.get_input_port())

    lower_limit = [-0.1, -0.1, -np.pi/2.0]
    upper_limit = [0.1, 0.1, np.pi/2.0]
    q0 = [0, 0, 0]
    if second_brick:
        lower_limit += lower_limit
        upper_limit += upper_limit
        q0 += [0.07, 0.07, 0.0]

    default_interactive_timeout = None if running_as_notebook else 1.0
    sliders = builder.AddSystem(
        JointSliders(meshcat,
                     plant,
                     initial_value=q0,
                     lower_limit=lower_limit,
                     upper_limit=upper_limit,
                     step=0.001))
    diagram = builder.Build()
    sliders.Run(diagram, default_interactive_timeout)
    meshcat.DeleteAddedControls()

contact_force_inspector(
    slope=0.1,
    mu=0.5,
    second_brick=True);


# # Contact results "inspector"
# 
# This simple visualization shows some of the complexity of the contact geometry problem.  I will make it better, but right now, when you move the objects into contact of each other you will see three points:  the contact point is in **red**, the contact normal is added to the contact point with the tip as **green**, and the (scaled) contact force tip is drawn in **blue**.  Contact points on the bodies are drawn in **orange**.

# In[ ]:


class PrintContactResults(LeafSystem):
    def __init__(self):
        LeafSystem.__init__(self)
        self.DeclareAbstractInputPort("contact_results",
                                      AbstractValue.Make(ContactResults()))
        self.DeclareForcedPublishEvent(self.Publish)

    def Publish(self, context):
        results = self.get_input_port().Eval(context)
        meshcat.Delete("contact")

        red = Rgba(1, 0, 0, 1)
        green = Rgba(0, 1, 0, 1)
        blue = Rgba(0, 0, 1, 1)
        orange = Rgba(1, .65, 0, 1)

        clear_output(wait=True)
        if results.num_point_pair_contacts()==0:
            print("no contact")
        for i in range(results.num_point_pair_contacts()):
            info = results.point_pair_contact_info(i)
            pair = info.point_pair()
            meshcat.SetObject(f"contact/{i}", Sphere(0.02), red)
            meshcat.SetTransform(
                f"contact/{i}", RigidTransform(info.contact_point()))
            meshcat.SetObject(f"contact/{i}A", Sphere(0.01), orange)
            meshcat.SetTransform(
                f"contact/{i}A", RigidTransform(pair.p_WCa))
            meshcat.SetObject(f"contact/{i}B", Sphere(0.01), orange)
            meshcat.SetTransform(
                f"contact/{i}B", RigidTransform(pair.p_WCb))
            meshcat.SetObject(f"contact/{i}normal", Sphere(0.02), green)
            meshcat.SetTransform(
                f"contact/{i}normal", RigidTransform(
                    info.contact_point() - pair.nhat_BA_W))
            meshcat.SetObject(f"contact/{i}force", Sphere(0.02), blue)
            meshcat.SetTransform(
                f"contact/{i}force", RigidTransform(
                    info.contact_point()+info.contact_force()/5000.0))

            formatter = {'float': lambda x: '{:5.2f}'.format(x)}
            point_string = np.array2string(
                info.contact_point(), formatter=formatter)
            normal_string = np.array2string(
                -pair.nhat_BA_W, formatter=formatter)
            force_string = np.array2string(
                info.contact_force(), formatter=formatter)
            print(
              f"slip speed:{info.slip_speed():.4f}, "
              f"separation speed:{info.separation_speed():.4f}, "
              f"depth:{pair.depth:.4f},\n"
              f"point:{point_string},\n"
              f"normal:{normal_string},\n"
              f"force:{force_string}\n"
            )

        return EventStatus.Succeeded()

shapes = {
  "Point": Sphere(0.01),
  "Sphere": Sphere(1.0),
  "Cylinder": Cylinder(1.0, 2.0),
  "Box": Box(1.0, 2.0, 3.0),
  "Capsule": Capsule(1.0, 2.0),
  "Ellipsoid": Ellipsoid(1.0, 2.0, 3.0),
}

def contact_inspector(shape_name_A, shape_name_B):
    builder = DiagramBuilder()

    shapeA = shapes[shape_name_A]
    shapeB = shapes[shape_name_B]

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0)
    frame = plant.AddFrame(FixedOffsetFrame("planar_joint_frame", plant.world_frame(), RigidTransform(RotationMatrix.MakeXRotation(np.pi/2))))

    mu = 0.5
    bodyA = plant.AddRigidBody("A", SpatialInertia(mass=1.0, p_PScm_E=np.array([0., 0., 0.]),
            G_SP_E=UnitInertia(1.0, 1.0, 1.0)))
    plant.RegisterCollisionGeometry(bodyA, RigidTransform(), shapeA, "A", CoulombFriction(mu, mu))
    plant.RegisterVisualGeometry(bodyA, RigidTransform(), shapeA, "A", [.9, .5, .5, 0.5])
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("A"))

    bodyB = plant.AddRigidBody("B", SpatialInertia(mass=1.0, p_PScm_E=np.array([0., 0., 0.]),
            G_SP_E=UnitInertia(1.0, 1.0, 1.0)))
    plant.RegisterCollisionGeometry(bodyB, RigidTransform(), shapeB, "B", CoulombFriction(mu, mu))
    plant.RegisterVisualGeometry(bodyB, RigidTransform(), shapeB, "B", [.5, .5, .9, 0.9])
    plant.AddJoint(PlanarJoint("B", frame, plant.GetFrameByName("B"), damping=[0,0,0]))

    plant.Finalize()

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)
    meshcat.Set2dRenderMode(xmin=-3.0, xmax=3.0, ymin=-.2, ymax=3.0)

    #    cparams = ContactVisualizerParams()
    #    cparams.force_threshold = 1e-6
    #    cparams.newtons_per_meter = 1.0
    #    cparams.radius = 0.002
    #    contact_visualizer = ContactVisualizer.AddToBuilder(
    #        builder, plant, meshcat, cparams)

    print_contact_results = builder.AddSystem(PrintContactResults())
    builder.Connect(plant.get_contact_results_output_port(),
                    print_contact_results.get_input_port())

    lower_limit = [-3, -3, -np.pi/2.0]
    upper_limit = [3, 3, np.pi/2.0]
    q0 = [1.2, 1.2, 0.0]

    default_interactive_timeout = None if running_as_notebook else 1.0
    sliders = builder.AddSystem(
        JointSliders(meshcat,
                     plant,
                     initial_value=q0,
                     lower_limit=lower_limit,
                     upper_limit=upper_limit))
    diagram = builder.Build()
    sliders.Run(diagram, default_interactive_timeout)
    meshcat.DeleteAddedControls()

contact_inspector("Box", "Sphere")


# # Contact geometry of the foam brick

# In[ ]:


def show_brick_contact():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.01)
    Parser(plant).AddModelFromFile(
        FindResource("models/061_foam_brick_w_visual_contact_spheres.sdf"))
    plant.Finalize()

    meshcat.Delete()
    meshcat.ResetRenderMode()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    diagram.Publish(context)

show_brick_contact()


# # Point cloud processing with Open3d
# 
# I've produced a scene with multiple cameras looking at our favorite YCB mustard bottle.  I've taken the individual point clouds, converted them into Open3d's point cloud format, estimated their normals, merged the point clouds, cropped then point clouds (to get rid of the geometry from the other cameras), then downsampled the point clouds.  (The order is important!)
# 
# I've pushed all of the point clouds to meshcat, but with many of them set to not be visible by default.  Use the drop-down menu to turn them on and off, and make sure you understand basically what is happening on each of the steps.

# In[ ]:


import open3d as o3d
from manipulation.mustard_depth_camera_example import MustardExampleSystem
from manipulation.open3d_utils import create_open3d_point_cloud

def point_cloud_processing_example():
    # This just sets up our mustard bottle with three depth cameras positioned around it.
    system = MustardExampleSystem()

    plant = system.GetSubsystemByName("plant")

    # Evaluate the camera output ports to get the images.
    context = system.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    meshcat.Delete()
    meshcat.SetProperty("/Background", "visible", False)

    pcd = []
    for i in range(3):
        point_cloud = system.GetOutputPort(f"camera{i}_point_cloud").Eval(context)
        meshcat.SetObject(f"pointcloud{i}", point_cloud, point_size=0.001)
        meshcat.SetProperty(f"pointcloud{i}", "visible", False)

        cloud = create_open3d_point_cloud(point_cloud)
        # Crop to region of interest.
        pcd.append(cloud.crop(
            o3d.geometry.AxisAlignedBoundingBox(min_bound=[-.3, -.3, -.3],
                                                max_bound=[.3, .3, .3])))
        draw_open3d_point_cloud(meshcat, f"pointcloud{i}_cropped", pcd[i])
        meshcat.SetProperty(f"pointcloud{i}_cropped", "visible", False)

        pcd[i].estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1, max_nn=30))

        camera = plant.GetModelInstanceByName(f"camera{i}")
        body = plant.GetBodyByName("base", camera)
        X_C = plant.EvalBodyPoseInWorld(plant_context, body)
        pcd[i].orient_normals_towards_camera_location(X_C.translation())

    # Merge point clouds.  (Note: You might need something more clever here for
    # noisier point clouds; but this can often work!)
    merged_pcd = pcd[0] + pcd[1] + pcd[2]
    draw_open3d_point_cloud(meshcat, "merged", merged_pcd)

    # Voxelize down-sample.  (Note that the normals still look reasonable)
    down_sampled_pcd = merged_pcd.voxel_down_sample(voxel_size=0.005)
    draw_open3d_point_cloud(meshcat, "down_sampled", down_sampled_pcd)

    # TODO(russt): Make normal rendering work in Meshcat C++
    #draw_open3d_point_cloud(v["normals"], down_sampled_pcd, normals_scale=0.01)
    ## Let the normals be drawn, only turn off the object...
    #v["normals"]["<object>"].set_property("visible", False)

    # If we wanted to show it in the open3d visualizer, we would use...
    # print("Use 'n' to show normals, and '+/-' to change their size.")
    # o3d.visualization.draw_geometries([down_sampled_pcd])


point_cloud_processing_example()


# # Estimating normals (and local curvature)
# 
# TODO: Add the version from depth images (nearest pixels instead of nearest neighbors), and implement it in DepthImageToPointCloud.

# In[ ]:


import open3d as o3d
from manipulation.mustard_depth_camera_example import MustardExampleSystem

def normal_estimation():
    system = MustardExampleSystem()
    context = system.CreateDefaultContext()

    meshcat.Delete()
    meshcat.SetProperty("/Background", "visible", False)

    point_cloud = system.GetOutputPort("camera0_point_cloud").Eval(context)
    meshcat.SetObject("point_cloud", point_cloud)

    pcd = create_open3d_point_cloud(point_cloud)

    kdtree = o3d.geometry.KDTreeFlann(pcd)
    pts = np.asarray(pcd.points)

    neighbors= PointCloud(40)
    AddMeshcatTriad(meshcat, "least_squares_basis", length=0.03, radius=0.0005)

    meshcat.AddSlider("point", min=0, max=pts.shape[0]-1, step=1, value=4165)
    meshcat.AddButton("Stop Normal Estimation")
    print("Press the 'Stop Normal Estimation' button in Meshcat to continue")
    last_index = -1
    while meshcat.GetButtonClicks("Stop Normal Estimation") < 1:
        index = round(meshcat.GetSliderValue("point"))
        if index == last_index:
            time.sleep(.1)
            continue
        last_index = index
          
        query = pts[index,:]
        meshcat.SetObject("query", Sphere(0.001), Rgba(0, 1, 0))
        meshcat.SetTransform("query", RigidTransform(query))
        (num, indices, distances) = kdtree.search_hybrid_vector_3d(
            query=query, radius=0.1, max_nn=40)

        neighbors.resize(num)
        neighbors.mutable_xyzs()[:] = pts[indices, :].T

        meshcat.SetObject("neighbors", neighbors,
                          rgba=Rgba(0, 0, 1), point_size=0.001)

        neighbor_pts = neighbors.xyzs().T
        pstar = np.mean(neighbor_pts,axis=0)
        prel = neighbor_pts - pstar
        W = np.matmul(prel.T, prel)
        w, V = np.linalg.eigh(W)
        R = np.fliplr(V)
        # Handle improper rotations
        R = np.diag([1, 1, np.linalg.det(R)]) @ R
        # Flip normals
        if R[0,2] < 0: 
            R = -R
        meshcat.SetTransform("least_squares_basis", RigidTransform(
            RotationMatrix(R), query))

        if not running_as_notebook:
            break

    meshcat.DeleteAddedControls()

normal_estimation()


# # Scoring grasp candidates

# In[ ]:


from pydrake.all import QueryObject
def grasp_candidate_cost(plant_context,
                         cloud,
                         plant,
                         query_object,
                         adjust_X_G=False,
                         text=False,
                         meshcat_path=None):
    clear_output(wait=True)
    q = plant.GetPositions(plant_context)
    if len(q)==6:
        X_G = RigidTransform(RollPitchYaw(q[3:]),q[:3])
    else:
        X_G = plant.GetFreeBodyPose(plant_context, plant.GetBodyByName("body"))

    # Transform cloud into gripper frame
    X_GW = X_G.inverse()
    pts = np.asarray(cloud.points).T
    p_GC = X_GW.multiply(pts)

    # Crop to a region inside of the finger box.
    crop_min = [-.05, 0.1, -0.00625]
    crop_max = [.05, 0.1125, 0.00625]
    indices = np.all((crop_min[0] <= p_GC[0,:], p_GC[0,:] <= crop_max[0],
                      crop_min[1] <= p_GC[1,:], p_GC[1,:] <= crop_max[1],
                      crop_min[2] <= p_GC[2,:], p_GC[2,:] <= crop_max[2]),
                     axis=0)

    if meshcat_path:
        pc = PointCloud(np.sum(indices))
        pc.mutable_xyzs()[:] = pts[:, indices]
        meshcat.SetObject("planning/points", pc, rgba=Rgba(1., 0, 0), point_size=0.01)

    if adjust_X_G and np.sum(indices)>0:
        p_GC_x = p_GC[0, indices]
        p_Gcenter_x = (p_GC_x.min() + p_GC_x.max())/2.0
        X_G.set_translation(X_G.translation() + X_G.rotation().multiply([p_Gcenter_x, 0, 0]))
        if len(q)==6:
            q[:3] = X_G.translation()
            q[3:] = RollPitchYaw(X_G.rotation()).vector()
            plant.SetPositions(q)
        else:
            plant.SetFreeBodyPose(
                plant_context, plant.GetBodyByName("body"), X_G)

        X_GW = X_G.inverse()

    # Check collisions between the gripper and the sink
    if query_object.HasCollisions():
        cost = np.inf
        if text:
            print("Gripper is colliding with the sink!\n")
            print(f"cost: {cost}")
        return cost

    # Check collisions between the gripper and the point cloud
    margin = 0.0  # must be smaller than the margin used in the point cloud preprocessing.
    for pt in cloud.points:
        distances = query_object.ComputeSignedDistanceToPoint(pt, threshold=margin)
        if distances:
            cost = np.inf
            if text:
                print("Gripper is colliding with the point cloud!\n")
                print(f"cost: {cost}")
            return cost


    n_GC = X_GW.rotation().multiply(np.asarray(cloud.normals)[indices,:].T)

    # Penalize deviation of the gripper from vertical.
    # weight * -dot([0, 0, -1], R_G * [0, 1, 0]) = weight * R_G[2,1]
    cost = 20.0*X_G.rotation().matrix()[2, 1]

    # Reward sum |dot product of normals with gripper x|^2
    cost -= np.sum(n_GC[0,:]**2)

    if text:
        print(f"cost: {cost}")
        print(f"normal terms: {n_GC[0,:]**2}")
    return cost


class ScoreSystem(LeafSystem):
    def __init__(self, plant, cloud):
        LeafSystem.__init__(self)
        self._plant = plant
        self._cloud = cloud
        self._plant_context = plant.CreateDefaultContext()
        self.DeclareVectorInputPort("state", plant.num_multibody_states())
        self.DeclareAbstractInputPort("query_object",
                                      AbstractValue.Make(QueryObject()))
        self.DeclareForcedPublishEvent(self.Publish)

    def Publish(self, context):
        state = self.get_input_port(0).Eval(context)
        self._plant.SetPositionsAndVelocities(self._plant_context, state)
        query_object = self.get_input_port(1).Eval(context)
        grasp_candidate_cost(self._plant_context,
                             self._cloud,
                             self._plant,
                             query_object,
                             text=True,
                             meshcat_path="planning/cost")

        return EventStatus.Succeeded()


def process_point_cloud(diagram, context, cameras, bin_name):
    """A "no frills" version of the example above, that returns the down-sampled point cloud"""
    plant = diagram.GetSubsystemByName("plant")
    plant_context = plant.GetMyContextFromRoot(context)

    # Compute crop box.
    bin_instance = plant.GetModelInstanceByName(bin_name)
    bin_body = plant.GetBodyByName("bin_base", bin_instance)
    X_B = plant.EvalBodyPoseInWorld(plant_context, bin_body)
    margin = 0.001  # only because simulation is perfect!
    a = X_B.multiply([-.22+0.025+margin, -.29+0.025+margin, 0.015+margin])
    b = X_B.multiply([.22-0.1-margin, .29-0.025-margin, 2.0])
    crop_min = np.minimum(a,b)
    crop_max = np.maximum(a,b)

    # Evaluate the camera output ports to get the images.
    merged_pcd = o3d.geometry.PointCloud()
    for c in cameras:
        point_cloud = diagram.GetOutputPort(f"{c}_point_cloud").Eval(context)
        pcd = create_open3d_point_cloud(point_cloud)

        # Crop to region of interest.
        pcd = pcd.crop(
            o3d.geometry.AxisAlignedBoundingBox(min_bound=crop_min,
                                                max_bound=crop_max))

        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1, max_nn=30))

        camera = plant.GetModelInstanceByName(c)
        body = plant.GetBodyByName("base", camera)
        X_C = plant.EvalBodyPoseInWorld(plant_context, body)
        pcd.orient_normals_towards_camera_location(X_C.translation())

        # Merge point clouds.
        merged_pcd += pcd

    # Voxelize down-sample.  (Note that the normals still look reasonable)
    return merged_pcd.voxel_down_sample(voxel_size=0.005)


def make_environment_model(directive=None,
                           draw=False,
                           rng=None,
                           num_ycb_objects=0,
                           bin_name="bin0"):
    # Make one model of the environment, but the robot only gets to see the sensor outputs.
    if not directive:
        directive = FindResource("models/two_bins_w_cameras.yaml")

    builder = DiagramBuilder()
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0005)
    parser = Parser(plant)
    AddPackagePaths(parser)
    ProcessModelDirectives(LoadModelDirectives(directive), plant, parser)

    for i in range(num_ycb_objects):
        object_num = rng.integers(len(ycb))
        sdf = FindResourceOrThrow("drake/manipulation/models/ycb/sdf/" + ycb[object_num][1])
        parser.AddModelFromFile(sdf, f"object{i}")

    plant.Finalize()
    AddRgbdSensors(builder, plant, scene_graph)

    if draw:
        MeshcatVisualizer.AddToBuilder(
            builder, scene_graph, meshcat,
            MeshcatVisualizerParams(prefix="environment"))

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()

    if num_ycb_objects > 0:
        generator = RandomGenerator(rng.integers(1000))  # this is for c++
        plant_context = plant.GetMyContextFromRoot(context)
        bin_instance = plant.GetModelInstanceByName(bin_name)
        bin_body = plant.GetBodyByName("bin_base", bin_instance)
        X_B = plant.EvalBodyPoseInWorld(plant_context, bin_body)
        z = 0.1
        for body_index in plant.GetFloatingBaseBodies():
            tf = RigidTransform(
                    UniformlyRandomRotationMatrix(generator),
                    [rng.uniform(-.15,.15), rng.uniform(-.2, .2), z])
            plant.SetFreeBodyPose(plant_context,
                                plant.get_body(body_index),
                                X_B.multiply(tf))
            z += 0.1

        simulator = Simulator(diagram, context)
        simulator.AdvanceTo(1.0 if running_as_notebook else 0.1)
    elif draw:
        meshcat.load()
        diagram.Publish(context)


    return diagram, context


def grasp_score_inspector():
    environment, environment_context = make_environment_model(
        directive=FindResource("models/clutter_mustard.yaml"))

    # Another diagram for the objects the robot "knows about": gripper, cameras, bins.  Think of this as the model in the robot's head.
    builder = DiagramBuilder()
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    parser = Parser(plant)
    AddPackagePaths(parser)
    ProcessModelDirectives(
        LoadModelDirectives(FindResource("models/clutter_planning.yaml")),
        plant, parser)
    AddFloatingRpyJoint(plant, plant.GetFrameByName("body"),
                        plant.GetModelInstanceByName("gripper"))
    plant.Finalize()

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    params = MeshcatVisualizerParams()
    params.prefix = "planning"
    visualizer = MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat,
                                                params)

    cloud = process_point_cloud(environment, environment_context,
                                ["camera0", "camera1", "camera2"], "bin0")
    draw_open3d_point_cloud(meshcat, "planning/cloud", cloud, point_size=0.003)

    score = builder.AddSystem(ScoreSystem(plant, cloud))
    builder.Connect(plant.get_state_output_port(), score.get_input_port(0))
    builder.Connect(scene_graph.get_query_output_port(),
                    score.get_input_port(1))

    lower_limit = [-1, -1, 0, -np.pi, -np.pi/4., -np.pi/4.]
    upper_limit = [1, 1, 1, 0, np.pi/4., np.pi/4.]
    q0 = [-.05, -.5, .25, -np.pi / 2.0, 0, 0]
    default_interactive_timeout = None if running_as_notebook else 1.0
    sliders = builder.AddSystem(
        JointSliders(meshcat,
                     plant,
                     initial_value=q0,
                     lower_limit=lower_limit,
                     upper_limit=upper_limit))
    diagram = builder.Build()
    sliders.Run(diagram, default_interactive_timeout)
    meshcat.DeleteAddedControls()

grasp_score_inspector()


# # Generating grasp candidates

# In[ ]:


def generate_grasp_candidate_antipodal(plant_context, cloud, plant, scene_graph,
                                       scene_graph_context, rng):
    """
    Picks a random point in the cloud, and aligns the robot finger with the normal of that pixel. 
    The rotation around the normal axis is drawn from a uniform distribution over [min_roll, max_roll].
    """
    body = plant.GetBodyByName("body")

    index = rng.integers(0,len(cloud.points)-1)

    # Use S for sample point/frame.
    p_WS = np.asarray(cloud.points[index])
    n_WS = np.asarray(cloud.normals[index])

    if False:
        vertices = np.empty((3,2))
        vertices[:, 0] = p_WS
        vertices[:, 1] = p_WS + 0.05*n_WS
        meshcat.set_object(g.LineSegments(g.PointsGeometry(vertices),
                            g.MeshBasicMaterial(color=0xff0000)))

    assert np.isclose(np.linalg.norm(n_WS), 1.0)

    Gx = n_WS # gripper x axis aligns with normal
    # make orthonormal y axis, aligned with world down
    y = np.array([0.0, 0.0, -1.0])
    if np.abs(np.dot(y,Gx)) < 1e-6:
        # normal was pointing straight down.  reject this sample.
        return None

    Gy = y - np.dot(y,Gx)*Gx
    Gz = np.cross(Gx, Gy)
    R_WG = RotationMatrix(np.vstack((Gx, Gy, Gz)).T)
    p_GS_G = [0.054 - 0.01, 0.10625, 0]

    # Try orientations from the center out
    min_roll=-np.pi/3.0
    max_roll=np.pi/3.0
    alpha = np.array([0.5, 0.65, 0.35, 0.8, 0.2, 1.0, 0.0])
    for theta in (min_roll + (max_roll - min_roll)*alpha):
        # Rotate the object in the hand by a random rotation (around the normal).
        R_WG2 = R_WG.multiply(RotationMatrix.MakeXRotation(theta))

        # Use G for gripper frame.
        p_SG_W = - R_WG2.multiply(p_GS_G)
        p_WG = p_WS + p_SG_W

        X_G = RigidTransform(R_WG2, p_WG)
        plant.SetFreeBodyPose(plant_context, body, X_G)
        cost = grasp_candidate_cost(
            plant_context,
            cloud,
            plant,
            scene_graph.get_query_output_port().Eval(scene_graph_context),
            adjust_X_G=True)
        X_G = plant.GetFreeBodyPose(plant_context, body)
        if np.isfinite(cost):
            return cost, X_G

        #draw_grasp_candidate(X_G, f"collision/{theta:.1f}")

    return np.inf, None

def draw_grasp_candidate(X_G, prefix='gripper', draw_frames=True):
    builder = DiagramBuilder()
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    parser = Parser(plant)
    gripper = parser.AddModelFromFile(FindResource(
        "models/schunk_wsg_50_welded_fingers.sdf"), "gripper")
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("body"), X_G)
    plant.Finalize()

    #frames_to_draw = {"gripper": {"body"}} if draw_frames else {}
    params = MeshcatVisualizerParams()
    params.prefix = prefix
    params.delete_prefix_on_initialization_event = False
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat, params)
    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    diagram.Publish(context)

def sample_grasps_example():
    meshcat.Delete()
    rng = np.random.default_rng()

    environment, environment_context = make_environment_model(rng=rng, num_ycb_objects=5, draw=False)

    # Another diagram for the objects the robot "knows about": gripper, cameras, bins.  Think of this as the model in the robot's head.
    builder = DiagramBuilder()
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    parser = Parser(plant)
    AddPackagePaths(parser)
    ProcessModelDirectives(LoadModelDirectives(FindResource("models/clutter_planning.yaml")), plant, parser)
    plant.Finalize()

    params = MeshcatVisualizerParams()
    params.prefix = "planning"
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat, params)
    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    diagram.Publish(context)

    # Hide the planning gripper
    meshcat.SetProperty("planning/gripper", "visible", False)

    cloud = process_point_cloud(environment, environment_context, ["camera0", "camera1", "camera2"], "bin0")
    draw_open3d_point_cloud(meshcat, "planning/cloud", cloud, point_size=0.003)

    plant_context = plant.GetMyContextFromRoot(context)
    scene_graph_context = scene_graph.GetMyContextFromRoot(context)

    costs = []
    X_Gs = []
    for i in range(100 if running_as_notebook else 2):
        cost, X_G = generate_grasp_candidate_antipodal(plant_context, cloud, plant, scene_graph, scene_graph_context, rng)#, meshcat=v.vis["sample"])
        if np.isfinite(cost):
            costs.append(cost)
            X_Gs.append(X_G)

    indices = np.asarray(costs).argsort()[:5]
    for (rank, index) in enumerate(indices):
        draw_grasp_candidate(
            X_Gs[index], prefix=f"{rank}th best", draw_frames=False)


sample_grasps_example()


# In[ ]:




