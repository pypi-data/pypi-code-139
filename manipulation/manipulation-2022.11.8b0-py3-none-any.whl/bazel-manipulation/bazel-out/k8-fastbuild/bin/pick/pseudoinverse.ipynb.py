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


import numpy as np
from pydrake.all import (DiagramBuilder, Integrator, JacobianWrtVariable,
                         LeafSystem, MeshcatVisualizer, Simulator,
                         StartMeshcat)

from manipulation import FindResource, running_as_notebook
from manipulation.scenarios import MakeManipulationStation


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


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

    visualizer.StartRecording(False)
    simulator.AdvanceTo(5.0 if running_as_notebook else 0.1);
    visualizer.PublishRecording()

jacobian_controller_example()


# In[ ]:




