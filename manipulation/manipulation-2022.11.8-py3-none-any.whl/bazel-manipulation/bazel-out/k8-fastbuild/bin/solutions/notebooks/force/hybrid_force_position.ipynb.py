from manipulation.exercises.grader import set_grader_throws
set_grader_throws(True)

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

# ## **Hybrid Force Position Control**

# In[ ]:


import matplotlib.pyplot as plt
import mpld3
import numpy as np
from IPython.display import HTML, display
from manipulation import running_as_notebook
from pydrake.all import (Box, ConnectPlanarSceneGraphVisualizer,
                         CoulombFriction, DiagramBuilder, JacobianWrtVariable,
                         LeafSystem, RigidTransform, RollPitchYaw, Simulator,
                         SpatialInertia, UnitInertia, VectorLogSink)
from pydrake.examples.manipulation_station import ManipulationStation

if running_as_notebook:
    mpld3.enable_notebook()


class TorqueController(LeafSystem):
    """Wrapper System for Commanding Pure Torques to planar iiwa.
    @param plant MultibodyPlant of the simulated plant.
    @param ctrl_fun function object to implement torque control law.
    @param vx Velocity towards the linear direction. 
    """
    def __init__(self, plant, ctrl_fun, vx):
        LeafSystem.__init__(self)
        self._plant = plant
        self._plant_context = plant.CreateDefaultContext()
        self._iiwa = plant.GetModelInstanceByName("iiwa")
        self._G = plant.GetBodyByName("body").body_frame()
        self._W = plant.world_frame()
        self._ctrl_fun = ctrl_fun
        self._vx = vx
        self._joint_indices = [
            plant.GetJointByName(j).position_start()
            for j in ("iiwa_joint_2", "iiwa_joint_4", "iiwa_joint_6")
        ]

        self.DeclareVectorInputPort("iiwa_position_measured", 3)
        self.DeclareVectorInputPort("iiwa_velocity_measured", 3)

        # If we want, we can add this in to do closed-loop force control on z.
        #self.DeclareVectorInputPort("iiwa_torque_external", 3)

        self.DeclareVectorOutputPort("iiwa_position_command", 3,
                                     self.CalcPositionOutput)
        self.DeclareVectorOutputPort("iiwa_torque_cmd", 3,
                                     self.CalcTorqueOutput)
        # Compute foward kinematics so we can log the wsg position for grading.
        self.DeclareVectorOutputPort("wsg_position", 3,
                                     self.CalcWsgPositionOutput)

    def CalcPositionOutput(self, context, output):
        """Set q_d = q_now. This ensures the iiwa goes into pure torque mode in sim by setting the position control torques in InverseDynamicsController to zero. 
        NOTE(terry-suh): Do not use this method on hardware or deploy this notebook on hardware. 
        We can only simulate pure torque control mode for iiwa on sim. 
        """
        q_now = self.get_input_port(0).Eval(context)
        output.SetFromVector(q_now)

    def CalcTorqueOutput(self, context, output):
        # Hard-coded position and force profiles. Can be connected from Trajectory class.
        if (context.get_time() < 2.0):
            px_des = 0.65
        else:
            px_des = 0.65 + self._vx * (context.get_time() - 2.0)

        fz_des = 10

        # Read inputs
        q_now = self.get_input_port(0).Eval(context)
        v_now = self.get_input_port(1).Eval(context)
        #tau_now = self.get_input_port(2).Eval(context)

        self._plant.SetPositions(self._plant_context, self._iiwa, q_now)

        # 1. Convert joint space quantities to Cartesian quantities.
        X_now = self._plant.CalcRelativeTransform(self._plant_context, self._W,
                                                  self._G)

        rpy_now = RollPitchYaw(X_now.rotation()).vector()
        p_xyz_now = X_now.translation()

        J_G = self._plant.CalcJacobianSpatialVelocity(
            self._plant_context, JacobianWrtVariable.kQDot,
            self._G, [0,0,0], self._W, self._W)

        # Only select relevant terms. We end up with J_G of shape (3,3).
        # Rows correspond to (pitch, x, z).
        # Columns correspond to (q0, q1, q2).
        J_G = J_G[np.ix_([1,3,5],self._joint_indices)]
        v_pxz_now = J_G.dot(v_now)

        p_pxz_now = np.array([rpy_now[1], p_xyz_now[0], p_xyz_now[2]])

        # 2. Apply ctrl_fun
        F_pxz = self._ctrl_fun(p_pxz_now, v_pxz_now, px_des, fz_des)

        # 3. Convert back to joint coordinates
        tau_cmd = J_G.T.dot(F_pxz)
        output.SetFromVector(tau_cmd)

    def CalcWsgPositionOutput(self, context, output):
        """
        Compute Forward kinematics. Needed to log the position trajectory for grading.  TODO(russt): Could use MultibodyPlant's body_poses output port for this.
        """
        q_now = self.get_input_port(0).Eval(context)
        self._plant.SetPositions(self._plant_context, self._iiwa, q_now)
        X_now = self._plant.CalcRelativeTransform(self._plant_context, self._W,
                                                  self._G)

        rpy_now = RollPitchYaw(X_now.rotation()).vector()
        p_xyz_now = X_now.translation()
        p_pxz_now = np.array([rpy_now[1], p_xyz_now[0], p_xyz_now[2]])

        output.SetFromVector(p_pxz_now)

def AddBook(plant):
    mu = 10.0
    book = plant.AddModelInstance("book")
    book_body = plant.AddRigidBody("book_body", book,
                                   SpatialInertia(
                                       mass = 0.2,
                                       p_PScm_E=np.array([0., 0., 0.]),
                                       G_SP_E = UnitInertia(1.0, 1.0, 1.0)))
    shape = Box(0.3, 0.1, 0.05)
    if plant.geometry_source_is_registered():
        plant.RegisterCollisionGeometry(book_body, RigidTransform(), shape, "book_body", CoulombFriction(mu, mu))
        plant.RegisterVisualGeometry(book_body, RigidTransform(), shape, "book_body", [.9, .2, .2, 1.0])

    return book

def BuildAndSimulate(ctrl_fun, velocity, duration):
    builder = DiagramBuilder()

    # Add ManipulationStation
    station = builder.AddSystem(ManipulationStation(time_step = 5e-4))
    station.SetupPlanarIiwaStation()
    book = AddBook(station.get_mutable_multibody_plant())

    station.Finalize()

    controller = builder.AddSystem(
        TorqueController(station.get_multibody_plant(), ctrl_fun, velocity))

    logger = builder.AddSystem(VectorLogSink(3))

    builder.Connect(controller.get_output_port(0),
                    station.GetInputPort("iiwa_position"))
    builder.Connect(controller.get_output_port(1),
                    station.GetInputPort("iiwa_feedforward_torque"))
    builder.Connect(controller.get_output_port(2),
                    logger.get_input_port(0))

    builder.Connect(station.GetOutputPort("iiwa_position_measured"),
                    controller.get_input_port(0))
    builder.Connect(station.GetOutputPort("iiwa_velocity_estimated"),
                    controller.get_input_port(1))

    if running_as_notebook:
        vis = ConnectPlanarSceneGraphVisualizer(
            builder,
            station.get_scene_graph(),
            output_port=station.GetOutputPort("query_object"),
            xlim=[-0.5, 1.2],
            ylim=[-0.8, 2],
            show=False)

    diagram = builder.Build()

    # Initialize default positions for plant.
    plant = station.get_mutable_multibody_plant()
    simulator = Simulator(diagram)
    plant_context = plant.GetMyContextFromRoot(simulator.get_mutable_context())
    plant.SetFreeBodyPose(plant_context, plant.GetBodyByName("book_body"),
                          RigidTransform([0.65, 0.0, 0.03
                                         ]))  # limit is between 0.5 and 0.55
    plant.SetPositions(plant_context,
                       plant.GetModelInstanceByName("iiwa"),
                       np.array([np.pi/4, -np.pi/3, np.pi/3]))

    station_context = station.GetMyContextFromRoot(
        simulator.get_mutable_context())
    station.GetInputPort("wsg_position").FixValue(station_context, [0.02])

    if running_as_notebook:
        vis.start_recording()
        simulator.AdvanceTo(duration)
        vis.stop_recording()

        ani = vis.get_recording_as_animation(repeat=False)
        display(HTML(ani.to_jshtml()))

    else:
        # TODO(terry-suh): we need to simulate this fully to grade student's answers, but CI won't be happy.
        simulator.AdvanceTo(duration)

    pose = plant.GetFreeBodyPose(plant_context,
                                 plant.GetBodyByName("book_body"))

    # Return these so that we can check the pose of each object.
    return logger.FindLog(simulator.get_context()), plant, plant_context


# # Book Dragging
# 
# In the lecture, we've written a controller that does non-prehensile manipulation by flipping a cheez-it box using external contacts. In this example, we will examine another example of non-prehensile manipulation that relies on pushing with friction. 
# 
# We have seen a wonderful example of non-prehensile manipulation on this example during lecture: 
# 
# [![Jiaji_book_pushing](http://img.youtube.com/vi/PngdQGEUi7w/0.jpg)](http://www.youtube.com/watch?v=PngdQGEUi7w "Video Title")
# 
# 
# Throughout this notebook, we will implement a hybrid force-position controller to achieve this dragging motion. 
# 

# # Analysis of Frictional Forces
# 
# Let's take some time to first think about the physics of what is going on. What causes the book to move when we drag it with some downwards force? This particular example is interesting because how much we rely on friction. If we were to draw a rough diagram of forces, we would end up with the below figure. Note that we've summarized the interaction forces with the book and the ground with a point contact model, but the story can be more complicated.  
# 
# <img src="https://raw.githubusercontent.com/RussTedrake/manipulation/master/figures/exercises/friction.png" width="700">
# 
# In class we saw the Coulomb model of friction, where the frictional forces must lie inside the friction cone that relates the normal force:
# $$|f_x| \leq \mu f_z$$
# 
# where $\mu$ is the static coefficient of friction. 
# 
# **Problem 9.3.a** [3pts]: Under the Coloumb friction model, write down the conditions for the ratio of friction coefficients $\mu^C/\mu^A$ that enables us to drag the book, as a function of $m,g$, and $f^{book_C}_{gripper,C_z}$ (HINT: don't forget about gravity!)  
# 

# **Solution**: For us to generate any movement, it must be the case that
# 
# $$f^{book_C}_{gripper,C_x} \geq f^{book_A}_{table,A_x}$$
# 
# Now we can write this in the boundary of the friction cone, where we have 
# 
# $$\mu^C f^{book_C}_{gripper,C_z} \geq \mu^A f^{book_A}_{table,A_z}$$
# 
# First write down the relation between $f^{book_C}_{gripper,C_z}$ and $f^{book_A}_{table,A_z}$ by doing force balance on the book. 
# 
# $$f^{book_C}_{gripper,C_z}+mg=f^{book_A}_{table,A_z}$$
# 
# So the coefficients must satisfy 
# $$ \mu^C f^{book_C}_{gripper,C_z} \geq \mu^A (f^{book_C}_{gripper,C_z} + mg)$$
# 
# re-arranging, we have 
# 
# $$ \frac{\mu^C}{\mu^A} \geq 1 + \frac{mg}{f^{book_C}_{gripper,C_z}}$$
# 
# When gravity is negligible compared to the normal force, it comes down to a simple comparison between the friction coefficients. 
# 
# 

# **Problem 9.3.b** [1pts] Based on the answer to 9.3.a, do you agree with the following statement? 
# 
# **Using a smoother surface on the gripper (lower $\mu^C$) will make this motion more feasible.**
# 
# Why or why not? 
# 
# **Problem 9.3.c** [1pts] Based on the answer to 9.3.a, do you agree with the following statement? 
# 
# **Pressing down harder (higher $f^{book_C}_{gripper,C_z}$) will make this motion more feasible**. 
# 
# Why or why not?

# **Solution**: We can increase $\mu^C$ by using more frictional material. We should be pushing the book as hard as possible (try it yourself! the book won't move for low $N_1$ at all.) 

# # Hybrid Force-Position Control 
# 
# How should we write this type of a controller? We know how to do position control, and we know how to do force control, and we know it's hard to do both. But this task seems to require both. Namely, 
# 
# - We want to achieve desired position along the x-direction. 
# - We want to achieve desired force along the z-direction. 
# 
# The key idea of hybrid force/position control is that when the force-controlled directions and the position-controlled directions are orthonormal, it is possible to control both in different directions! 
# 
# NOTE: We will do an axis-aligned version of orthonormal forces here, but with a bit more math, the rich theory of linear algebra allows us to generalize to arbitrary orthonormal planes as well. 

# #### **Problem 9.3.d** [4pts] Below, you will write a function `compute_ctrl` that implements a feedback policy which computes spatial forces $u=[\tau_y,f_x,f_z]$ upon given current and desired position along the $x,\theta_y$ direction, while achieving desired forces along the $z$ direction. 
# 
# You can implement each direction independently as follows:
# - Implement a PD controller in x-direction which drives `x_now` to `x_des`. You are free to set and tune the gains. 
# - Implement a PD controller in $\theta_y$-direction which drives `theta_now` to 0. 
# - Implement an open-loop force controller in the $z$-direction which applies forces along the z-direction, such that `f_des` is the force applied on the book. 
# 
# NOTE: If we had a point finger, we wouldn't have had to regulate `theta_now` at all - but why was this necessary for the rigid-body gripper? After implementing everything, try setting only tau_y (`u[0]`) to zero and see what happens! 

# In[ ]:


def compute_ctrl(p_pxz_now, v_pxz_now, x_des, f_des):
  """Compute control action given current position and velocities, as well as 
  desired x-direction position p_des(t) / desired z-direction force f_des. 
  You may set theta_des yourself, though we recommend regulating it to zero. 
  Input:
    - p_pxz_now: np.array (dim 3), position of the finger. [thetay, px, pz] 
    - v_pxz_now: np.array (dim 3), velocity of the finger. [wy, vx, vz] 
    - x_des: float, desired position of the finger along the x-direction. 
    - f_des: float, desired force on the book along the z-direction. 
  Output:
    - u    : np.array (dim 3), spatial torques to send to the manipulator. [tau_y, fx, fz] 
  """

  u = np.zeros(3)
  return u


# You can run the below cell to check your implementation. Using your controller, we will be tracking a linear position trajectory in the $x$-direction specified as:
# 
# `x_des(t) = 0.65 + velocity * max(t - 2.0, 0.0)`
# 
# In the below cell, you are free to set the velocity, and the $t_f$ (the end time of the trajectory). For grading, we will be checking for the following:
# 
# - At the end of the time, the left edge of the book lies between the gap of the two tables. 
# - At each timestep, the gripper fingers stays above the book. (we specifically want you to drag the book, so pushing it from the side is not allowed).  

# In[ ]:


# NOTE: you may tune the velocity and duration to achieve the above specification. 
velocity = -0.125  # p_des = 0.65 + velocity * max\{time - 2.0, 0\}
duration = 0.1     # duration to simulate. We check the book pose at the end of duration. set to 5~10.
log, plant, plant_context = BuildAndSimulate(compute_ctrl, velocity, duration)


# In[ ]:


def compute_ctrl(p_pxz_now, v_pxz_now, x_des, f_des):
  """Compute control action given current position and velocities, as well as 
  desired x-direction position p_des(t) / desired z-direction force f_des. 
  You may set theta_des yourself, though we recommend regulating it to zero. 
  Input:
    - p_pxz_now: np.array (dim 3), position of the finger. [thetay, px, pz] 
    - v_pxz_now: np.array (dim 3), velocity of the finger. [wy, vx, vz] 
    - x_des: float, desired position of the finger along the x-direction. 
    - f_des: float, desired force on the book along the z-direction. 
  Output:
    - u    : np.array (dim 3), spatial torques to send to the manipulator. [tau_y, fx, fz] 
  """

  kp_x = 50.      
  kd_x = 15.      
  kp_p = 20.
  kd_p = 5. 

  u = np.zeros(3)
  u[0] = -kp_p * p_pxz_now[0] - kd_p * v_pxz_now[0]
  u[1] = -kp_x * (p_pxz_now[1] - x_des) -kd_x * v_pxz_now[1] 
  u[2] = -f_des

  return u

velocity = -0.125  # p_des = 0.65 + velocity * max\{time - 2.0, 0\}
duration = 6.1
log, plant, plant_context = BuildAndSimulate(compute_ctrl, velocity, duration)


# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do two things. 
# - Download and submit the notebook `hybrid_force_position.ipynb` to Gradescope.
# - Write down your answers to 9.3.a, 9.3.b, and 9.3.c in your PDF submission to Gradescope. 
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [3 pts] 9.3.a is answered correctly.
# - [1 pts] 9.3.b is answered correctly. 
# - [1 pts] 9.3.c is answered correctly.
# - [4 pts] `compute_ctrl` must be implemented correctly.
# 

# In[ ]:


from manipulation.exercises.force.test_hybrid import TestHybrid
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestHybrid], [locals()], 'results.json')
Grader.print_test_results('results.json')


# In[ ]:




