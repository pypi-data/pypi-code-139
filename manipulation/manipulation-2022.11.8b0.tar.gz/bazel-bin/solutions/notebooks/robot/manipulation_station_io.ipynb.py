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

# # **Input and Output Ports of the Manipulation Station**
# 

# In[ ]:


import numpy as np
from IPython.display import HTML
from manipulation import FindResource
from manipulation.scenarios import MakeManipulationStation
from pydrake.all import StartMeshcat
from pydrake.geometry import MeshcatVisualizer
from pydrake.systems.analysis import Simulator
from pydrake.systems.framework import DiagramBuilder, GenerateHtml


# In[ ]:


meshcat = StartMeshcat()


# ## Access System Input/Output Values
# In this exercise, you will explore the [ManipulationStation](http://manipulation.mit.edu/robot.html#manipulation_station) that was mentioned during the lecture. You should recall that the orange ports are the ones that do not exist for the actual hardware platform.
# 
# <html>
# <table align="center" cellpadding="0" cellspacing="0"><tbody><tr align="center"><td style="vertical-align:middle"><table cellspacing="0" cellpadding="0"><tbody><tr><td align="right" style="padding:5px 0px 5px 0px">iiwa_position→</td></tr><tr><td align="right" style="padding:5px 0px 5px 0px">iiwa_feedforward_torque (optional)→</td></tr><tr><td align="right" style="padding:5px 0px 5px 0px">wsg_position→</td></tr><tr><td align="right" style="padding:5px 0px 5px 0px">wsg_force_limit (optional)→</td></tr></tbody></table></td><td align="center" style="border:solid;padding-left:20px;padding-right:20px;vertical-align:middle" bgcolor="#F0F0F0"><a href="https://github.com/RussTedrake/manipulation/blob/ceb817b527cbf1826c5b9a573ffbef415cb0f013/manipulation/scenarios.py#L453">ManipulationStation</a></td><td style="vertical-align:middle"><table cellspacing="0" cellpadding="0"><tbody><tr><td align="left" style="padding:5px 0px 5px 0px">→ iiwa_position_commanded</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ iiwa_position_measured</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ iiwa_velocity_estimated</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ iiwa_state_estimated</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ iiwa_torque_commanded</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ iiwa_torque_measured</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ iiwa_torque_external</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ wsg_state_measured</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ wsg_force_measured</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ camera_[NAME]_rgb_image</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ camera_[NAME]_depth_image</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ <b style="color:orange">camera_[NAME]_label_image</b></td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ ...</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ camera_[NAME]_rgb_image</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ camera_[NAME]_depth_image</td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ <b style="color:orange">camera_[NAME]_label_image</b></td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ <b style="color:orange">query_object</b></td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ <b style="color:orange">contact_results</b></td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ <b style="color:orange">plant_continuous_state</b></td></tr><tr><td align="left" style="padding:5px 0px 5px 0px">→ <b style="color:orange">body_poses</b></td></tr></tbody></table></td></tr></tbody></table>
# </html>
# 
# Now we construct a ManipulationStation object and finalize the system setting. To get a sense of what this manipulation station looks like, you can open the meshcat viewer from the generated link as usual. There should be a bookshelf and a Kuka arm with a gripper attached (it might take a few seconds to load).

# In[ ]:


station = MakeManipulationStation(
    filename=FindResource("models/clutter.dmd.yaml"))
plant = station.GetSubsystemByName("plant")

builder = DiagramBuilder()
builder.AddSystem(station)
MeshcatVisualizer.AddToBuilder(
      builder, station.GetOutputPort("query_object"), meshcat)
diagram = builder.Build()
simulator = Simulator(diagram)
simulator.Initialize()


# [**Context**](https://drake.mit.edu/pydrake/pydrake.systems.framework.html?highlight=context#pydrake.systems.framework.Context_) is an abstract class template that represents all the typed values that are used in a System’s computations: time, numeric-valued input ports, numerical state, and numerical parameters. There are also type-erased abstract state variables, abstract-valued input ports, abstract parameters, and a double accuracy setting. It is important to note that a **Context** is designed to be used only with the System that created it. State and Parameter data can be copied between contexts for compatible systems as necessary. One of the most common mistakes is to pass the wrong context. Although most methods in drake should throw an error if you pass a context from the wrong system, but not all of them do yet. 
# 
# In the cell below, we first create a root context from the diagram, and then we retrieve the contexts of the subsystems from the root context.

# In[ ]:


# initialize context
context = diagram.CreateDefaultContext()
plant_context = plant.GetMyContextFromRoot(context)
station_context = station.GetMyContextFromRoot(context)


# In this exercise, you will familiarize yourself with the input and output mechanism from the manipulation station system. Remember you can always generate a schematic view of your system by running the cell below. By clicking the "+" sign on the manipulation_station, you can get a more detailed view of the diverse modules within the manipulation station. (You might need to run the cell twice to see the diagram)

# In[ ]:


diagram.set_name("diagram")
HTML('<script src="https://unpkg.com/gojs/release/go.js"></script>' + GenerateHtml(diagram))


# Now if we set the joint position of the Kuka arm, we should expect to get the same values from the iiwa_position_measured port, which can be found from the output ports of **manipulation_station** object. Below we demonstrate how this can be done using **drake**'s syntax. You may also find it useful to review the **system** class documentation [here](https://drake.mit.edu/pydrake/pydrake.systems.framework.html?highlight=output_port#pydrake.systems.framework.System_).

# In[ ]:


# provide initial states
q0 = np.array([-1.57, 0.1, 0, -1.2, 0, 1.6, 0])
iiwa = plant.GetModelInstanceByName("iiwa")
# set the joint positions of the kuka arm
plant.SetPositions(plant_context, iiwa, q0)
# examine the output port
station.GetOutputPort("iiwa_position_measured").Eval(station_context)


# Note that the [output port](https://drake.mit.edu/pydrake/pydrake.systems.framework.html?highlight=outputport#pydrake.systems.framework.OutputPort) named "iiwa_position_measured" is first retrieved from the station and then evaluated using **Eval** method. This is a very common approach to read the values of a selected output port.
# 
# Alternatively, you may retrieve the joint angles from the **plant**, which is a subsystem of the manipulation station.

# In[ ]:


joint_angles = []
for i in range(1, 8):
    joint_angles.append(
        plant.GetJointByName(
            'iiwa_joint_{}'.format(i)).get_angle(plant_context))

# alternatively, use GetPositions to obtain the generalized positions
# from the plant context
q_general = plant.GetPositions(plant_context, iiwa)

print(joint_angles)
print(q_general)


# # Exercise a: Code Submission
# Now, it's your time to code! Use **GetOutputPort** and **Eval** to retrieve the joint velocities from the "iiwa_velocity_estimated" output port. Note that we have set the velocities for you. 

# In[ ]:


plant.SetVelocities(plant_context, iiwa, np.zeros(7,))


# Below, `get_velocity(station, station_context)` is the function you must modify to query values from "iiwa_velocity_estimated".

# In[ ]:


def get_velocity(station, station_context):
    """
    fill in your code in this method
    """
    velocity_estimated = None
    return velocity_estimated


# In[ ]:


def get_velocity(station, station_context):
    velocity_estimated = station.GetOutputPort("iiwa_velocity_estimated").Eval(
        station_context)
    return velocity_estimated


# You can check if you got the implementation correct by running the below autograder.

# In[ ]:


from manipulation.exercises.robot.test_manipulation_io import TestManipulationIO
from manipulation.exercises.grader import Grader

Grader.grade_output([TestManipulationIO], [locals()], 'results.json')
Grader.print_test_results('results.json')


# Please note that the *iiwa_position_commanded* and the *iiwa position* are NOT the same variable. The *iiwa_position_commanded* are the commanded positions sent to the robot, whereas the *iiwa_positions* are the current positions of the simulated robot. We also expect to have different values for the feedforward torque (system input) and the commanded torque (system output). Next, you will investigate why. First, let us provide a zero feedforward torque to the "iiwa_feedforward_torque" port.

# In[ ]:


station.GetInputPort("iiwa_feedforward_torque").FixValue(
    station_context, np.zeros(7,))
tau_no_ff = station.GetOutputPort("iiwa_torque_commanded").Eval(station_context)
print('feedforward torque: {}'.format(np.zeros(7,)))
print('commanded torque with no feedforward torque:{}'.format(tau_no_ff))


# Now try the same experiment with a non-zero feedforward torque as shown below.

# In[ ]:


tau_ff = np.linspace(3.1, 3.7, 7)
print('feedforward torque: {}'.format(tau_ff))
station.GetInputPort("iiwa_feedforward_torque").FixValue(
    station_context, tau_ff)
torque_commanded = station.GetOutputPort("iiwa_torque_commanded").Eval(
    station_context)
print('the commanded torque: {}'.format(torque_commanded))


# # Exercise b: Written Problem.
# Below, we have a question for you.
# 
# **In this exercise, please explain what causes the discrepancy between the feedforward torque and the commanded torque.**
# 
# HINT: can you find any relationship among *tau_ff*, *tau_no_ff*, *torque_commanded*?

# ## Your Answer
# 
# Answer the Question here, and copy-paste to the Gradescope 'written submission' section!
# 

# ## Solution
# 
# The discrepancy between the output torque torque_commanded and the input feedforward torque is caused by the internal controller. You may find that in this case, torque_commanded = tau_ff + tau_no_ff. That is, the commanded torque is the sum of the torque when the feedforward torque is zero and the non-zero feedfoward torque supplied to the system. The internal controller is needed to compensate for gravity.

# ## How will this notebook be graded?

# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [5pts] `get_velocity` must be implemented correctly. 
# - [5pts] You must answer correctly why there is a difference between feed-forward torque and commanded torque. 

# ## Additional Note.

# So far we have not looked into the outputs of simulated camera sensors. Fortunately, accessing the camera data can be done in an almost exactly the same way as we have shown above. We will get to it soon! 
