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


# Imports
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import pydot
from IPython.display import SVG, clear_output, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, AngleAxis,
                         DiagramBuilder, EventStatus, FindResourceOrThrow,
                         Integrator, JacobianWrtVariable, JointSliders,
                         LeafSystem, LoadModelDirectives, MeshcatVisualizer,
                         MultibodyPlant, MultibodyPositionToGeometryPose,
                         Parser, PiecewisePolynomial, PiecewisePose,
                         ProcessModelDirectives, Quaternion, Rgba,
                         RigidTransform, RollPitchYaw, RotationMatrix,
                         SceneGraph, Simulator, StartMeshcat, TrajectorySource)

from manipulation import FindResource, running_as_notebook
from manipulation.scenarios import (AddMultibodyTriad, AddPackagePaths,
                                    MakeManipulationStation, SetColor)

if running_as_notebook:
    mpld3.enable_notebook()


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Inspecting the kinematic tree
# 
# Here is a simple example that demonstrates how to inspect the kinematic tree stored in a `MultibodyPlant`.

# In[ ]:


def kinematic_tree_example():
    plant = MultibodyPlant(time_step=0.0)
    parser = Parser(plant)
    parser.AddModelFromFile(FindResourceOrThrow(
        "drake/manipulation/models/allegro_hand_description/sdf/allegro_hand_description_right.sdf"))
    parser.AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf"))
    plant.Finalize()

    # TODO(russt): Add floating base connections
    # TODO(russt): Consider a more interactive javascript rendering?
    display(SVG(pydot.graph_from_dot_data(plant.GetTopologyGraphvizString())[0].create_svg()))

kinematic_tree_example()


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
        clear_output(wait=True)
        print("gripper position (m): " + np.array2string(
            pose.translation(), formatter={
                'float': lambda x: "{:3.2f}".format(x)}))
        print("gripper roll-pitch-yaw (rad):" + np.array2string(
            RollPitchYaw(pose.rotation()).vector(),
                         formatter={'float': lambda x: "{:3.2f}".format(x)}))
        return EventStatus.Succeeded()

def gripper_forward_kinematics_example():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0)
    parser = Parser(plant)
    AddPackagePaths(parser)
    # TODO: Clean up pending https://github.com/RobotLocomotion/drake/issues/17390
    ProcessModelDirectives(
        LoadModelDirectives(FindResource("models/iiwa_and_wsg.dmd.yaml")),
        parser)
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


# # Don't assume $\dot{q} \equiv v$
# 
# Let's just add a single object into the scene.  We won't weld it to the world frame, so it is a "free body" or has a "floating base".

# In[ ]:


def num_positions_velocities_example():
    plant = MultibodyPlant(time_step = 0.0)
    Parser(plant).AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf"))
    plant.Finalize()

    context = plant.CreateDefaultContext()
    print(context)

    print(f"plant.num_positions() = {plant.num_positions()}")
    print(f"plant.num_velocities() = {plant.num_velocities()}")

num_positions_velocities_example()


# Looking at the `Context` you can see that this system has 13 total state variables.  7 of them are positions, $q$; this is due to our pose representation using unit quaternions.  But only 6 of them are velocities, $v$; this is because a six-element spatial velocity provides a better (unconstrained) representation of the rate of change of the unit quaternion.  But clearly, if the length of the vectors don't even match, we do *not* have $\dot{q} = v$.

# # Kinematic Jacobians for pick and place
# 
# Let's set up the same iiwa + wsg example, with sliders (but without the frames), that we used above.  But this time I'll display the value of the Jacobian $J^G(q)$.

# In[ ]:


class PrintJacobian(LeafSystem):
    def __init__(self, plant, frame):
        LeafSystem.__init__(self)
        self._plant = plant
        self._plant_context = plant.CreateDefaultContext()
        self._frame = frame
        self.DeclareVectorInputPort("state", plant.num_multibody_states())
        self.DeclareForcedPublishEvent(self.Publish)

    def Publish(self, context):
        state = self.get_input_port().Eval(context)
        self._plant.SetPositionsAndVelocities(self._plant_context, state)
        W = self._plant.world_frame()
        J_G = self._plant.CalcJacobianSpatialVelocity(
            self._plant_context, JacobianWrtVariable.kQDot, self._frame,
            [0, 0, 0], W, W)  ## This is the important line

        clear_output(wait=True)
        print("J_G:")
        print(np.array2string(J_G, formatter={
              'float': lambda x: "{:5.1f}".format(x)}))
        print(
            f"smallest singular value(J_G): {np.min(np.linalg.svd(J_G, compute_uv=False))}")
        return EventStatus.Succeeded()

def pick_and_place_jacobians_example():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0)
    parser = Parser(plant)
    AddPackagePaths(parser)
    ProcessModelDirectives(
        LoadModelDirectives(FindResource("models/iiwa_and_wsg.dmd.yaml")),
        parser)
    plant.Finalize()

    meshcat.Delete()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph.get_query_output_port(), meshcat)

    G = plant.GetBodyByName("body").body_frame()
    print_jacobian = builder.AddSystem(PrintJacobian(plant, G))
    builder.Connect(plant.get_state_output_port(),
                    print_jacobian.get_input_port())

    # If you want to set the initial positions manually, use this:
    #plant.SetPositions(plant.GetMyContextFromRoot(context),
    #                   plant.GetModelInstanceByName("iiwa"),
    #                   [0, 0, 0, 0, 0, 0, 0])

    default_interactive_timeout = None if running_as_notebook else 1.0
    sliders = builder.AddSystem(JointSliders(meshcat, plant))
    diagram = builder.Build()
    sliders.Run(diagram, default_interactive_timeout)
    meshcat.DeleteAddedControls()

pick_and_place_jacobians_example()


# # Our first end-effector "controller"
# 
# Let's use the pseudo-inverse of the Jacobian to drive the robot around.  To do that, we'll write a very simple system that looks at the current value of $q$, computes $[J^G]^+$, and uses it to command a constant spatial velocity, $V^G$.
# 
# We'll only run this controller for a short duration.  Constant spatial velocities aren't something that makes sense for a longer simulation!
# 
# Make sure you try changing $V^G$, and understand how the command relates to the motion of the robot.

# In[ ]:


# We can write a new System by deriving from the LeafSystem class.
# There is a little bit of boiler plate, but hopefully this example makes sense.
class PseudoInverseController(LeafSystem):
    def __init__(self, plant):
        LeafSystem.__init__(self)
        self._plant = plant
        self._plant_context = plant.CreateDefaultContext()
        self._iiwa = plant.GetModelInstanceByName("iiwa")
        self._G = plant.GetBodyByName("body").body_frame()
        self._W = plant.world_frame()

        self.DeclareVectorInputPort("iiwa_position", 7)
        self.DeclareVectorOutputPort("iiwa_velocity", 7,
                                     self.CalcOutput)

    def CalcOutput(self, context, output):
        q = self.get_input_port().Eval(context)
        self._plant.SetPositions(self._plant_context, self._iiwa, q)
        J_G = self._plant.CalcJacobianSpatialVelocity(
            self._plant_context, JacobianWrtVariable.kQDot,
            self._G, [0,0,0], self._W, self._W)
        J_G = J_G[:,0:7] # Ignore gripper terms

        V_G_desired = np.array([0,    # rotation about x
                                -.1,  # rotation about y
                                0,    # rotation about z
                                0,    # x
                                -.05, # y
                                -.1]) # z
        v = np.linalg.pinv(J_G).dot(V_G_desired)
        output.SetFromVector(v)


def jacobian_controller_example():
    builder = DiagramBuilder()

    station = builder.AddSystem(
        MakeManipulationStation(
            filename=FindResource("models/iiwa_and_wsg.dmd.yaml")))
    plant = station.GetSubsystemByName("plant")

    controller = builder.AddSystem(PseudoInverseController(plant))
    integrator = builder.AddSystem(Integrator(7))

    builder.Connect(controller.get_output_port(),
                    integrator.get_input_port())
    builder.Connect(integrator.get_output_port(),
                    station.GetInputPort("iiwa_position"))
    builder.Connect(station.GetOutputPort("iiwa_position_measured"),
                    controller.get_input_port())

    meshcat.Delete()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, station.GetOutputPort("query_object"), meshcat)

    diagram = builder.Build()
    simulator = Simulator(diagram)
    context = simulator.get_mutable_context()
    station_context = station.GetMyContextFromRoot(context)
    station.GetInputPort("iiwa_feedforward_torque").FixValue(
        station_context, np.zeros((7, 1)))
    station.GetInputPort("wsg_position").FixValue(station_context, [0.1])
    integrator.set_integral_value(
        integrator.GetMyContextFromRoot(context),
        plant.GetPositions(plant.GetMyContextFromRoot(context),
                           plant.GetModelInstanceByName("iiwa")))

    simulator.set_target_realtime_rate(1.0)
    simulator.AdvanceTo(0.01);

    return simulator

simulator = jacobian_controller_example()


# In[ ]:


# Wait for the model to load in the visualizer, then run this cell to see the interesting part...
simulator.AdvanceTo(5.0 if running_as_notebook else 0.1);


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


# # A pick and place "sketch" with keyframes
# 
# Let's first define the canonical frames of our problem.  We've got a handful of them, and will pass them in and out of several functions, so I'll use a dictionary to store them.
# 
# *Edit*: I've added one more frame into the mix here, to get some clearance when moving between the bins.  Leaving it out gave my a nice [robot outtake](http://manipulation.csail.mit.edu/data/pick_fail.html), but we can do better.

# In[ ]:


def make_gripper_frames(X_G, X_O):
    """
    Takes a partial specification with X_G["initial"] and X_O["initial"] and X_0["goal"], and 
    returns a X_G and times with all of the pick and place frames populated.
    """
    # Define (again) the gripper pose relative to the object when in grasp.
    p_GgraspO = [0, 0.11, 0]
    R_GgraspO = RotationMatrix.MakeXRotation(np.pi/2.0).multiply(
        RotationMatrix.MakeZRotation(np.pi/2.0))
    X_GgraspO = RigidTransform(R_GgraspO, p_GgraspO)
    X_OGgrasp = X_GgraspO.inverse()
    # pregrasp is negative y in the gripper frame (see the figure!).
    X_GgraspGpregrasp = RigidTransform([0, -0.08, 0])

    X_G["pick"] = X_O["initial"].multiply(X_OGgrasp)
    X_G["prepick"] = X_G["pick"].multiply(X_GgraspGpregrasp)
    X_G["place"] = X_O["goal"].multiply(X_OGgrasp)
    X_G["preplace"] = X_G["place"].multiply(X_GgraspGpregrasp)

    # I'll interpolate a halfway orientation by converting to axis angle and halving the angle.
    X_GprepickGpreplace = X_G["prepick"].inverse().multiply(X_G["preplace"])
    angle_axis = X_GprepickGpreplace.rotation().ToAngleAxis()
    X_GprepickGclearance = RigidTransform(AngleAxis(angle=angle_axis.angle()/2.0, axis=angle_axis.axis()),
                                          X_GprepickGpreplace.translation()/2.0 + np.array([0, -0.3, 0]))
    X_G["clearance"] = X_G["prepick"].multiply(X_GprepickGclearance)

    # Now let's set the timing
    times = {"initial": 0}
    X_GinitialGprepick = X_G["initial"].inverse().multiply(X_G["prepick"])
    times["prepick"] = times["initial"] + 10.0*np.linalg.norm(X_GinitialGprepick.translation())
    # Allow some time for the gripper to close.
    times["pick_start"] = times["prepick"] + 2.0
    times["pick_end"] = times["pick_start"] + 2.0
    X_G["pick_start"] = X_G["pick"]
    X_G["pick_end"] = X_G["pick"]
    times["postpick"] = times["pick_end"] + 2.0
    X_G["postpick"] = X_G["prepick"]
    time_to_from_clearance = 10.0*np.linalg.norm(X_GprepickGclearance.translation())
    times["clearance"] = times["postpick"] + time_to_from_clearance
    times["preplace"] = times["clearance"] + time_to_from_clearance
    times["place_start"] = times["preplace"] + 2.0
    times["place_end"] = times["place_start"] + 2.0
    X_G["place_start"] = X_G["place"]
    X_G["place_end"] = X_G["place"]
    times["postplace"] = times["place_end"] + 2.0
    X_G["postplace"] = X_G["preplace"]

    return X_G, times

X_G = {"initial": RigidTransform(RotationMatrix.MakeXRotation(-np.pi/2.0), [0, -0.25, 0.25])}
X_O = {
    "initial":
        RigidTransform(RotationMatrix.MakeZRotation(np.pi / 2.0),
                       [-.2, -.75, 0.025]),
    "goal":
        RigidTransform(RotationMatrix.MakeZRotation(np.pi), [.75, 0, 0.025])
}
X_G, times = make_gripper_frames(X_G, X_O)
print(f"Sanity check: The entire maneuver will take {times['postplace']} seconds to execute.")


# Here's a simple visualization of those frames.  Use the controls menu in meshcat to view the different objects on the different "paths" to understand which objects belong to which frames.  Everything look reasonable?
# 
# Try changing the initial and final pose of the gripper / object.

# In[ ]:


def visualize_gripper_frames(X_G, X_O):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step = 0.0)
    parser = Parser(plant, scene_graph)
    gripper = FindResourceOrThrow(
        "drake/manipulation/models/wsg_50_description/sdf/schunk_wsg_50_no_tip.sdf")
    brick = FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf")
    for key, pose in X_G.items():
      g = parser.AddModelFromFile(gripper, f"gripper_{key}")
      plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("body", g), pose)
    for key, pose in X_O.items():
      o = parser.AddModelFromFile(brick, f"object_{key}")
      plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("base_link", o), pose)

    plant.Finalize()

    meshcat.Delete()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    diagram.Publish(context)

visualize_gripper_frames(X_G, X_O)


# # Pick and place trajectories
# 
# We've defined the keyframes, but now we will fill in timing details (what should be happening at each instant).
# 
# Interpolating between the positions is quite simple; we can encode these details as a `PiecewisePolynomial` trajectory in $\Re^3$ over time.  Interpolating over orientations requires more care.  We'll use `PiecewiseQuaternionSlerp` to do the job.
# 
# See the documentation of [PiecewisePose](https://drake.mit.edu/doxygen_cxx/classdrake_1_1trajectories_1_1_piecewise_pose.html#ae2f8a49b642aecb5c19ef3625be5e61d) for more details.

# In[ ]:


def make_gripper_trajectory(X_G, times):
    """
    Constructs a gripper position trajectory from the plan "sketch".
    """

    sample_times = []
    poses = []
    for name in ["initial", "prepick", "pick_start", "pick_end", "postpick",
                 "clearance", "preplace", "place_start", "place_end",
                 "postplace"]:
        sample_times.append(times[name])
        poses.append(X_G[name])

    return PiecewisePose.MakeLinear(sample_times, poses)

traj = make_gripper_trajectory(X_G, times)


# Now let's plot our trajectories.

# In[ ]:


traj_p_G = traj.get_position_trajectory()

p_G = traj_p_G.vector_values(traj_p_G.get_segment_times())
plt.plot(traj_p_G.get_segment_times(), p_G.T)
plt.legend(['x', 'y', 'z'])
plt.title('p_G')
mpld3.display()


# We can also plot the trajectory in 3D directly in Meshcat.

# In[ ]:


meshcat.ResetRenderMode()
meshcat.SetLine('p_G', p_G, 2.0, rgba=Rgba(1, 0.65, 0))


# We can plot the orientation trajectory, too.  Here are the components of the quaternion over time.

# In[ ]:


traj_R_G = traj.get_orientation_trajectory()
R_G = traj_R_G.vector_values(traj_R_G.get_segment_times())
plt.plot(traj_R_G.get_segment_times(), R_G.T)
plt.legend(['qx', 'qy', 'qz', 'qw'])
plt.title('R_G')
mpld3.display()


# Better, I think, to just plot the entire result.  Before we do, let's quickly define the finger trajectory.

# In[ ]:


opened = np.array([0.107]);
closed = np.array([0.0]);

def make_wsg_command_trajectory(times):
    traj_wsg_command = PiecewisePolynomial.FirstOrderHold(
        [times["initial"], times["pick_start"]], np.hstack([[opened], [opened]]))
    traj_wsg_command.AppendFirstOrderSegment(times["pick_end"], closed)
    traj_wsg_command.AppendFirstOrderSegment(times["place_start"], closed)
    traj_wsg_command.AppendFirstOrderSegment(times["place_end"], opened)
    traj_wsg_command.AppendFirstOrderSegment(times["postplace"], opened)
    return traj_wsg_command

traj_wsg_command = make_wsg_command_trajectory(times)


# In[ ]:


wsg_command = traj_wsg_command.vector_values(
    traj_wsg_command.get_segment_times())
plt.plot(traj_wsg_command.get_segment_times(), wsg_command.T)
plt.title('wsg_command')
mpld3.display()


# Now let's really visualize the trajectory.  The best way is to animate it in 3D!  Please forgive the messiness of this particular bit of code; I'm trying to provide some intermediate steps that aren't typically used by the main drake developers.
# 
# TODO(russt): make this less "bespoke".

# In[ ]:


class GripperTrajectoriesToPosition(LeafSystem):
    def __init__(self, plant, traj_p_G, traj_R_G, traj_wsg_command):
        LeafSystem.__init__(self)
        self.plant = plant
        self.gripper_body = plant.GetBodyByName("body")
        self.left_finger_joint = plant.GetJointByName("left_finger_sliding_joint")
        self.right_finger_joint = plant.GetJointByName("right_finger_sliding_joint")
        self.traj_p_G = traj_p_G
        self.traj_R_G = traj_R_G
        self.traj_wsg_command = traj_wsg_command
        self.plant_context = plant.CreateDefaultContext()

        self.DeclareVectorOutputPort("position",
                                     plant.num_positions(),
                                     self.CalcPositionOutput)

    def CalcPositionOutput(self, context, output):
        t = context.get_time()
        X_G = RigidTransform(Quaternion(self.traj_R_G.value(t)), self.traj_p_G.value(t))
        self.plant.SetFreeBodyPose(self.plant_context, self.gripper_body, X_G)
        wsg = self.traj_wsg_command.value(t)
        self.left_finger_joint.set_translation(self.plant_context, -wsg/2.0)
        self.right_finger_joint.set_translation(self.plant_context, wsg/2.0)
        output.SetFromVector(self.plant.GetPositions(self.plant_context))

def visualize_pick_and_place_trajectory(traj_p_G, traj_R_G, traj_wsg_command, X_O):
    builder = DiagramBuilder()

    # Note: Don't use AddMultibodyPlantSceneGraph because we are only using
    # MultibodyPlant for parsing, then wiring directly to SceneGraph.
    scene_graph = builder.AddSystem(SceneGraph())
    plant = MultibodyPlant(time_step=0.0)
    plant.RegisterAsSourceForSceneGraph(scene_graph)
    parser = Parser(plant, scene_graph)
    gripper = parser.AddModelFromFile(FindResourceOrThrow(
        "drake/manipulation/models/wsg_50_description/sdf/schunk_wsg_50_no_tip.sdf"), "gripper")
    brick = FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf")
    for key, pose in X_O.items():
        o = parser.AddModelFromFile(brick, f"object_{key}")
        plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("base_link", o), pose)
    plant.Finalize()

    to_pose = builder.AddSystem(MultibodyPositionToGeometryPose(plant))
    builder.Connect(to_pose.get_output_port(), scene_graph.get_source_pose_port(plant.get_source_id()))

    traj_to_position = builder.AddSystem(
        GripperTrajectoriesToPosition(plant, traj_p_G, traj_R_G,
                                      traj_wsg_command))
    builder.Connect(traj_to_position.get_output_port(), to_pose.get_input_port())

    meshcat.Delete()
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)

    diagram = builder.Build()

    simulator = Simulator(diagram)
    # TODO(russt): get recording working again with new Meshcat (and remove realtime rate)
    #meshcat.start_recording()
    if running_as_notebook:
        simulator.set_target_realtime_rate(1.0)
    simulator.AdvanceTo(traj_p_G.end_time() if running_as_notebook else 0.1)
    #meshcat.publish_recording()

visualize_pick_and_place_trajectory(traj_p_G, traj_R_G, traj_wsg_command, X_O)


# # Putting it all together
# 
# In the visualization above, we animated the plan, but did not actually command the robot!  Let's put our grasping trajectories back together with our Jacobian-based controller.
# 
# The first thing you might have noticed is that the Jacobian controller takes spatial velocities as input.  But so far we have trajectories for positions and orientations.  Let's differentiate them to get the velocities.

# In[ ]:


traj_v_G = traj_p_G.MakeDerivative()

v_G = traj_v_G.vector_values(traj_v_G.get_segment_times())
plt.plot(traj_v_G.get_segment_times(), v_G.T)
plt.legend(['vx', 'vy', 'vz'])
plt.title('v_G')
mpld3.display()


# Now we need a slightly modified version of our Jacobian controller, which can take the spatial velocity commands from an input port.

# In[ ]:


# We can write a new System by deriving from the LeafSystem class.
# There is a little bit of boiler plate, but hopefully this example makes sense.
class PseudoInverseController(LeafSystem):
    def __init__(self, plant):
        LeafSystem.__init__(self)
        self._plant = plant
        self._plant_context = plant.CreateDefaultContext()
        self._iiwa = plant.GetModelInstanceByName("iiwa")
        self._G = plant.GetBodyByName("body").body_frame()
        self._W = plant.world_frame()

        self.V_G_port = self.DeclareVectorInputPort("V_WG", 6)
        self.q_port = self.DeclareVectorInputPort("iiwa_position", 7)
        self.DeclareVectorOutputPort("iiwa_velocity", 7, self.CalcOutput)
        self.iiwa_start = plant.GetJointByName("iiwa_joint_1").velocity_start()
        self.iiwa_end = plant.GetJointByName("iiwa_joint_7").velocity_start()

    def CalcOutput(self, context, output):
        V_G = self.V_G_port.Eval(context)
        q = self.q_port.Eval(context)
        self._plant.SetPositions(self._plant_context, self._iiwa, q)
        J_G = self._plant.CalcJacobianSpatialVelocity(
            self._plant_context, JacobianWrtVariable.kV,
            self._G, [0,0,0], self._W, self._W)
        J_G = J_G[:,self.iiwa_start:self.iiwa_end+1] # Only iiwa terms.
        v = np.linalg.pinv(J_G).dot(V_G)
        output.SetFromVector(v)


# Oh, boy.  Big moment.  I'm excited... are you?  Let's do this thing!

# In[ ]:


X_O = {"initial": RigidTransform(RotationMatrix.MakeZRotation(np.pi/2.0), [-.2, -.65, 0.0]),
       "goal": RigidTransform(RotationMatrix.MakeZRotation(np.pi),[.5, 0, 0.0])}

builder = DiagramBuilder()

model_directives = """
directives:
- add_directives:
    file: package://manipulation/clutter.dmd.yaml
- add_model:
    name: foam_brick
    file: package://drake/examples/manipulation_station/models/061_foam_brick.sdf
"""
station = builder.AddSystem(
    MakeManipulationStation(model_directives=model_directives))
plant = station.GetSubsystemByName("plant")
plant.SetDefaultFreeBodyPose(plant.GetBodyByName("base_link"), X_O['initial'])

# Find the initial pose of the gripper (as set in the default Context)
temp_context = station.CreateDefaultContext()
temp_plant_context = plant.GetMyContextFromRoot(temp_context)
X_G = {
    "initial":
        plant.EvalBodyPoseInWorld(temp_plant_context,
                                  plant.GetBodyByName("body"))
}
X_G, times = make_gripper_frames(X_G, X_O)
print(f"Sanity check: The entire maneuver will take {times['postplace']} seconds to execute.")

# Make the trajectories
traj = make_gripper_trajectory(X_G, times)
traj_V_G = traj.MakeDerivative()

V_G_source = builder.AddSystem(TrajectorySource(traj_V_G))
V_G_source.set_name("v_WG")
controller = builder.AddSystem(PseudoInverseController(plant))
controller.set_name("PseudoInverseController")
builder.Connect(V_G_source.get_output_port(), controller.GetInputPort("V_WG"))

integrator = builder.AddSystem(Integrator(7))
integrator.set_name("integrator")
builder.Connect(controller.get_output_port(),
                integrator.get_input_port())
builder.Connect(integrator.get_output_port(),
                station.GetInputPort("iiwa_position"))
builder.Connect(station.GetOutputPort("iiwa_position_measured"),
                controller.GetInputPort("iiwa_position"))

traj_wsg_command = make_wsg_command_trajectory(times)
wsg_source = builder.AddSystem(TrajectorySource(traj_wsg_command))
wsg_source.set_name("wsg_command")
builder.Connect(wsg_source.get_output_port(), station.GetInputPort("wsg_position"))

meshcat.Delete()
visualizer = MeshcatVisualizer.AddToBuilder(
    builder, station.GetOutputPort("query_object"), meshcat)

diagram = builder.Build()
diagram.set_name("pick_and_place")

simulator = Simulator(diagram)
context = simulator.get_mutable_context()
station_context = station.GetMyContextFromRoot(context)
integrator.set_integral_value(
    integrator.GetMyContextFromRoot(context),
    plant.GetPositions(plant.GetMyContextFromRoot(context),
                       plant.GetModelInstanceByName("iiwa")))

if running_as_notebook:
    simulator.set_target_realtime_rate(1.0)
visualizer.StartRecording()
simulator.AdvanceTo(traj_p_G.end_time() if running_as_notebook else 0.1)
visualizer.PublishRecording()


# That's quite some diagram we've assembled.  Do you understand all of the parts?

# In[ ]:


SVG(
    pydot.graph_from_dot_data(
        diagram.GetGraphvizString(max_depth=1))[0].create_svg())


# In[ ]:




