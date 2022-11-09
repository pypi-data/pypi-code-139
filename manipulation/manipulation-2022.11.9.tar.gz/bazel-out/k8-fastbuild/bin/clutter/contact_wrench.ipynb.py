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


import numpy as np
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, Box,
                         ContactResults, ContactVisualizer,
                         ContactVisualizerParams, CoulombFriction,
                         DiagramBuilder, FixedOffsetFrame, JointSliders,
                         LeafSystem, MeshcatCone, MeshcatVisualizer,
                         PrismaticJoint, Rgba, RigidTransform, RotationMatrix,
                         SpatialInertia, Sphere, StartMeshcat, UnitInertia,
                         VectorToSkewSymmetric)

from manipulation import running_as_notebook
from manipulation.scenarios import AddShape


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Contact wrench cone "inspector"

# In[ ]:


from IPython.display import clear_output
from pydrake.all import Cylinder, PointCloud
mu = 1.0
height = .3
N = 50
t = np.linspace(0, 2*np.pi, N)
vertices = np.vstack((height*mu*np.sin(t), height*mu*np.cos(t), height + 0*t))
vertices = np.append(np.array([[0], [0], [height]]), vertices, axis=1)
vertices = np.append(np.zeros((3,1)), vertices, axis=1)
faces = []
for i in range(N-1):
    faces.append([0, i+2, i+3])
    faces.append([1, i+3, i+2])
faces = np.asarray(faces, dtype=int).T
#color = np.tile(np.array([0, 0, 255]), (vertices.shape[1],1)).T
cloud = PointCloud(vertices.shape[1])

class DrawContactWrench(LeafSystem):
    def __init__(self):
        LeafSystem.__init__(self)
        self.DeclareAbstractInputPort("contact_results",
                                      AbstractValue.Make(ContactResults()))
        self.DeclareForcedPublishEvent(self.Publish)

    def Publish(self, context):
        results = self.get_input_port().Eval(context)

        for i in range(results.num_point_pair_contacts()):
            info = results.point_pair_contact_info(i)
            meshcat.SetObject(f"contact_{i}",
                              MeshcatCone(height, height * mu, height * mu), rgba=Rgba(0.1, 0.9, 0.1, 1.0))
            p_WC = info.contact_point()
            R_WC = RotationMatrix.MakeFromOneVector(info.point_pair().nhat_BA_W,
                                                    2)
            X_WC = RigidTransform(R_WC, p_WC)
            meshcat.SetTransform(f"contact_{i}", X_WC)

            X_WB = RigidTransform()  # box center is at world origin
            meshcat.SetObject(f"box_center/contact_{i}/translational",
                              MeshcatCone(height, height * mu, height * mu),
                              rgba=Rgba(0.7, 0.1, 0.1, 1.0))
            meshcat.SetTransform("box_center", X_WB)
            R_BC = X_WB.inverse().rotation() @ R_WC
            meshcat.SetTransform(f"box_center/contact_{i}",
                                 RigidTransform(R_BC))
            p_CB_C = -(R_WC @ (X_WB.inverse() @ p_WC))
            A_CCtau = VectorToSkewSymmetric(p_CB_C)
            # Three.js does not fully support non-uniform scaling
            # https://github.com/mrdoob/three.js/issues/15079.
            # So I cannot simply draw the meshcatcone and transform it.
            # Instead I will create the vertices myself.
            cloud.mutable_xyzs()[:] = A_CCtau @ vertices
            meshcat.SetObject(f"box_center/contact_{i}/rotational_cloud",
                              cloud, point_size=0.002,
                              rgba=Rgba(0, 1, 0, 1))
            # TODO(russt): Figure out colors.  The surface mesh example works ok in meshcat_manual_test...
            meshcat.SetTriangleMesh(f"box_center/contact_{i}/rotational",
                                    A_CCtau @ vertices,
                                    faces, rgba=Rgba(0, 0, 1, 1))

        clear_output(wait=True)


def contact_wrench_inspector(second_finger=False):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0)
    box_instance = AddShape(plant, Box(1, 2, 3), "box", color=[.9, .7, .5, .5])
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("box"))

    finger1 = AddShape(plant, Sphere(0.1), "finger1", color=[.2, .2, .2, 1.0])
    box_negative_x = plant.AddFrame(
        FixedOffsetFrame("box_negative_x", plant.world_frame(),
                         RigidTransform([-.58, 0, 0]), box_instance))
    finger1_false_body = plant.AddRigidBody(
        "false_body", finger1, SpatialInertia(0, [0,0,0], UnitInertia(0,0,0)))
    finger1_y = plant.AddJoint(
        PrismaticJoint("finger1_y", box_negative_x,
                       plant.GetFrameByName("false_body", finger1), [0, 1, 0],
                       -.5, .5))
    finger1_z = plant.AddJoint(PrismaticJoint(
        "finger1_z", plant.GetFrameByName("false_body", finger1), plant.GetFrameByName("finger1"),
        [0, 0, 1], -1.5, 1.5))
    decrement_keycodes=["ArrowLeft", "ArrowDown"]
    increment_keycodes=["ArrowRight", "ArrowUp"]

    # optionally add a second finger with the same joints, but on a different face
    if second_finger:
        finger2 = AddShape(plant,
                           Sphere(0.1),
                           "finger2",
                           color=[.2, .2, .2, 1.0])
        box_positive_x = plant.AddFrame(
            FixedOffsetFrame("box_positive_x", plant.world_frame(),
                             RigidTransform([.58, 0, 0]), box_instance))
        finger2_false_body = plant.AddRigidBody(
            "false_body", finger2,
            SpatialInertia(0, [0, 0, 0], UnitInertia(0, 0, 0)))
        finger2_y = plant.AddJoint(
            PrismaticJoint("finger2_y", box_positive_x,
                           plant.GetFrameByName("false_body", finger2),
                           [0, 1, 0], -.5, .5))
        finger2_z = plant.AddJoint(
            PrismaticJoint("finger2_z",
                           plant.GetFrameByName("false_body", finger2),
                           plant.GetFrameByName("finger2"), [0, 0, 1], -1.5,
                           1.5))
        decrement_keycodes.append("KeyA")
        decrement_keycodes.append("KeyS")
        increment_keycodes.append("KeyD")
        increment_keycodes.append("KeyW")

    plant.Finalize()

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    meshcat.SetProperty('/Background', 'visible', False)
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)

    if False:
        cparams = ContactVisualizerParams()
        #cparams.force_threshold = 1e-6
        cparams.newtons_per_meter = 200.0
        cparams.radius = 0.02
        contact_visualizer = ContactVisualizer.AddToBuilder(
                builder, plant, meshcat, cparams)

    draw_contact_wrench = builder.AddSystem(DrawContactWrench())
    builder.Connect(plant.get_contact_results_output_port(),
                    draw_contact_wrench.get_input_port())

    default_interactive_timeout = None if running_as_notebook else 1.0
    sliders = builder.AddSystem(
        JointSliders(meshcat,
                     plant,
                     step=[0.05] * (4 if second_finger else 2),
                     decrement_keycodes=decrement_keycodes,
                     increment_keycodes=increment_keycodes))
    diagram = builder.Build()
    sliders.Run(diagram, default_interactive_timeout)
    meshcat.DeleteAddedControls()

contact_wrench_inspector(second_finger=True)


# In[ ]:




