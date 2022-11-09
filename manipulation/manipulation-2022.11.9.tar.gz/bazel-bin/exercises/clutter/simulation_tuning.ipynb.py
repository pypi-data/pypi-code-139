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

# In[ ]:


import numpy as np

from manipulation import running_as_notebook

from pydrake.all import (
    AddMultibodyPlantSceneGraph, Box, DiagramBuilder, ContactVisualizerParams,
    LeafSystem, MeshcatVisualizer, ContactVisualizer, MeshcatVisualizerParams, 
    MultibodyPlant, FixedOffsetFrame, Role, AbstractValue, EventStatus,
    PlanarJoint, ContactResults, BodyIndex, RigidTransform, RotationMatrix, 
    SceneGraph, JointSliders, Simulator, SpatialInertia, Sphere, UnitInertia, 
    StartMeshcat, CoulombFriction, RollPitchYaw
)

from IPython.display import clear_output

# Start the visualizer.
meshcat = StartMeshcat()


# ## **Tuning MultibodyPlant for Contact Simulation**

# # Problem Description
# 
# In earlier homework problems, you were given the simulation environment to start with. It is your turn to design and understand how simulation environment models the real world and is used in robotic software development (important topic!). In the lecture, we learned about contact modeling and what are the important parameters for a stable simulation. For this exercise, you will investigate the underlying simulation details and get prepared for your project. Specifically, we will learn both how to reproduce desired simulation output and pinpoint simulation issues, in a classic physics example of two blocks stacking on a slope.
# 
# **These are the learning goals of this exercise:**
# 1. Inspecting the contact forces of two interpenetrating boxes and capture the discontinuity of the contact forces. 
# 2. Learning to debug and engineer collision geometries.
# 3. Reproduce the output of a feasible simulation by tuning parameters.

# In[ ]:


# initial state of the boxes and the slope
slope  = 0.1 
q1 = [0.0, 0.15, 0]  
q2 = [0.0, 0.20, 0]  

# box sizes
box_size1 = [0.05, 0.05, 0.05]
box_size2 = [0.05, 0.05, 0.05]


# In[ ]:


##############################################
### Don't change/remove! For visualization ###

nonstack_pose1 = [[ 9.94885056e-01, -1.55900179e-02,  9.98031851e-02,  1.95741356e-02],
 [ 1.56650268e-02,  9.99877295e-01,  3.21017596e-05, -1.15839339e-04],
 [-9.97914393e-02,  1.53148200e-03,  9.95007198e-01,  5.83171660e-02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]

nonstack_pose2 = [[-1.00114398e-01,  5.89905683e-03,  9.94958446e-01,  2.11092651e-01],
 [ 4.44194866e-04,  9.99982590e-01, -5.88414908e-03,  2.24353720e-03],
 [-9.94975834e-01, -1.47132606e-04, -1.00115275e-01,  3.89206165e-02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]


stack_pose1 = [[ 9.94996362e-01, -3.77459725e-05,  9.99111553e-02,  2.64605688e-01],
 [ 3.79942503e-05,  9.99999999e-01, -5.82200282e-07, -1.13024604e-06],
 [-9.99111552e-02,  4.37533660e-06,  9.94996362e-01,  3.33522993e-02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]

stack_pose2 = [[ 9.94996470e-01, -1.41453220e-05,  9.99100858e-02,  2.66676737e-01],
 [ 1.41925281e-05,  1.00000000e+00,  2.38281298e-07, -9.14267754e-07],
 [-9.99100858e-02,  1.18088765e-06,  9.94996470e-01,  5.22415534e-02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]
 
##############################################
 


# In[ ]:


class PrintContactResults(LeafSystem):
    """ Helpers for printing contact results
    """
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

def AddGTBox(plant, visual_shape, name, pose, color=[.5, .5, .9, 1.0]):
    instance = plant.AddModelInstance(name + "gt")
    plant.RegisterVisualGeometry(plant.world_body(), RigidTransform(pose), visual_shape, name + "gt", color)
     


# # Inspect geometry and contact forces

# Remember in lecture we discuss how visual geometry is separated from collision geometry in scene graph. The first thing we will do is to set up the visual and collision geometry of the objects and have sanity check on their geometry, for instance, visualizing them and inspecting contact forces. 

# In[ ]:


def AddBoxDifferentGeometry(plant, visual_shape, collision_shape, name, mass=1, mu=1, color=[.5, .5, .9, 1.0]):
    instance = plant.AddModelInstance(name)
    inertia = UnitInertia.SolidBox(visual_shape.width(), visual_shape.depth(),
                                       visual_shape.height())
     
    body = plant.AddRigidBody(
        name, instance,
        SpatialInertia(mass=mass,
                       p_PScm_E=np.array([0., 0., 0.]),
                       G_SP_E=inertia))
    if plant.geometry_source_is_registered():
        """ register collision geometry"""       
        plant.RegisterCollisionGeometry(body, RigidTransform(), collision_shape, name,
                                        CoulombFriction(mu, mu))
        """ register visual geometry"""
        plant.RegisterVisualGeometry(body, RigidTransform(), visual_shape, name, color)
    return 


# In[ ]:


q1_teleop = [0.0, 0.15, 0]  
q2_teleop = [0.0, 0.20, 0]  

# box sizes
box_size1_teleop = [0.05, 0.05, 0.05]
box_size2_teleop = [0.05, 0.05, 0.05]

def make_teleop_simulation(time_step, mass, mu, slope_size=[10,10,0.1], mu_g=0.1, interactive=True):
    """
    a nice interface to inspect contact forces
    YOUR CODE HERE
    """
    builder = DiagramBuilder()
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.01)
    box = Box(*slope_size) 
    X_WBox = RigidTransform(RotationMatrix.MakeYRotation(slope), [0, 0, 0])
    plant.RegisterCollisionGeometry(plant.world_body(), X_WBox, box, "ground",
                                    CoulombFriction(mu_g, mu_g))
    plant.RegisterVisualGeometry(plant.world_body(), X_WBox, box, "ground",
                                    [.9, .9, .9, 1.0])

    box_instance = AddBoxDifferentGeometry(plant, Box(*box_size1_teleop), Box(*[x*0.5 for x in box_size1_teleop]), "box", 
                        mass[0], mu[0], color=[0.8, 0, 0, 1.0])

    frame = plant.AddFrame(
        FixedOffsetFrame(
            "planar_joint_frame", plant.world_frame(),
            RigidTransform(RotationMatrix.MakeXRotation(np.pi / 2))))
    plant.AddJoint(
        PlanarJoint("box",
                    frame,
                    plant.GetFrameByName("box"),
                    damping=[0, 0, 0]))

    box_instance_2 = AddBoxDifferentGeometry(plant, Box(*box_size2_teleop), Box(*[x*0.5 for x in box_size2_teleop]), "box_2",
                        mass[1], mu[1], color=[0, 0.8, 0, 1.0])
    
    frame_2 = plant.AddFrame(
        FixedOffsetFrame(
            "planar_joint_frame_2", plant.world_frame(),
            RigidTransform(RotationMatrix.MakeXRotation(np.pi / 2))))
    plant.AddJoint(
        PlanarJoint("box_2",
                    frame_2,
                    plant.GetFrameByName("box_2"),
                    damping=[0, 0, 0]))
    plant.Finalize()

    """ meshcat visualization """
    meshcat.Delete()
    meshcat.DeleteAddedControls()
    meshcat_param = MeshcatVisualizerParams()
    
    """ kProximity for collision geometry and kIllustration for visual geometry """
    meshcat_param.role = Role.kIllustration 
    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat, meshcat_param)
    meshcat.Set2dRenderMode(xmin=-.2, xmax=.2, ymin=-.2, ymax=0.3)
    print_contact_results = builder.AddSystem(PrintContactResults())
    builder.Connect(plant.get_contact_results_output_port(),
                    print_contact_results.get_input_port())

    """ visualize contact force """               
    cparams = ContactVisualizerParams()
    cparams.force_threshold = 1e-4
    cparams.newtons_per_meter = 2
    cparams.radius = 0.001
    contact_visualizer = ContactVisualizer.AddToBuilder(
        builder, plant, meshcat, cparams)   

    """ add joint slider """
    default_interactive_timeout = None if running_as_notebook else 1.0
    lower_limit = [-0.2, -0.2, -np.pi/2.0]
    upper_limit = [0.2, 0.2, np.pi/2.0]
    lower_limit += lower_limit
    upper_limit += upper_limit    
    sliders = builder.AddSystem(
        JointSliders(meshcat,
                        plant,
                        initial_value=q1_teleop+q2_teleop,
                        lower_limit=lower_limit,
                        upper_limit=upper_limit,
                        step=0.001))
             
    diagram = builder.Build()
    if running_as_notebook and interactive:
        sliders.Run(diagram, default_interactive_timeout)
        meshcat.DeleteAddedControls() 
    return plant, diagram


# (2pt) a. Try running the teleop simulation and try to make two boxes collide. Is there contact forces between the box when two boxes just touch each other? Actually, your evil TA leave a small bug in one line in `make_teleop_simulation` that causes geometry mismatch and we should fix it! HINT: Visualize the collision geometry by setting `meshcat_param.role = Role.kProximity`. You can use Stop_JointSliders in the meshcat to terminate the simulation block.

# In[ ]:


plant_a, diagram_a = make_teleop_simulation(0.01, (0.1, 0.1), (0.1, 0.1))


# Even with the correct collision geometry, there are cases where simple contact models are not sufficient. To make sure you understand this point, let's use the teleop interface again to find any discontinuous contact force changes between the two boxes.
#  
# (2pt) b. Change parameters in the function `set_block_2d_poses` such that there is an instantaneous change of contact forces in your visualization. You will need to find two sets of values for the block 2D pose that are very close to each other but cause a discontinuous jump in the contact force. Recall the point contact discussion the [lecture](https://youtu.be/N19SU7vgX7c?t=4550). 
# 
# Hints:
# - Use the meshcat sliders and the contact force visualizer to find (x, y, theta) values for both blocks.
# - Find one set of values that causes a contact force in one direction, and a nearby set of values that causes a contact force in a very different direction. Note that there is just one contact between the [surfaces](https://drake.mit.edu/doxygen_cxx/group__contact__engineering.html).

# In[ ]:


def set_block_2d_poses():
    """
    fill the 2D pose of the blocks that causes a discontinuous force change
    YOUR CODE HERE
    """
    box1_pos1 = [0., 0.12, 0.]
    box2_pos1 = [0., 0.2, 0.]
    
    box1_pos2 = [0., 0.13, 0.]
    box2_pos2 = [0., 0.2, 0.]
    return box1_pos1, box2_pos1, box1_pos2, box2_pos2


# #  Set up your MultibodyPlant
# In practice, you often have a simulation engine that is doing its job and an intuition on what the simulation outcomes would be. However, to make the simulation performant, you often need to set the right physics parameters, e.g. mass and frictions, in addition to have a correct geometry. Run the code below to set up the simulation testing code.

# In[ ]:


# use a new set of hyperparameters for the remaining sections
slope  = 0.1
q1 = [0.0, 0,  0.15]  
q2 = [0.0, 0,  0.20]  

# box sizes
box_size1 = [0.02, 0.02, 0.02]
box_size2 = [0.02, 0.02, 0.02]


# In[ ]:


# use a new set of hyperparameters for the remaining sections
slope  = 0.1
q1 = [0.0, 0,  0.15]  
q2 = [0.0, 0,  0.20]  

# box sizes
box_size1 = [0.02, 0.02, 0.02]
box_size2 = [0.02, 0.02, 0.02]

def AddBox(plant, shape, name, mass=1, mu=1, color=[.5, .5, .9, 1.0]):
    instance = plant.AddModelInstance(name)
    inertia = UnitInertia.SolidBox(shape.width(), shape.depth(),
                                       shape.height())
     
    body = plant.AddRigidBody(
        name, instance,
        SpatialInertia(mass=mass,
                       p_PScm_E=np.array([0., 0., 0.]),
                       G_SP_E=inertia))
    if plant.geometry_source_is_registered():
        plant.RegisterCollisionGeometry(body, RigidTransform(), shape, name,
                                        CoulombFriction(mu, mu))
        plant.RegisterVisualGeometry(body, RigidTransform(), shape, name, color)
    return 


class SimulationMaker:
    def __init__(self, add_box_func=None):
        self.add_box_func = add_box_func

    def set_add_box_func(self, add_box_func):
        self.add_box_func = add_box_func

    def make_simulation(self, time_step, mass, mu, slope_size=[10,10,0.1], mu_g=0.1, 
                    simulation_time=1., vis_contact_force=False):
        assert self.add_box_func is not None, 'Must set our self.add_box_func! Please call self.set_add_box_func with a user-defined function'
        builder = DiagramBuilder()
        plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=time_step)
        box = Box(*slope_size)
        X_WBox = RigidTransform(RotationMatrix.MakeYRotation(slope), [0, 0, 0]) # -5.05
        plant.RegisterCollisionGeometry(plant.world_body(), X_WBox, box, "ground",
                                        CoulombFriction(mu_g, mu_g))
        plant.RegisterVisualGeometry(plant.world_body(), X_WBox, box, "ground",
                                        [.9, .9, .9, 1.0])
        box_instance = self.add_box_func(plant, Box(*box_size1), "box", mass[0], mu[0], color=[0.8, 0, 0, 1.0])
        box_instance_2 = self.add_box_func(plant, Box(*box_size2), "box_2", mass[1], mu[1], color=[0, 0.8, 0, 1.0])
        nonstacking = (simulation_time == 1)
        if nonstacking:
            AddGTBox(plant, Box(*box_size1), "box", pose=nonstack_pose1, color=[0.8, 0, 0, 0.3] )
            AddGTBox(plant, Box(*box_size1), "box_2", pose=nonstack_pose2, color=[0, 0.8, 0, 0.3] )
        else:
            AddGTBox(plant, Box(*box_size1), "box", pose=stack_pose1, color=[0.8, 0, 0, 0.3] )
            AddGTBox(plant, Box(*box_size1), "box_2", pose=stack_pose2, color=[0, 0.8, 0, 0.3] )

        # build the plant and meshcat
        plant.Finalize()
        meshcat.Delete()
        meshcat.DeleteAddedControls()
        meshcat_param = MeshcatVisualizerParams()

        """ kProximity for collision geometry and kIllustration for visual geometry """
        meshcat_param.role = Role.kIllustration 
        visualizer = MeshcatVisualizer.AddToBuilder(
            builder, scene_graph, meshcat, meshcat_param)

        meshcat.Set2dRenderMode(xmin=-.2, xmax=.2, ymin=-.2, ymax=0.3)
        print_contact_results = builder.AddSystem(PrintContactResults())
        builder.Connect(plant.get_contact_results_output_port(),
                        print_contact_results.get_input_port())

        if vis_contact_force:
            """ visualize contact force """               
            cparams = ContactVisualizerParams()
            cparams.force_threshold = 1e-4
            cparams.newtons_per_meter = 2
            cparams.radius = 0.001
            contact_visualizer = ContactVisualizer.AddToBuilder(
                builder, plant, meshcat, cparams)  
            meshcat.SetRealtimeRate(0.01) 

        # initialize simulation
        diagram = builder.Build()
        simulator = Simulator(diagram)
        if  nonstacking: 
            simulator.set_target_realtime_rate(.5)  # slow motion!
        else:
            simulator.set_target_realtime_rate(3)  # fast motion!

        tf1 = RigidTransform(RollPitchYaw(0, 0, 0), q1)
        tf2 = RigidTransform(RollPitchYaw(0, 0, 0), q2)     
        context = simulator.get_context()
        plant_context = diagram.GetSubsystemContext(plant, context)
        plant.SetFreeBodyPose(plant_context, plant.get_body(BodyIndex(1)), tf1)
        plant.SetFreeBodyPose(plant_context, plant.get_body(BodyIndex(2)), tf2)

        # simulate and visualize
        visualizer.StartRecording()
        simulator.AdvanceTo(simulation_time)

        visualizer.StopRecording()
        visualizer.PublishRecording()
        return simulator, diagram

sim_maker = SimulationMaker(AddBox)


# (2pt) c. Run the code block below. We notice that the green block is falling below the red block as well as the thin slope. Why? Anwer in your written submission.
# 
# (2pt) d. There are specific algorithms that can help avoid pass-through events in simulation, which we haven't implemented yet here. But even without them, we can address the issue by tuning the timesteps. Try tuning the simulation timestep and the mass in `set_parameter_d` such that the both block falls on (but not inside) the slope. Note that if the simulation advances too fast, you can pause and reset simulation to check the initial state. Write your answer in written submission.

# In[ ]:


def set_parameter_d():
    """
    fill your choice of parameters here to make the box 
    not fall under the slope
    YOUR CODE HERE
    """
    time_step = 0.1
    mass1, mass2 = 0.01, 5
    return time_step, (mass1, mass2), (0.1, 0.1)

simulator_d, diagram_d = sim_maker.make_simulation(*set_parameter_d())


# # Improve contact geometry
# 
# Contact geometry, especially for complex meshes, plays an important role for your manipulation simulation to accurately model the real world (or even just remain stable). In your project, you might find this [package](https://github.com/gizatt/convex_decomp_to_sdf) useful for generating convex decomposition of complex mesh. 
# 
# (4pt) e. When it is not falling below the slope (with timestep 0.001), you might observe an unexpected out-of-plane rotation of the box on the slope.  In lectures and the exercise above, we discuss that simulation quality depends on the geometry. Although a more general approach for contact dynamics simulation is often prefered, such as [hydroelastic](https://drake.mit.edu/doxygen_cxx/group__hydroelastic__user__guide.html), we consider a simple "hacky" way to make the simulation of box on the slope more [accurate](https://drake.mit.edu/doxygen_cxx/group__contact__engineering.html). We will make the box to be of smaller size ($1e-7$ m at each dimension) and adding a small `Sphere(radius=1e-7)` around the 8 corners of the box. Please re-implement the function `AddBox` below and make the blocks do not rotate out-of-plane. Note that you can set `vis_contact_force=True` in `set_simulation` to visualize the contact force. 

# In[ ]:


def AddBox(plant, shape, name, mass=1, mu=1, color=[.5, .5, .9, 1.0]):
    instance = plant.AddModelInstance(name)
    inertia = UnitInertia.SolidBox(shape.width(), shape.depth(),
                                       shape.height())
     
    body = plant.AddRigidBody(
        name, instance,
        SpatialInertia(mass=mass,
                       p_PScm_E=np.array([0., 0., 0.]),
                       G_SP_E=inertia))
    if plant.geometry_source_is_registered():
        #######################################
        """ 
        replace the line below and reimplement your code for collsion geometry here 
        step 1: make a smaller box
        step 2: put small spheres at each of the corners
        """
        plant.RegisterCollisionGeometry(body, RigidTransform(), shape, name,
                                        CoulombFriction(mu, mu))        
        plant.RegisterVisualGeometry(body, RigidTransform(), shape, name, color)
    return 

### Don't remove ###

sim_maker.set_add_box_func(AddBox)

####################


# In[ ]:


simulator_e, diagram_e = sim_maker.make_simulation(0.001, (1, 1), (0.1, 0.1)) # parameters for grading


# (2pt) f. Finally, try to reproduce the image of the groundtruth simulation at time T=1.0 by tuning the friction parameters and the masses of the boxes in `set_parameter_f`  
# 
# <img src="https://raw.githubusercontent.com/RussTedrake/manipulation/master/figures/exercises/sim_tuning_final_state1.gif" width="700"> 

# In[ ]:


q1 = [0.0, 0,  0.065]  
q2 = [0.0, 0,  0.087]
def set_parameter_f():
    """
    fill your choice of parameters here to match the gif above
    YOUR CODE HERE
    """
    mass1, mass2 = 0.01, 5
    mu1, mu2     = 0., 1
    return 0.001, (mass1, mass2), (mu1, mu2)
simulator_f, diagram_f = sim_maker.make_simulation(*set_parameter_f())


# # Stacking blocks
# (3pt) g. Define the slope angle as $p$ and the friction between the two blocks (top $m_1$ and bottom $m_2$) is $\mu_1$ and the friction between the slope surface and the bottom block $m_2$ to be $\mu_2$. Assume that two boxes are on top of each other on the slope, what constraint needs to be on the friction parameter $\mu_1,\mu_2$ such that the top block is sticking (no relative velocity) and the bottom block is sliding at the constant speed, which one is greater and do them depend on the mass $m_1,m_2$ of the blocks? Draw out the free-body [diagram](https://youtu.be/N19SU7vgX7c?t=3394). Write your answer in written submission.
# 
# (3pt) h. Try to reproduce the goal image in simulation below at time step 1.0 by changing the parameters in `set_parameter_h`. 
# 
# <img src="https://raw.githubusercontent.com/RussTedrake/manipulation/master/figures/exercises/sim_tuning_final_state2.gif" width="700"> 

# In[ ]:


q1 = [0.0, 0,  0.065]  
q2 = [0.0, 0,  0.087] 

def set_parameter_h():
    """
    fill your choice of parameters here to make the blocks stack and move as above
    YOUR CODE HERE
    """
    time_step = 0.1 
    mass1, mass2 = 0.1, 5
    mu1, mu2     = 0.4, 1 
    return time_step, (mass1, mass2), (mu1, mu2)

# you might have to make simulator timestep really small, and it would still be sliding. Why?
# Check the last section here https://drake.mit.edu/doxygen_cxx/group__contact__engineering.html
simulator_h, diagram_h = sim_maker.make_simulation(*set_parameter_h(), simulation_time=5.)


# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do two things. 
# - Download and submit the notebook `simulation_tuning.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# - Write down your answers to 5.6 to a separately pdf file and submit it to Gradescope's written submission section. 
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [2 pts] 5.6.a the bug in `make_teleop_simulation` is fixed correctly.
# - [2 pts] 5.6.b `set_block_2d_poses` is implemented correctly.
# - [2 pts] 5.6.c the reason for block falling is answered correctly and attached to written solution. 
# - [2 pts] 5.6.d `set_parameter_d` is implemented correctly. 
# - [4 pts] 5.6.e `AddBox` is implemented correctly. 
# - [2 pts] 5.6.f `set_parameter_f` is implemented correctly.
# - [3 pts] 5.6.g  the analysis is answered correctly.
# - [3 pts] 5.6.h `set_parameter_h` is implemented correctly.

# In[ ]:


from manipulation.exercises.clutter.test_simulation_tuning import TestSimulationTuning
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestSimulationTuning], [locals()], 'results.json')
Grader.print_test_results('results.json')

