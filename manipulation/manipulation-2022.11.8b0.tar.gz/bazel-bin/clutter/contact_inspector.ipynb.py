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
from IPython.display import clear_output, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, Box,
                         Capsule, ContactResults, ContactVisualizer,
                         ContactVisualizerParams, CoulombFriction, Cylinder,
                         DiagramBuilder, Ellipsoid, FixedOffsetFrame,
                         JointSliders, LeafSystem, MeshcatVisualizer, Parser,
                         PlanarJoint, Rgba, RigidTransform, RotationMatrix,
                         SpatialInertia, Sphere, StartMeshcat, UnitInertia)

from manipulation import running_as_notebook
from manipulation.utils import FindResource


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


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

        clear_output(wait=True)

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
            
        clear_output(wait=True)

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


# In[ ]:




