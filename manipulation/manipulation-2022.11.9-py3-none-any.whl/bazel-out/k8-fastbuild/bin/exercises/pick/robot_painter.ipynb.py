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

# # Robot Painter

# In[ ]:


import matplotlib.pyplot as plt
import mpld3
import numpy as np
from IPython.display import HTML, display
from manipulation import running_as_notebook, FindResource
from manipulation.meshcat_utils import AddMeshcatTriad
from manipulation.scenarios import MakeManipulationStation
from pydrake.all import (AddMultibodyPlantSceneGraph, AngleAxis, BasicVector,
                         ConstantVectorSource, DiagramBuilder,
                         FindResourceOrThrow, Integrator, JacobianWrtVariable,
                         LeafSystem, MeshcatVisualizer,
                         MeshcatVisualizerParams, MultibodyPlant,
                         MultibodyPositionToGeometryPose, Parser,
                         PiecewisePose, Quaternion, RigidTransform,
                         RollPitchYaw, RotationMatrix, SceneGraph, Simulator,
                         StartMeshcat, TrajectorySource)


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# In the following cell we provide a wrapper class that hides parts of the implementation details in Drake. You are not required to understand how it works.

# In[ ]:


class IIWA_Painter():
    def __init__(self, traj=None):
        builder = DiagramBuilder()
        # set up the system of manipulation station
        self.station = MakeManipulationStation(filename=FindResource("models/clutter.dmd.yaml"))

        builder.AddSystem(self.station)
        self.plant = self.station.GetSubsystemByName("plant")

        # optionally add trajectory source
        if traj is not None:
            traj_V_G = traj.MakeDerivative()
            V_G_source = builder.AddSystem(TrajectorySource(traj_V_G))
            self.controller = builder.AddSystem(
                PseudoInverseController(self.plant))
            builder.Connect(V_G_source.get_output_port(),
                            self.controller.GetInputPort("V_G"))

            self.integrator = builder.AddSystem(Integrator(7))
            builder.Connect(self.controller.get_output_port(),
                            self.integrator.get_input_port())
            builder.Connect(self.integrator.get_output_port(),
                            self.station.GetInputPort("iiwa_position"))
            builder.Connect(
                self.station.GetOutputPort("iiwa_position_measured"),
                self.controller.GetInputPort("iiwa_position"))

        params = MeshcatVisualizerParams()
        params.delete_on_initialization_event = False
        self.visualizer = MeshcatVisualizer.AddToBuilder(
            builder, self.station.GetOutputPort("query_object"), meshcat, params)

        wsg_position = builder.AddSystem(ConstantVectorSource([0.1]))
        builder.Connect(wsg_position.get_output_port(),
                        self.station.GetInputPort("wsg_position"))

        self.diagram = builder.Build()
        self.gripper_frame = self.plant.GetFrameByName('body')
        self.world_frame = self.plant.world_frame()

        context = self.CreateDefaultContext()
        self.diagram.Publish(context)

    def visualize_frame(self, name, X_WF, length=0.15, radius=0.006):
        """
        visualize imaginary frame that are not attached to existing bodies
        
        Input: 
            name: the name of the frame (str)
            X_WF: a RigidTransform to from frame F to world.
        
        Frames whose names already exist will be overwritten by the new frame
        """
        AddMeshcatTriad(meshcat, "painter/" + name,
                        length=length, radius=radius, X_PT=X_WF)

    def CreateDefaultContext(self):
        context = self.diagram.CreateDefaultContext()
        plant_context = self.diagram.GetMutableSubsystemContext(
            self.plant, context)
        station_context = self.diagram.GetMutableSubsystemContext(
            self.station, context)

        # provide initial states
        q0 = np.array([ 1.40666193e-05,  1.56461165e-01, -3.82761069e-05,
                       -1.32296976e+00, -6.29097287e-06,  1.61181157e+00, -2.66900985e-05])
        # set the joint positions of the kuka arm
        iiwa = self.plant.GetModelInstanceByName("iiwa")
        self.plant.SetPositions(plant_context, iiwa, q0)
        self.plant.SetVelocities(plant_context, iiwa, np.zeros(7))
        wsg = self.plant.GetModelInstanceByName("wsg")
        self.plant.SetPositions(plant_context, wsg, [-0.05, 0.05])
        self.plant.SetVelocities(plant_context, wsg, [0, 0])        

        if hasattr(self, 'integrator'):
            self.integrator.set_integral_value(
                self.integrator.GetMyMutableContextFromRoot(context), q0)

        return context


    def get_X_WG(self, context=None):

        if not context:
            context = self.CreateDefaultContext()
        plant_context = self.plant.GetMyMutableContextFromRoot(context)
        X_WG = self.plant.CalcRelativeTransform(
                    plant_context,
                    frame_A=self.world_frame,
                    frame_B=self.gripper_frame)
        return X_WG

    def paint(self, sim_duration=20.0):
        context = self.CreateDefaultContext()
        simulator = Simulator(self.diagram, context)
        simulator.set_target_realtime_rate(1.0)

        duration = sim_duration if running_as_notebook else 0.01
        simulator.AdvanceTo(duration)

class PseudoInverseController(LeafSystem):
    """
    same controller seen in-class
    """
    def __init__(self, plant):
        LeafSystem.__init__(self)
        self._plant = plant
        self._plant_context = plant.CreateDefaultContext()
        self._iiwa = plant.GetModelInstanceByName("iiwa")
        self._G = plant.GetBodyByName("body").body_frame()
        self._W = plant.world_frame()

        self.V_G_port = self.DeclareVectorInputPort("V_G", BasicVector(6))
        self.q_port = self.DeclareVectorInputPort("iiwa_position", BasicVector(7))
        self.DeclareVectorOutputPort("iiwa_velocity", BasicVector(7),
                                     self.CalcOutput)
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
        v = np.linalg.pinv(J_G).dot(V_G) #important
        output.SetFromVector(v)


# # Problem Description
# In the lecture, we learned the basics of spatial transformations. For this exercise, you will have iiwa arm *paint* a circular, planar trajectory by computing and interpolating the key frames, just as we have seen from the lecture
# 
# **These are the main steps of the exercise:**
# 1. Design and implement a circular trajectory for the Iiwa arm to follow.
# 2. Observe and reflect on the Differential IK controller.

# # Circular Trajectory
# 
# In this exercise, you will design a circular planar trajectory like the one below for the iiwa arm to follow, like a robot painting in the air! To do so, we will follow the same procedure as shown in class:
# 
# (1) compute the key frames of the circular trajectory
# 
# (2) construct interpolated trajectory from the key frames

# <img src="https://raw.githubusercontent.com/RussTedrake/manipulation/master/figures/exercises/robot_painter_circle.png" width="700">

# The x and y axis in the diagram above are from the world frame.

# <img src="https://raw.githubusercontent.com/RussTedrake/manipulation/master/figures/exercises/robot_painter_screenshot.png" width="700">

# The screenshot above visualizes the key frames of the circular trajectory. The key frames illustrate the poses of the gripper in the world frame at different time steps along the trajectory. First, you should notice from the visualization above that the gripper frame is different from the world frame. In particular, the +y axis of the gripper frame points vertically downward, and the +z axis of the gripper points backward. This is an important observation for this exercise.
# 
# The rigid transform of the center of the circular trajectory as well as the radius of the circle is defined below. In words, we would like to have our arm rotate counterclockwise about the +z axis in the world frame. Besides, we would like the +z axis of the gripper frame to always point toward the center of the circle. 

# In[ ]:


# define center and radius
radius = 0.1
p0 = [0.45, 0.0, 0.4]
R0 = RotationMatrix(np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]]).T)
X_WorldCenter = RigidTransform(R0, p0)

num_key_frames = 10
"""
you may use different thetas as long as your trajectory starts
from the Start Frame above and your rotation is positive
in the world frame about +z axis
thetas = np.linspace(0, 2*np.pi, num_key_frames)
"""
thetas = np.linspace(0, 2*np.pi, num_key_frames)

painter = IIWA_Painter()


# We have provided an `IIWA_painter` class at the very top of this notebook to help you abstract away parts of the implementation details in Drake. You may find `visualize_frame` method helpful to visualize rigid transforms. The cell below first computes the rigid transform of the current gripper pose, and then it draws a frame of that pose in meshcat. Note that the frame drawn here is not attached to any body in the scene. They are for visualization only.

# In[ ]:


X_WG = painter.get_X_WG()
painter.visualize_frame('gripper_current', X_WG)


# Finally, you can compose arbitrary rotations via `MakeXRotation`, `MakeYRotation`, and `MakeZRotation` methods. Their names are quite self-explanatory.

# In[ ]:


RotationMatrix.MakeYRotation(np.pi/6.0)


# **Below, your job is to complete the compose_circular_key_frames method given the center of the circle and interpolated rotation angles about the center of the circle of the key frames**

# In[ ]:


def compose_circular_key_frames(thetas, X_WorldCenter, X_WorldGripper_init):
    """    
    returns: a list of RigidTransforms
    """
    ## this is an template, replace your code below
    key_frame_poses_in_world = [X_WorldGripper_init]
    for theta in thetas:
        this_pose = RigidTransform()
        key_frame_poses_in_world.append(this_pose)
        
    return key_frame_poses_in_world


# In[ ]:


# check key frames instead of interpolated trajectory
def visualize_key_frames(frame_poses):
    for i, pose in enumerate(frame_poses):
        painter.visualize_frame('frame_{}'.format(i), pose, length=0.05)
        
key_frame_poses = compose_circular_key_frames(thetas, X_WorldCenter, painter.get_X_WG())   
visualize_key_frames(key_frame_poses)


# ## Construct Trajectory
# 
# Now construct the trajectories to interpolate the positions and orientations of key frames using `PiecewisePose`. You might find it helpful to review the examples in the main chapter notebook.
# 

# In[ ]:


X_WorldGripper_init = painter.get_X_WG()
total_time = 20
key_frame_poses = compose_circular_key_frames(thetas, X_WorldCenter, X_WorldGripper_init)  
times = np.linspace(0, total_time, num_key_frames+1)
traj = PiecewisePose.MakeLinear(times, key_frame_poses)


# Now you should be able to visualize the execution of the circular painting. Use it to confirm that the gripper moves counterclockwise following the key frames previously drawn in the scene.

# In[ ]:


painter = IIWA_Painter(traj)
painter.paint(sim_duration=total_time)


# **Note that in this problem we have explicitly chosen to use the initial gripper pose as the start of the circular trajectory. Is this choice necessary to have the robot follow the desired circular path? Explain your answer and reasoning.**
# 
# Hints: 
# - Take a look at the constructor for the `IIWA_Painter` class a few cells above. Note the input/output variables of our pseudoinverse controller and the iiwa controller. Also, what's that integrator doing there?
# - You can test this using the code above by modifying the first pose of the trajectory and observing the result (just make sure to change your `compose_circular_key_frames` function to the final version you want before submitting to the grader!)

# ## Your Answer
# 
# Answer the question here, and copy-paste to the Gradescope 'written submission' section!

# **Note that the default amount of time we simulate forward (in the `paint()` method of the `IIWA_Painter`) matches the total time interval we specify for our trajectory (in `np.linspace()` a few cells above). What happens if you increase the simulation time while keeping the total time for the trajectory fixed? What is the cause of your expected/observed behavior?**

# ## Your Answer
# 
# Answer the question here, and copy-paste to the Gradescope 'written submission' section!

# 

# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do two things. 
# - Download and submit the notebook `robot_painter.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [4.0 pts] `compose_circular_key_frames` is correct according to the requirement
# - [3.0 pts] reasonable answer on the written question

# In[ ]:


from manipulation.exercises.pick.test_robot_painter import TestRobotPainter
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestRobotPainter], [locals()], 'results.json')
Grader.print_test_results('results.json')

