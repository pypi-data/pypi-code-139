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

# ## **Grasp Candidate Sampling**
# 

# In[ ]:


import numpy as np
from manipulation import running_as_notebook
from manipulation.meshcat_utils import AddMeshcatTriad
from manipulation.mustard_depth_camera_example import MustardPointCloud
from manipulation.scenarios import AddMultibodyTriad
from manipulation.utils import FindResource, LoadDataResource
from pydrake.all import (AddMultibodyPlantSceneGraph, Box, DiagramBuilder,
                         FindResourceOrThrow, MeshcatVisualizer, Parser,
                         PointCloud, Rgba, RigidTransform, RotationMatrix,
                         StartMeshcat)
from scipy.spatial import KDTree


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# In[ ]:


# Basic setup
pcd = MustardPointCloud(normals=True, down_sample=False)

meshcat.SetProperty("/Background", "visible", False)
meshcat.SetObject("cloud", pcd, point_size=0.001)

def setup_grasp_diagram(draw_frames=True):
  builder = DiagramBuilder()
  plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
  parser = Parser(plant)
  gripper = parser.AddModelFromFile(FindResource(
      "models/schunk_wsg_50_welded_fingers.sdf"), "gripper")
  if draw_frames:
      AddMultibodyTriad(plant.GetFrameByName("body"), scene_graph)
  plant.Finalize()  

  meshcat_vis = MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)
  diagram = builder.Build()
  context = diagram.CreateDefaultContext()

  return plant, scene_graph, diagram, context

# Now we'll use this as a global variable. 
drake_params = setup_grasp_diagram()

def draw_grasp_candidate(X_G, prefix='gripper', refresh=False):
  plant, scene_graph, diagram, context = drake_params
  if (refresh):
    meshcat.Delete()

  plant_context = plant.GetMyContextFromRoot(context)
  plant.SetFreeBodyPose(plant_context, 
                        plant.GetBodyByName("body"), X_G)
  diagram.Publish(context)

  X_G = plant.GetFreeBodyPose(plant_context,
                        plant.GetBodyByName("body"))
  
def draw_grasp_candidates(X_G, prefix='gripper', draw_frames=True):
  builder = DiagramBuilder()
  plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
  parser = Parser(plant)
  gripper = parser.AddModelFromFile(FindResource(
      "models/schunk_wsg_50_welded_fingers.sdf"), "gripper")
  plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("body"), X_G)
  if draw_frames:
      AddMultibodyTriad(plant.GetFrameByName("body"), scene_graph)
  plant.Finalize()
  
  meshcat_vis = MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)
  diagram = builder.Build()
  context = diagram.CreateDefaultContext()
  diagram.Publish(context)

def compute_sdf(pcd, X_G, visualize=False):
  plant, scene_graph, diagram, context = drake_params
  plant_context = plant.GetMyContextFromRoot(context)
  scene_graph_context = scene_graph.GetMyContextFromRoot(context)
  plant.SetFreeBodyPose(plant_context, 
                        plant.GetBodyByName("body"), X_G)
  
  if (visualize):
      diagram.Publish(context)

  query_object = scene_graph.get_query_output_port().Eval(scene_graph_context)

  pcd_sdf = np.inf 
  for pt in pcd.xyzs().T:
    distances = query_object.ComputeSignedDistanceToPoint(pt)
    for body_index in range(len(distances)):
      distance = distances[body_index].distance
      if distance < pcd_sdf:
        pcd_sdf = distance

  return pcd_sdf 

def check_collision(pcd, X_G, visualize=False):
  sdf = compute_sdf(pcd, X_G, visualize)
  return (sdf > 0)


# ## Grasp Candidate based on Local Curvature 
# 
# This is an implementation-heavy assignment, where we will implement a variation of the grasp candidate sampling algorithm on [this paper](https://arxiv.org/pdf/1706.09911.pdf). from 2017. Parts of the [library](https://github.com/atenpas/gpg) based on the paper, which the authors have named "Grasp Pose Generator" (GPG), is used in real grasp selection systems including the one being run at Toyota Research Institute. 
# 
# As opposed to sampling candidate grasp poses using the "antipodal heuristic", this sampling algorithm uses a heuristic based on the local curvature. This heursitic can work quite well especially for smoother / symmetrical objects which has relatively consistent curvature characteristics. 
# 

# ## Computing the Darboux Frame
# 
# First, let's work on formalizing our notion of a "local curvature" by bringing up the [**Darboux Frame**](https://en.wikipedia.org/wiki/Darboux_frame) from differential geometry. It has a fancy French name (after its creator), but the concept is quite simple.
# 
# Given a point $p\in\mathbb{R}^3$ on a differentiable surface $\mathcal{S}\subset\mathbb{R}^3$, we've seen that we can compute the normal vector at point $p$. Let's denote this vector as $n(p)$. 
# 
# The Darboux frame first aligns the $y$-axis with the inward normal vector, and aligns the $x$ and $z$ axis with principal axii of the tangent surface given the curvature. We will define the axis as 
# - x-axis: aligned with the major axis of curvature at point $p$.
# - y-axis: aligned with the inward normal vector at point $p$.
# - z-axis: aligned with the minor axis of curvature at point $p$. 
# 
# Where major axis of curvature has a smaller radius of curvature compared to the minor axis. The below figure might clear things up. 
# 
# <img src="https://raw.githubusercontent.com/RussTedrake/manipulation/master/figures/exercises/darboux_frame.png" width="400">

# Below, your job is to compute the RigidTransform from the world to the Darboux frame of a specific point on the pointcloud. 
# 
# Here is a simple outline of the algorithm that we've seeen in class:
# 1. Compute the set of points $\mathcal{S}$ around the given point using [`kdtree.query`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html), with `ball_radius` as the distance upper bound.  
# 2. Compute the $3\times3$ matrix with sum of outer-products of the normal vectors. 
# $$\mathbf{N}=\sum_{p\in\mathcal{S}} n(p)n^T(p)$$
# 3. Run eigen decomposition and get the eigenvectors using `np.linalg.eig`. Denote the eigen vectors as $[v_1, v_2, v_3]$, in order of decreasing corresponding eigenvalues. Convince yourself that:
# - $v_1$ is the normal vector,
# - $v_2$ is the major tangent vector, 
# - $v_3$ is the minor tangent vector. 
# Note that `np.linalg.eig` does **not** necessarily return the eigenvectors in the correct order. (The function `np.argsort` may come in handy.)
# 4. If $v_1$ is heading outwards (same direction as $n(p)$), negate $v_1$. (You can check this using the dot product.)
# 5. Using $v_1,v_2,v_3$, construct the Rotation matrix by horizontally stacking the vertical vectors: $\mathbf{R} = [v_2 | v_1 | v_3]$
# 6. If the rotation is improper, negate $v_2$. (You can check this by checking the sign of the determinant.)
# 5. Return a `RigidTransform` that has the rotation set as defined in the figure above, and translation defined at the desired point.
# 
# The [textbook example on normal estimation](https://manipulation.csail.mit.edu/clutter.html#normal_estimation) may be useful to reference in this problem.
# 
# NOTE: Convince yourself of the following: if you knew the orthonormal basis vectors of a frame ${}^W[i,j,k]$, then the Rotation matrix of of that frame with respect to the world ${}^W\mathbf{R}^F$ can be computed by horizontally stacking the vertical vectors ($[i|j|k]$). Why would this be? (This doesn't necessarily mean the eigenvector matrix is always a rotation matrix due to improper rotations)

# In[ ]:


def compute_darboux_frame(index, pcd, kdtree, ball_radius=0.002, max_nn=50):
    """
    Given a index of the pointcloud, return a RigidTransform from world to the 
    Darboux frame at that point.
    Args: 
    - index (int): index of the pointcloud. 
    - pcd (PointCloud object): pointcloud of the object.
    - kdtree (scipy.spatial.KDTree object): kd tree to use for nn search. 
    - ball_radius (float): ball_radius used for nearest-neighbors search 
    - max_nn (int): maximum number of points considered in nearest-neighbors search. 
    """
    points = pcd.xyzs() # 3xN np array of points
    normals = pcd.normals() # 3xN np array of normals

    # Fill in your code here. 
    X_WF = RigidTransform() # modify here.
    
    return X_WF


# You can check your work by running the cell below and looking at the frame visualization in Meshcat. 

# In[ ]:


# 151, 11121 are pretty good verifiers of the implementation.
index = 151
meshcat.Delete() 

# Build KD tree.
kdtree = KDTree(pcd.xyzs().T)
X_WP = compute_darboux_frame(index, pcd, kdtree)
print(X_WP.GetAsMatrix4())
meshcat.SetObject("cloud", pcd)
AddMeshcatTriad(meshcat, "frame", length=0.025, radius=0.001, X_PT=X_WP)


# ## Collision Line Search 
# 
# Now we wish to align our gripper frame with the Darboux frame that we found, but naively doing it will result in collision / being too far from the object.
# 
# An important heuristic that is used in the GPG work is that grasps are more stable when contact area is maximized. For that, we would need the gripper to be as inwards as possible towards the object but avoid collisions.
# 
# To implement this, we will use a line search along a grid along the y-axis, and find the **maximum** value of $y$ (remember that our $y$ is towards the inwards normal) that results in no-collision. 
# 
# We've given you the grid you should search over, and the function `distance=compute_sdf(pcd, X_WG)` that will return the signed distance function between the set of pointclouds, and the gripper, given the transform `X_WG`. You are required to use this to detect the presence of collisions. 
# 
# Finally, if there is no value of $y$ that results in no collisions, you should return `np.nan` for the signed distance, and `None` for the rigid transform. 

# In[ ]:


# Compute static rotation between the frame and the gripper. 
def find_minimum_distance(pcd, X_WG):
  """
  By doing line search, compute the maximum allowable distance along the y axis before penetration.
  Return the maximum distance, as well as the new transform.
  Args:
    - pcd (PointCloud object): pointcloud of the object.
    - X_WG (Drake RigidTransform object): RigidTransform. You can expect this to be the return from compute_darboux_frame.  
  Return:
    - Tuple (signed_distance, X_WGnew) where
    - signed_distance (float): signed distance between gripper and object pointcloud at X_WGnew. 
    - X_WGnew: New rigid transform that moves X_WG along the y axis while maximizing the y-translation subject to no collision. 
    If there is no value of y that results in no collisions, return (np.nan, None). 
  """
  y_grid = np.linspace(-0.05, 0.05, 10) # do not modify 

  # modify here. 
  signed_distance = 0.0 # modify here 
  X_WGnew = RigidTransform() # modify here

  return signed_distance, X_WGnew


# You can check your work below by running the cell below. If the visualization results in a collision, or the gripper is excessively far from the object, your implementation is probably wrong. 

# In[ ]:


meshcat.Delete()
meshcat.SetObject("cloud", pcd, point_size=0.001)
AddMeshcatTriad(meshcat, "frame", length=0.025, radius=0.001, X_PT=X_WP)
shortest_distance, X_WGnew = find_minimum_distance(pcd, X_WP)
draw_grasp_candidate(X_WGnew, refresh=False)


# ## Nonempty Grasp 
# 
# Let's add one more heuristic: when we close the gripper, we don't want what is in between the two fingers to be an empty region. That would make our robot look not very smart! 
# 
# There is a simple way to check this: let's define a volumetric region swept by the gripper's closing trajectory, and call it $\mathcal{B}(^{W}X^{G})$. We will also call the gripper body (when fully open) as the set $\mathcal{C}(^{W}X^G)$. If there are no object pointclouds within the set $\mathcal{B}(^{W}X^{G})$, we can simply discard it. 
# 
# <img src="https://raw.githubusercontent.com/RussTedrake/manipulation/master/figures/exercises/closing_plane.png" width="800">
# 
# You're probably thinking - how do I do a rigid transform on a set? Generally it's doable if the transform is affine, the set is polytopic, etc., but there is an easier trick - we just transform all the pointclouds to the gripper frame $G$! 
# 
# The function below follows these steps:
#   1. Transform the pointcloud points `pcd` from world frame to gripper frame.
#   2. For each point, check if it is within the bounding box we have provided.
#   3. If there is a point inside the set, return True. If not, return false. 

# In[ ]:


def check_nonempty(pcd, X_WG, visualize=False):
  """
  Check if the "closing region" of the gripper is nonempty by transforming the pointclouds to gripper coordinates. 
  Args:
    - pcd (PointCloud object): pointcloud of the object.
    - X_WG (Drake RigidTransform): transform of the gripper.
  Return:
    - is_nonempty (boolean): boolean set to True if there is a point within the cropped region. 
  """
  pcd_W_np = pcd.xyzs() 

  # Bounding box of the closing region written in the coordinate frame of the gripper body. 
  # Do not modify 
  crop_min = [-0.054, 0.036, -0.01]
  crop_max = [0.054, 0.117, 0.01]

  # Transform the pointcloud to gripper frame. 
  X_GW = X_WG.inverse()
  pcd_G_np = X_GW.multiply(pcd_W_np)

  # Check if there are any points within the cropped region. 
  indices = np.all((crop_min[0] <= pcd_G_np[0,:], pcd_G_np[0,:] <= crop_max[0],
                    crop_min[1] <= pcd_G_np[1,:], pcd_G_np[1,:] <= crop_max[1],
                    crop_min[2] <= pcd_G_np[2,:], pcd_G_np[2,:] <= crop_max[2]),
                   axis = 0)
  
  is_nonempty = indices.any()

  if (visualize):
    meshcat.Delete()
    pcd_G = PointCloud(pcd) 
    pcd_G.mutable_xyzs()[:] = pcd_G_np

    draw_grasp_candidate(RigidTransform())
    meshcat.SetObject("cloud", pcd_G)
    
    box_length = np.array(crop_max) - np.array(crop_min)
    box_center = (np.array(crop_max) + np.array(crop_min)) / 2. 
    meshcat.SetObject("closing_region", Box(
        box_length[0], box_length[1], box_length[2]), Rgba(1, 0, 0, 0.3))
    meshcat.SetTransform("closing_region", RigidTransform(box_center))

  return is_nonempty 


# The following cell demonstrates the functionality of `check_nonempty`, where we have visualized the pointclouds and $\mathcal{B}({}^W X^G)$ from the gripper frame. 

# In[ ]:


# Lower and upper bounds of the closing region in gripper coordinates. Do not modify. 
check_nonempty(pcd, X_WGnew, visualize=True)


# ## Grasp Sampling Algorithm
# 
# That was a lot of subcomponents, but we're finally onto the grand assembly. You will now generate `candidate_num` candidate grasps using everything we have written so far. The sampling algorithm goes as follows:
# 
# 1. Select a random point $p$ from the pointcloud (use `np.random.randint()`)
# 2. Compute the Darboux frame ${}^WX^F(p)$ of the point $p$ using `compute_darboux_frame`. 
# 3. Randomly sample an $x$ direction translation $x\in[x_{min},x_{max}]$, and a $z$ direction rotation $\phi\in[\phi_{min},\phi_{max}]$. Compute a grasp frame $T$ that has the relative transformation `X_FT=(RotateZ(phi),TranslateX(x))`. Convince yourself this makes the point $p$ stay in the "closing plane" (drawn in red) defined in the figure above. (NOTE: For ease of grading, make sure you compute the $x$ direction first with `np.random.rand()`, then compute the $\phi$ direction with another call to `np.random.rand()`, not the other way around.) 
# 4. From the grasp frame $T$, translate along the $y$ axis such that the gripper is closest to the object without collision. Use `find_minimum_distance`, and call this frame $G$. Remember that `find_minimum_distance` can return `np.nan`. Skip the loop if this happens. 
# 5. If $G$ results in no collisions (see `check_collision`) and results in non-empty grasp (use `check_nonempty`), append it to the candidate list. If not, continue the loop until we have desired number of candidates. 
# 

# In[ ]:


def compute_candidate_grasps(pcd, candidate_num = 10, random_seed=5):
    """
    Compute candidate grasps. 
    Args:
        - pcd (PointCloud object): pointcloud of the object.
        - candidate_num (int) : number of desired candidates. 
        - random_seed (int) : seed for rng, used for grading. 
    Return:
        - candidate_lst (list of drake RigidTransforms) : candidate list of grasps. 
    """

    # Do not modify.
    x_min = -0.03
    x_max = 0.03
    phi_min = -np.pi/3
    phi_max = np.pi/3
    np.random.seed(random_seed)

    # Build KD tree for the pointcloud. 
    kdtree = KDTree(pcd.xyzs().T)
    ball_radius = 0.002

    candidate_count = 0 
    candidate_lst = [] # list of candidates, given by RigidTransforms. 

    # Modify from here. 

    
    return candidate_lst


# You can check your implementation by running the cell below. Note that although we've only sampled 20 candidates, a lot of them look promising. 

# In[ ]:


pcd_downsampled = pcd.VoxelizedDownSample(voxel_size=0.005)

if running_as_notebook:
    grasp_candidates = compute_candidate_grasps(pcd_downsampled, candidate_num=3, random_seed=5)

    meshcat.Delete()
    meshcat.SetObject("cloud", pcd_downsampled)
    for i in range(len(grasp_candidates)):
        draw_grasp_candidates(
            grasp_candidates[i], prefix="gripper" + str(i), draw_frames=False)


# ## Note on Running Time
# 
# You might be disappointed in how slowly this runs, but the same algorithm written in C++ with optimized libraries can run much faster. (I would expect around a 20 times speedup). 
# 
# But more fundamentally, it's important to note how trivially parallelizable the candidate sampling process is. With a parallelized and optimized implementation, hundreds of grasp candidates can be sampled in real time.

# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do two things. 
# - Download and submit the notebook `grasp_candidate.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [4 pts] `compute_darboux_frame` must be implemented correctly.
# - [4 pts] `find_minimum_distance` must be implemented correctly.
# - [4 pts] `compute_candidate_grasps` must be implemented correctly.

# In[ ]:


from manipulation.exercises.clutter.test_grasp_candidate import TestGraspCandidate
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestGraspCandidate], [locals()], 'results.json')
Grader.print_test_results('results.json')


# In[ ]:




