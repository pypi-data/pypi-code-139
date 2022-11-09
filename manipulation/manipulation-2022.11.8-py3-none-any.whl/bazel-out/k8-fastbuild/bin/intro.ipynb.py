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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/intro.html).  I recommend having both windows open, side-by-side!
# 
# ## Instructions for running this notebook on Deepnote
# 
# - Log in (the free account will be sufficient for this class)
# - "Duplicate" the document.  Icon is in the top right next to Login. 
# - Read/run the cells one at a time OR use the "Run notebook" icon just above this cell
# - To open the visualizer, click on the url printed just below "StartMeshcat" in the second code cell of the notebook.
# - To teleop, use the keyboard commands printed in the third/fourth code cell outputs OR in meshcat, click "Open controls" and use the sliders.
# - When you're done, press the ESCAPE key OR click the "Stop Simulation" button in meshcat.

# In[ ]:


import logging
import numpy as np
from pydrake.geometry import MeshcatVisualizer, StartMeshcat
from pydrake.math import RigidTransform, RotationMatrix
from pydrake.systems.analysis import Simulator
from pydrake.systems.framework import DiagramBuilder

from manipulation import running_as_notebook
from manipulation.meshcat_utils import MeshcatPoseSliders, WsgButton
from manipulation.scenarios import (AddIiwaDifferentialIK,
                                    MakeManipulationStation)


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Teleop Example (2D)
# 
# In this example, we assemble a diagram with all of the relevant subsystems (the manipulation station, the meshcat visualizer, and some systems that provide a minimal teleop interface and convert the teleop output from end-effector commands into joint commands.  We'll learn more about each of these components in the following chapters.
# 
# **NOTE:** If you command the robot to move its gripper beyond what is possible, then you get a message about "differential IK" failing.  I've left that in for now (rather than setting very conservative slider limits) partly because it has tutorial value.  We'll understand it more precisely soon!  For now, just stop the simulation and rerun the cell if you get stuck.
# 

# In[ ]:


# TODO(russt): Add planar joint to brick
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
- add_model:
    name: wsg
    file: package://drake/manipulation/models/wsg_50_description/sdf/schunk_wsg_50_with_tip.sdf
- add_weld:
    parent: iiwa::iiwa_link_7
    child: wsg::body
    X_PC:
        translation: [0, 0, 0.09]
        rotation: !Rpy { deg: [90, 0, 90]}
- add_model:
    name: foam_brick
    file: package://drake/examples/manipulation_station/models/061_foam_brick.sdf
    default_free_body_pose:
        base_link:
            translation: [0.6, 0, 0]
- add_model:
    name: robot_table
    file: package://drake/examples/kuka_iiwa_arm/models/table/extra_heavy_duty_table_surface_only_collision.sdf
- add_weld:
    parent: world
    child: robot_table::link
    X_PC:
        translation: [0, 0, -0.7645]
- add_model:
    name: work_table
    file: package://drake/examples/kuka_iiwa_arm/models/table/extra_heavy_duty_table_surface_only_collision.sdf
- add_weld:
    parent: world
    child: work_table::link
    X_PC:
        translation: [0.75, 0, -0.7645]
"""

def teleop_2d():
    builder = DiagramBuilder()

    time_step = 0.001
    station = builder.AddSystem(
        MakeManipulationStation(model_directives, time_step=time_step))
    plant = station.GetSubsystemByName("plant")
    controller_plant = station.GetSubsystemByName(
        "iiwa_controller").get_multibody_plant()

    # Add a meshcat visualizer.
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, station.GetOutputPort("query_object"), meshcat)
    meshcat.Set2dRenderMode(xmin=-0.25, xmax=1.5, ymin=-0.1, ymax=1.3)
    meshcat.DeleteAddedControls()

    # Set up differential inverse kinematics.
    differential_ik = AddIiwaDifferentialIK(
        builder,
        controller_plant,
        frame=controller_plant.GetFrameByName("iiwa_link_7"))
    builder.Connect(differential_ik.get_output_port(),
                    station.GetInputPort("iiwa_position"))
    builder.Connect(station.GetOutputPort("iiwa_state_estimated"),
                    differential_ik.GetInputPort("robot_state"))

    # Set up teleop widgets.
    teleop = builder.AddSystem(
        MeshcatPoseSliders(
            meshcat,
            min_range=MeshcatPoseSliders.MinRange(roll=0, x=-0.6, z=0.0),
            max_range=MeshcatPoseSliders.MaxRange(roll=2 * np.pi, x=0.8, z=1.1),
            value=MeshcatPoseSliders.Value(pitch=0, yaw=np.pi / 2, y=0),
            visible=MeshcatPoseSliders.Visible(pitch=False, yaw=False, y=False),
            decrement_keycode=MeshcatPoseSliders.DecrementKey(x="ArrowLeft",
                                                              z="ArrowDown",
                                                              roll="KeyA"),
            increment_keycode=MeshcatPoseSliders.IncrementKey(x="ArrowRight",
                                                              z="ArrowUp",
                                                              roll="KeyD"),
            body_index=plant.GetBodyByName("iiwa_link_7").index()))
    builder.Connect(teleop.get_output_port(0),
                    differential_ik.get_input_port(0))
    builder.Connect(station.GetOutputPort("body_poses"),
                    teleop.GetInputPort("body_poses"))
    wsg_teleop = builder.AddSystem(WsgButton(meshcat))
    builder.Connect(wsg_teleop.get_output_port(0),
                    station.GetInputPort("wsg_position"))

    # Simulate.
    diagram = builder.Build()
    simulator = Simulator(diagram)

    if running_as_notebook:  # Then we're not just running as a test on CI.
        simulator.set_target_realtime_rate(1.0)
        meshcat.AddButton("Stop Simulation", "Escape")
        print("Press Escape to stop the simulation")
        while meshcat.GetButtonClicks("Stop Simulation") < 1:
            simulator.AdvanceTo(simulator.get_context().get_time() + 2.0)
        meshcat.DeleteButton("Stop Simulation")
    else:
        simulator.AdvanceTo(0.1)

teleop_2d()


# # Teleop Example (3D)
# 
# The physics and geometry engines running in the simulation above are actually running in 3D.  This example is almost identical, but we'll use the (default) 3D visualization and add more sliders for controlling the full `roll`, `pitch`, `yaw` angles and `x`, `y`, `z` positions of the end effector.

# In[ ]:


model_directives = """
directives:
- add_directives:
    file: package://manipulation/clutter.dmd.yaml
- add_model:
    name: foam_brick
    file: package://drake/examples/manipulation_station/models/061_foam_brick.sdf
    default_free_body_pose:
        base_link:
            translation: [0, -0.6, 0.2]
"""


def teleop_3d():
    builder = DiagramBuilder()

    time_step = 0.001
    station = builder.AddSystem(
        MakeManipulationStation(model_directives, time_step=time_step))
    plant = station.GetSubsystemByName("plant")
    controller_plant = station.GetSubsystemByName(
        "iiwa_controller").get_multibody_plant()

    # Add a meshcat visualizer.
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, station.GetOutputPort("query_object"), meshcat)
    meshcat.ResetRenderMode()
    meshcat.DeleteAddedControls()

    # Set up differential inverse kinematics.
    differential_ik = AddIiwaDifferentialIK(
        builder,
        controller_plant,
        frame=controller_plant.GetFrameByName("iiwa_link_7"))
    builder.Connect(differential_ik.get_output_port(),
                    station.GetInputPort("iiwa_position"))
    builder.Connect(station.GetOutputPort("iiwa_state_estimated"),
                    differential_ik.GetInputPort("robot_state"))

    # Set up teleop widgets.
    teleop = builder.AddSystem(
        MeshcatPoseSliders(
            meshcat,
            min_range=MeshcatPoseSliders.MinRange(roll=0,
                                                  pitch=-0.5,
                                                  yaw=-np.pi,
                                                  x=-0.6,
                                                  y=-0.8,
                                                  z=0.0),
            max_range=MeshcatPoseSliders.MaxRange(roll=2 * np.pi,
                                                  pitch=np.pi,
                                                  yaw=np.pi,
                                                  x=0.8,
                                                  y=0.3,
                                                  z=1.1),
            body_index=plant.GetBodyByName("iiwa_link_7").index()))
    builder.Connect(teleop.get_output_port(0),
                    differential_ik.get_input_port(0))
    builder.Connect(station.GetOutputPort("body_poses"),
                    teleop.GetInputPort("body_poses"))
    wsg_teleop = builder.AddSystem(WsgButton(meshcat))
    builder.Connect(wsg_teleop.get_output_port(0),
                    station.GetInputPort("wsg_position"))

    diagram = builder.Build()
    simulator = Simulator(diagram)
    context = simulator.get_mutable_context()

    if running_as_notebook:  # Then we're not just running as a test on CI.
        simulator.set_target_realtime_rate(1.0)

        meshcat.AddButton("Stop Simulation", "Escape")
        print("Press Escape to stop the simulation")
        while meshcat.GetButtonClicks("Stop Simulation") < 1:
            simulator.AdvanceTo(simulator.get_context().get_time() + 2.0)
        meshcat.DeleteButton("Stop Simulation")

    else:
        simulator.AdvanceTo(0.1)


teleop_3d()


# In[ ]:




