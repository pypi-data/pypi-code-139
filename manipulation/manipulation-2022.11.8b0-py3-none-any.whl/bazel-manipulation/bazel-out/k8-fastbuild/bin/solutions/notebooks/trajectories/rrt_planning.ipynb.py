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

# In[ ]:


import time
from random import random

import numpy as np
from manipulation import running_as_notebook
from manipulation.exercises.trajectories.rrt_planner.robot import (
    ConfigurationSpace, Range)
from manipulation.exercises.trajectories.rrt_planner.rrt_planning import     Problem
from manipulation.meshcat_utils import AddMeshcatTriad
from pydrake.all import (DiagramBuilder, FindResourceOrThrow,
                         MeshcatVisualizer, MultibodyPlant, Parser,
                         RigidTransform, RollPitchYaw, RotationMatrix,
                         Simulator, SolutionResult, Solve, StartMeshcat)
from pydrake.examples.manipulation_station import (IiwaCollisionModel,
                                                   ManipulationStation)
from pydrake.multibody import inverse_kinematics


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# In[ ]:



class ManipulationStationSim:
    def __init__(self, is_visualizing=False):
        self.station = ManipulationStation()
        self.station.SetupManipulationClassStation(
            IiwaCollisionModel.kBoxCollision)
        self.station.Finalize()
        self.plant = self.station.get_mutable_multibody_plant()
        self.scene_graph = self.station.get_mutable_scene_graph()
        self.is_visualizing = is_visualizing

        # scene graph query output port.
        self.query_output_port = self.scene_graph.GetOutputPort("query")

        builder = DiagramBuilder()
        builder.AddSystem(self.station)
        # meshcat visualizer
        if is_visualizing:
            self.viz = MeshcatVisualizer.AddToBuilder(
                builder, 
                self.station.GetOutputPort("query_object"),
                meshcat)

        self.diagram = builder.Build()

        # contexts
        self.context_diagram = self.diagram.CreateDefaultContext()
        self.context_station = self.diagram.GetSubsystemContext(
            self.station, self.context_diagram)
        self.context_scene_graph = self.station.GetSubsystemContext(
            self.scene_graph, self.context_station)
        self.context_plant = self.station.GetMutableSubsystemContext(
            self.plant, self.context_station)
        # mark initial configuration
        self.q0 = self.station.GetIiwaPosition(self.context_station)
        if is_visualizing:
            self.DrawStation(self.q0, 0.1, -np.pi/2, np.pi/2)

    def SetStationConfiguration(self, q_iiwa, gripper_setpoint, left_door_angle,
                                right_door_angle):
        """
        :param q_iiwa: (7,) numpy array, joint angle of robots in radian.
        :param gripper_setpoint: float, gripper opening distance in meters.
        :param left_door_angle: float, left door hinge angle, \in [0, pi/2].
        :param right_door_angle: float, right door hinge angle, \in [0, pi/2].
        :return:
        """
        self.station.SetIiwaPosition(self.context_station, q_iiwa)
        self.station.SetWsgPosition(self.context_station, gripper_setpoint)

        # cabinet doors
        if left_door_angle > 0:
            left_door_angle *= -1
        left_hinge_joint = self.plant.GetJointByName("left_door_hinge")
        left_hinge_joint.set_angle(context=self.context_plant,
                                   angle=left_door_angle)

        right_hinge_joint = self.plant.GetJointByName("right_door_hinge")
        right_hinge_joint.set_angle(context=self.context_plant,
                                    angle=right_door_angle)

    def DrawStation(self, q_iiwa, gripper_setpoint, q_door_left, q_door_right):
        if not self.is_visualizing:
            print("collision checker is not initialized with visualization.")
            return
        self.SetStationConfiguration(
            q_iiwa, gripper_setpoint, q_door_left, q_door_right)
        self.diagram.Publish(self.context_diagram)

    def ExistsCollision(self, q_iiwa, gripper_setpoint, q_door_left, q_door_right):

        self.SetStationConfiguration(
            q_iiwa, gripper_setpoint, q_door_left, q_door_right)
        query_object = self.query_output_port.Eval(self.context_scene_graph)
        collision_paris = query_object.ComputePointPairPenetration()

        return len(collision_paris) > 0
    
class IiwaProblem(Problem):
    def __init__(self,
                 q_start: np.array,
                 q_goal: np.array,
                 gripper_setpoint: float,
                 left_door_angle: float,
                 right_door_angle: float,
                 is_visualizing=False):
        self.gripper_setpoint = gripper_setpoint
        self.left_door_angle = left_door_angle
        self.right_door_angle = right_door_angle
        self.is_visualizing = is_visualizing

        self.collision_checker = ManipulationStationSim(
            is_visualizing=is_visualizing)

        # Construct configuration space for IIWA.
        plant = self.collision_checker.plant
        nq = 7
        joint_limits = np.zeros((nq, 2))
        for i in range(nq):
            joint = plant.GetJointByName("iiwa_joint_%i" % (i + 1))
            joint_limits[i, 0] = joint.position_lower_limits()
            joint_limits[i, 1] = joint.position_upper_limits()

        range_list = []
        for joint_limit in joint_limits:
            range_list.append(Range(joint_limit[0], joint_limit[1]))

        def l2_distance(q: tuple):
            sum = 0
            for q_i in q:
                sum += q_i ** 2
            return np.sqrt(sum)

        max_steps = nq * [np.pi / 180 * 2]  # three degrees
        cspace_iiwa = ConfigurationSpace(range_list, l2_distance, max_steps)

        # Call base class constructor.
        Problem.__init__(
            self,
            x=10,  # not used.
            y=10,  # not used.
            robot=None,  # not used.
            obstacles=None,  # not used.
            start=tuple(q_start),
            goal=tuple(q_goal),
            cspace=cspace_iiwa)

    def collide(self, configuration):
        q = np.array(configuration)
        return self.collision_checker.ExistsCollision(
                    q, self.gripper_setpoint, self.left_door_angle, self.right_door_angle)

    def visualize_path(self, path):
        if path is not None:
        # show path in meshcat
            for q in path:
                q = np.array(q)
                self.collision_checker.DrawStation(
                    q, self.gripper_setpoint, self.left_door_angle,
                    self.right_door_angle)
                if running_as_notebook:
                    time.sleep(0.2)


class IKSolver(object):
    def __init__(self):
        ## setup controller plant
        plant_iiwa = MultibodyPlant(0.0)
        iiwa_file = FindResourceOrThrow(
        "drake/manipulation/models/iiwa_description/iiwa7/"
        "iiwa7_no_collision.sdf")
        iiwa = Parser(plant_iiwa).AddModelFromFile(iiwa_file)
        # Define frames
        world_frame = plant_iiwa.world_frame()
        L0 = plant_iiwa.GetFrameByName("iiwa_link_0")
        l7_frame = plant_iiwa.GetFrameByName("iiwa_link_7")
        plant_iiwa.WeldFrames(world_frame, L0)
        plant_iiwa.Finalize()
        plant_context = plant_iiwa.CreateDefaultContext()
        
        # gripper in link 7 frame
        X_L7G = RigidTransform(rpy=RollPitchYaw([np.pi/2, 0, np.pi/2]), 
                                    p=[0,0,0.114])
        world_frame = plant_iiwa.world_frame()

        self.world_frame = world_frame
        self.l7_frame = l7_frame
        self.plant_iiwa = plant_iiwa
        self.plant_context = plant_context
        self.X_L7G = X_L7G

    def solve(self, X_WT, q_guess = None, theta_bound=0.01, position_bound=0.01):
        """
        plant: a mini plant only consists of iiwa arm with no gripper attached
        X_WT: transform of target frame in world frame
        q_guess: a guess on the joint state sol
        """
        plant = self.plant_iiwa
        l7_frame = self.l7_frame
        X_L7G = self.X_L7G
        world_frame = self.world_frame

        R_WT = X_WT.rotation()
        p_WT = X_WT.translation()
        
        if q_guess is None:
            q_guess = np.zeros(7)
        
        ik_instance = inverse_kinematics.InverseKinematics(plant)
        # align frame A to frame B
        ik_instance.AddOrientationConstraint(frameAbar=l7_frame, 
                                        R_AbarA=X_L7G.rotation(),
                                        #   R_AbarA=RotationMatrix(), # for link 7
                                        frameBbar=world_frame, 
                                        R_BbarB=R_WT, 
                                        theta_bound=position_bound)
        # align point Q in frame B to the bounding box in frame A
        ik_instance.AddPositionConstraint(frameB=l7_frame, 
                                        p_BQ=X_L7G.translation(),
                                        # p_BQ=[0,0,0], # for link 7
                                    frameA=world_frame, 
                                    p_AQ_lower=p_WT-position_bound, 
                                    p_AQ_upper=p_WT+position_bound)
        prog = ik_instance.prog()
        prog.SetInitialGuess(ik_instance.q(), q_guess)
        result = Solve(prog)
        if result.get_solution_result() != SolutionResult.kSolutionFound:
            return result.GetSolution(ik_instance.q()), False
        return result.GetSolution(ik_instance.q()), True

class TreeNode:
    def __init__(self, value, parent=None):
        self.value = value  # tuple of floats representing a configuration
        self.parent = parent  # another TreeNode
        self.children = []  # list of TreeNodes
        
class RRT:
    """
    RRT Tree.
    """
    def __init__(self, root: TreeNode, cspace: ConfigurationSpace):
        self.root = root  # root TreeNode
        self.cspace = cspace  # robot.ConfigurationSpace
        self.size = 1  # int length of path
        self.max_recursion = 1000  # int length of longest possible path

    def add_configuration(self, parent_node, child_value):
        child_node = TreeNode(child_value, parent_node)
        parent_node.children.append(child_node)
        self.size += 1
        return child_node

    # Brute force nearest, handles general distance functions
    def nearest(self, configuration):
        """
        Finds the nearest node by distance to configuration in the
             configuration space.

        Args:
            configuration: tuple of floats representing a configuration of a
                robot

        Returns:
            closest: TreeNode. the closest node in the configuration space
                to configuration
            distance: float. distance from configuration to closest
        """
        assert self.cspace.valid_configuration(configuration)
        def recur(node, depth=0):
            closest, distance = node, self.cspace.distance(node.value, configuration)
            if depth < self.max_recursion:
                for child in node.children:
                    (child_closest, child_distance) = recur(child, depth+1)
                    if child_distance < distance:
                        closest = child_closest
                        child_distance = child_distance
            return closest, distance
        return recur(self.root)[0]


# # RRT Motion Planning
# 
# In the lectures on motion planning, you are introduced to optimization-based motion planning and sampling-based motion planning. In this exercise, you will first implement the famous Rapidly-exploring Random Tree (RRT) algorithm. Next, you will reflect on the properties of the RRT algorithm. A 2D visualization of the RRT algorithm is shown below. 

# In[ ]:


from IPython.display import Image
Image(url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Rapidly-exploring_Random_Tree_%28RRT%29_500x373.gif/450px-Rapidly-exploring_Random_Tree_%28RRT%29_500x373.gif')


# Let's first generate a problem instance. Let's use the default initial joint state as our starting configuration $q_{start}$. Let's use a pre-defined frame in 3D world as our goal pose. The frame of the goal pose can be viewed in the meshcat visualizer below. 

# In[ ]:


env = ManipulationStationSim(True)
q_start = env.q0
R_WG = RotationMatrix(np.array([[0,1,0], [1,0,0], [0,0,-1]]).T)
T_WG_goal = RigidTransform(p=np.array([4.69565839e-01, 2.95894043e-16, 0.65]), R=R_WG)
AddMeshcatTriad(meshcat, 'goal pose', X_PT=T_WG_goal, opacity=.5)


# The joint states of the goal pose can be computed via inverse kinematics.

# In[ ]:


ik_solver = IKSolver()
q_goal, optimal = ik_solver.solve(T_WG_goal, q_guess=q_start)


# Given the start and goal states, we now have sufficient information to formulate the pathfinding problem. We use `IiwaProblem` class to store all relevant information about the pathfinding problem. For this exercise, you don't have to know the details of this class.

# In[ ]:


gripper_setpoint = 0.1
door_angle = np.pi/2 - 0.001
left_door_angle = -np.pi/2
right_door_angle = np.pi/2

iiwa_problem = IiwaProblem(
    q_start=q_start,
    q_goal=q_goal,
    gripper_setpoint=gripper_setpoint,
    left_door_angle=left_door_angle,
    right_door_angle=right_door_angle,
    is_visualizing=True)


# # RRT Algorithm
# 
# An RRT grows a tree rooted at the starting configuration by using random samples from the search space. As each sample is drawn, a connection is attempted between it and the nearest state in the tree. If the connection is feasible (passes entirely through free space and obeys any constraints), this results in the addition of the new state to the tree.
# 
# With uniform sampling of the search space, the probability of expanding an existing state is proportional to the size of its Voronoi region. As the largest Voronoi regions belong to the states on the frontier of the search, this means that the tree preferentially expands towards large unsearched areas.
# 
# However, it may be useful sometimes to bias our exploration towards the goal. In that case, one can artificially set a probability to use the value of the goal as the next sample. 
# 
# The pseudocode of the RRT algorithm is shown below.

#   **Algorithm RRT**
#     
#       Input: q_start, q_goal, max_interation, prob_sample_goal
#       Output: path
# 
#       G.init(q_start)
#       for k = 1 to max_interation:
#         q_sample ← Generate Random Configuration
#         random number ← random()
#         if random_number < prob_sample_goal:
#             q_sample ← q_goal
#         n_near ← Find the nearest node in the tree(q_sample)
#         (q_1, q_2, ... q_N) ← Find intermediate q's from n_near to q_sample
#         
#         // iteratively add the new nodes to the tree to form a new edge
#         last_node ← n_near
#         for n = 1 to N:
#             last_node ← Grow RRT tree (parent_node, q_{n}) 
#         
#         if last node reaches the goal:
#             path ← backup the path recursively
#             return path
#         
#       return None

# Implementing RRT from scratch can be very time-consuming. Below, we have provided you the important features you will need to implement the RRT algorithm. Note that in `RRT_tools`, a robot configuration is referred to as $q$, whereas a node in the RRT tree is referred to as a node. One can access the configuration of a node by 
# ```
# q_sample = node.value
# ```

# In[ ]:


class RRT_tools:
    def __init__(self, problem):
        # rrt is a tree 
        self.rrt_tree = RRT(TreeNode(problem.start), problem.cspace)
        problem.rrts = [self.rrt_tree]
        self.problem = problem
        
    def find_nearest_node_in_RRT_graph(self, q_sample):
        nearest_node = self.rrt_tree.nearest(q_sample)
        return nearest_node
    
    def sample_node_in_configuration_space(self):
        q_sample = self.problem.cspace.sample()
        return q_sample
    
    def calc_intermediate_qs_wo_collision(self, q_start, q_end):
        '''create more samples by linear interpolation from q_start
        to q_end. Return all samples that are not in collision
        
        Example interpolated path: 
        q_start, qa, qb, (Obstacle), qc , q_end
        returns >>> q_start, qa, qb
        '''
        return self.problem.safe_path(q_start, q_end)
    
    def grow_rrt_tree(self, parent_node, q_sample):
        """
        add q_sample to the rrt tree as a child of the parent node
        returns the rrt tree node generated from q_sample
        """
        child_node = self.rrt_tree.add_configuration(parent_node, q_sample)
        return child_node
    
    def node_reaches_goal(self, node):
        return node.value == self.problem.goal
    
    def backup_path_from_node(self, node):
        path = [node.value]
        while node.parent is not None:
            node = node.parent
            path.append(node.value)
        path.reverse()
        return path


# ## Implement RRT
# 
# **(a) Implement the RRT algorithm below. You may find it significantly easier to use the `RRT_tools`.** 
# In your implementation, you may plan in either configuration space or task space. The provided `RRT_tools` is only for planning in the configuration space. Your implementation will be graded on whether the last node of the path has reached the goal.

# In[ ]:


def rrt_planning(problem, max_iterations=1000, prob_sample_q_goal=.05):
    """
    Input: 
        problem (IiwaProblem): instance of a utility class
        max_iterations: the maximum number of samples to be collected 
        prob_sample_q_goal: the probability of sampling q_goal

    Output:
        path (list): [q_start, ...., q_goal]. 
                    Note q's are configurations, not RRT nodes 
    """
    rrt_tools = RRT_tools(iiwa_problem)
    q_goal = problem.goal
    q_start = problem.start
    
    return None


# In[ ]:


def rrt_planning(problem, max_iterations=1000, prob_sample_q_goal=.05):
    """
    Input: 
        problem (IiwaProblem): instance of a utility class
        max_iterations: the maximum number of samples to be collected 
        prob_sample_q_goal: the probability of sampling q_goal

    Output:
        path (list): [q_start, ...., q_goal]. 
                    Note q's are configurations, not RRT nodes 
    """
    rrt_tools = RRT_tools(iiwa_problem)
    q_goal = problem.goal
    q_start = problem.start
    
    for i in range(max_iterations):
        q_sample = rrt_tools.sample_node_in_configuration_space()
        if random() < prob_sample_q_goal or i == max_iterations-1:
            q_sample = q_goal
        closest_node = rrt_tools.find_nearest_node_in_RRT_graph(q_sample)
        edge = rrt_tools.calc_intermediate_qs_wo_collision(closest_node.value, q_sample)
        last_node = closest_node
        for j in range(1, len(edge)):
            last_node = rrt_tools.grow_rrt_tree(last_node, edge[j])
        
        if rrt_tools.node_reaches_goal(last_node):
            print('found goal')
            path = rrt_tools.backup_path_from_node(last_node)
            return path
    return None


# In[ ]:


path = rrt_planning(iiwa_problem, 600, .05)


# You may step through the waypoints of the planned path below.

# In[ ]:


iiwa_problem.visualize_path(path)


# **Answer the following question regarding the properties of the RRT algorithm**
# 
# (b) Consider the case where we let our RRT algorithm run forever, i..e max_iterations is set to $\infty$. If there is no path to the goal, will RRT warn you? If there is a path to the goal, will RRT eventually find that path? Explain your reasoning for both cases. 
# 

# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do two things. 
# - Download and submit the notebook `rrt_planning.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# - Write down your answers to 8.2.b in your PDF submission to Gradescope. 
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [5 pts] Correct Implementation of `rrt_planning` method.
# - [3 pts] Reasonable answers and explanations for part (b) 

# In[ ]:


from manipulation.exercises.trajectories.test_rrt_planning import TestRRT
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestRRT], [locals()], 'results.json')
Grader.print_test_results('results.json')

