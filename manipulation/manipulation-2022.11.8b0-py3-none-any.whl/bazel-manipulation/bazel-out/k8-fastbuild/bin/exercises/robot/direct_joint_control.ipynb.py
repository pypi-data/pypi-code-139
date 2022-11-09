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

# # Drake practice - "Direct" Joint Angle Teleop
# First, we provide a reference to the first example notebook of chapter 1. Then, in the bottom cell, you will find a similar function with slightly different functionality, and code missing that you are required to fill in. Take a look below for further instructions!

# ## Review: 2D End-effector Teleop (from Chapter 1)
# 
# In the chapter 1 [example](https://manipulation.csail.mit.edu/intro.html#teleop2d), we assembled a diagram with the manipulation station, a meshcat visualizer, some systems that provide a minimal teleop interface, along with some systems to convert the teleop output from end-effector commands into joint commands.
# 
# In this problem, your goal is to **remove** some of these subsystems, and instead wire up the diagram to directly control the joint angles of the robot.
# 

# ## Setup
# Imports from drake and starting the Meshcat viewer.

# In[ ]:


import numpy as np
from pydrake.geometry import MeshcatVisualizer, StartMeshcat
from pydrake.systems.analysis import Simulator
from pydrake.systems.framework import DiagramBuilder

from manipulation import running_as_notebook
from manipulation.meshcat_utils import MeshcatPoseSliders
from manipulation.scenarios import MakeManipulationStation


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()

model_directives = """
directives:
- add_model:
    name: iiwa
    file: package://drake/manipulation/models/iiwa_description/urdf/planar_iiwa14_spheres_dense_elbow_collision.urdf
    default_joint_positions:
        iiwa_joint_2: [0.1]
        iiwa_joint_4: [-1.2]
        iiwa_joint_6: [1.6]
- add_weld:
    parent: world
    child: iiwa::iiwa_link_0
"""


# ## Directly control the robot joints
# You'll now get a chance to replace the teleop functionality in the 2D example above with a direct "joint angle setter". 
# 
# More specifically, we want you to complete the `teleop_2d_direct` function below, such that a user can directly pass in a desired angle of each joint and have the robot move to the commanded joint angles. You will have to make use of some drake functionality that's not used in the `teleop_2d` function (see [`FixValue`](https://drake.mit.edu/doxygen_cxx/classdrake_1_1systems_1_1_input_port.html#ab285168d3a19d8ed367e11053aec79c3) and [`CreateDefaultContext`](https://drake.mit.edu/doxygen_cxx/classdrake_1_1systems_1_1_system.html#ad047317ab91889c6743d5e47a64c7f08)) and you can leave out all the components that were used in `teleop_2d` which are no longer needed.
# 
# ### The goals of this exercise are twofold:
# - Understand the way core subsystems in Drake are wired together well enough to know which lines in the  `teleop_2d` function must be removed.
# - Use the information in the examples from the textbook, other exercises, and Drake documentation, to correctly implement the same high-level joint-space control behavior, but using a different Drake function. 
# 

# In[ ]:


def teleop_2d_direct(interactive=False, q_cmd=np.zeros(3)):
    """
    Joint position control of the Kuka iiwa robot, without using teleop sliders or differential IK.

    Args:
        interactive (bool): If True, function will query the user to manually set the desired joint positions
            while running the simulator. Otherwise, function will use "q_cmd" as the target joint position.
        q_cmd (np.ndarray): Shape (3,). Desired positions of the three movable joints on the 2D robot.
            "q_cmd" cannot be None if "interactive" is set to False.
    """
    assert (not interactive and q_cmd is not None) or interactive, 'Variable "q_cmd" must not be None if the function is run in non-interactive mode'

    builder = DiagramBuilder()

    time_step = 0.001
    station = builder.AddSystem(
        MakeManipulationStation(model_directives, time_step=time_step))

    # Add a meshcat visualizer.
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, station.GetOutputPort("query_object"), meshcat)
    meshcat.Set2dRenderMode(xmin=-0.25, xmax=1.5, ymin=-0.1, ymax=1.3)

    #######################################################################
    # Your code here 
    # (setup the diagram, simulation, and necessary contexts)

    diagram = None
    simulator = None
    context = None

    #######################################################################

    if simulator is None:
        print("You must set the simulator variable above")
        return station, context
        
    simulator.set_target_realtime_rate(1.0 if interactive else 0)
    meshcat.AddButton("Stop Simulation")
    while meshcat.GetButtonClicks("Stop Simulation") < 1:
        simulator.AdvanceTo(simulator.get_context().get_time() + 2.0)       

        #######################################################################
        # Your code here 
        # (read the current measured joint angles into the variable `q_current`)
        # (hint: what output ports does the `station` instance have available?)

        q_current = np.zeros(3)
        print(f'Current joint angles: {q_current}')            

        ####################################################################### 

        if interactive and running_as_notebook:
            j1_input = input(f'Please enter value for first movable joint (current value: {q_current[0]:.3f})')
            j2_input = input(f'Please enter value for second movable joint (current value: {q_current[1]:.3f})')
            j3_input = input(f'Please enter value for third movable joint (current value: {q_current[2]:.3f})') 
            j_inputs = [j1_input, j2_input, j3_input]
            q_cmd = q_current.copy()
            for j_idx, j_inp in enumerate(j_inputs):
                try:
                    j_val = float(j_inp)
                except Exception as e:
                    print(e)
                    print(f'Setting joint {j_idx} value to current joint value')
                    j_val = q_cmd[j_idx]
                q_cmd[j_idx] = j_val                      

        #######################################################################
        # Your code here 
        # (command the desired joint positions, and read the joint angle command into variable `q_current_cmd`)

        q_current_cmd = np.zeros(3)
        print(f'Current commanded joint angles: {q_current_cmd}\n')

        #######################################################################  

        if not interactive or not running_as_notebook:
            break
            
    meshcat.DeleteButton("Stop Simulation")
        
    return station, context


# Run the cell below to use the function you wrote in an interactive mode, but note that the autograder will test the functionality of your code in non-interactive mode.

# In[ ]:


teleop_2d_direct(interactive=True)


# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do as follows:. 
# - Download and submit the notebook `direct_joint_control.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [5pts] `teleop_2d_direct` must be implemented correctly (i.e., we will check if you are properly sending position commands to the robot)
# 
# Below is our autograder where you can check your score!

# In[ ]:


from manipulation.exercises.grader import Grader
from manipulation.exercises.robot.test_direct_joint_control import     TestDirectJointControl

Grader.grade_output([TestDirectJointControl], [locals()], 'results.json')
Grader.print_test_results('results.json')

