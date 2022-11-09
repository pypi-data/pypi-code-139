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

# # Bunny ICP

# In[ ]:


# Imports
import numpy as np
from manipulation import FindResource, running_as_notebook
from pydrake.all import (PointCloud, Rgba, RigidTransform, RotationMatrix,
                         StartMeshcat)
from scipy.spatial import KDTree


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# ## Problem Description
# In the lecture, we learned about the Iterative Closest Point (ICP) algorithm. In this exercise, you will implement the ICP algorithm to solve the standard Stanford Bunny problem!
# 
# **These are the main steps of the exercise:**
# 1. Implement the ```least_squares_transform``` function to optimize transformation given correspondence
# 2. Implement the ```icp``` algorithm using the functions implemented above.
# 
# Let's first visualize the point clouds of Stanford bunny in meshcat!

# In[ ]:


# Visualize Stanford Bunny 
xyzs = np.load(FindResource('models/bunny/bunny.npy'))
cloud = PointCloud(xyzs.shape[1])
cloud.mutable_xyzs()[:] = xyzs

# Pose for the blue bunny
X_blue = RigidTransform(RotationMatrix.MakeXRotation(np.pi/6), [-.1, .1, .1])

pointcloud_model = xyzs
pointcloud_scene = X_blue.multiply(xyzs)

meshcat.Delete()
meshcat.SetProperty("/Background",'visible', False)
meshcat.SetProperty("/Cameras/default/rotated/<object>","zoom", 10.5)
meshcat.SetObject("red_bunny", cloud, point_size=0.01, rgba=Rgba(1.0, 0, 0))
meshcat.SetTransform("red_bunny", RigidTransform())
meshcat.SetObject("blue_bunny", cloud, point_size=0.01, rgba=Rgba(0, 0, 1.0))
meshcat.SetTransform("blue_bunny", X_blue)


# ## Point cloud registration with known correspondences
# 
# In this section, you will follow the [derivation](http://manipulation.csail.mit.edu/pose.html#registration) to solve the optimization problem below. 
# 
# $$\begin{aligned} \min_{p\in\mathbb{R}^3,R\in\mathbb{R}^{3\times3}} \quad & \sum_{i=1}^{N_s} \| p + R \hspace{.1cm} {^Op^{m_{c_i}}} - p^{s_i}\|^2, \\ s.t. \quad & RR^T = I, \quad \det(R)=1\end{aligned}$$
#     
# The goal is to find the transform that registers the point clouds of the model and the scene, assuming the correspondence is known.  You may refer to the implementation from [deepnote](https://deepnote.com/workspace/Manipulation-ac8201a1-470a-4c77-afd0-2cc45bc229ff/project/4-Geometric-Pose-Estimation-cc6340f5-374e-449a-a195-839a3cedec4a/%2Ficp.ipynb) and the explanation from [textbook](http://manipulation.csail.mit.edu/pose.html#icp).
# 
# In the cell below, implement the ```least_squares_transform``` nethod.

# In[ ]:


def least_squares_transform(scene, model) -> RigidTransform:
    '''
    Calculates the least-squares best-fit transform that maps corresponding
    points scene to model.
    Args:
      scene: 3xN numpy array of corresponding points
      model: 3xM numpy array of corresponding points
    Returns:
      X_BA: A RigidTransform object that maps point_cloud_A on to point_cloud_B 
            such that
                        X_BA.multiply(model) ~= scene,
    '''
    X_BA = RigidTransform()
    ##################
    # your code here
    ##################
    return X_BA


# In[ ]:


def least_squares_transform(scene, model) -> RigidTransform:
    '''
    Calculates the least-squares best-fit transform that maps corresponding
    points scene to model.
    Args:
      scene: 3xN numpy array of corresponding points
      model: 3xM numpy array of corresponding points
    Returns:
      X_BA: A RigidTransform object that maps point_cloud_A on to point_cloud_B 
            such that
                        X_BA.multiply(model) ~= scene,
    '''
    # number of dimensions
    X_BA = RigidTransform()

    # your code here
    ##################
    mu_m = np.mean(model, axis=1)
    mu_s = np.mean(scene, axis=1)

    W = (scene.T - mu_s).T @ (model.T - mu_m)
    U, Sigma, Vh = np.linalg.svd(W)
    R_star = U @ Vh

    if np.linalg.det(R_star) < 0:
        Vh[-1] *= -1
        R_star = U @ Vh

    t_star = mu_s - R_star @ mu_m

    X_BA.set_rotation(RotationMatrix(R_star))
    X_BA.set_translation(t_star)
    ##################

    return X_BA


# ## Point correspondence from closest point
# The ```least_squares_transform``` function assumes that the point correspondence is known. Unfortunately, this is often not the case, so we will have to estimate the point correspondence as well. A common heuristics for estimating point correspondence is the closest point/nearest neighbor. 
# 
# We have implemented the closest neighbors using [scipy's implementation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html) of [k-d trees](https://en.wikipedia.org/wiki/K-d_tree).

# In[ ]:


def nearest_neighbors(scene, model):
    '''
    Find the nearest (Euclidean) neighbor in model for each
    point in scene
    Args:
        scene: 3xN numpy array of points
        model: 3xM numpy array of points
    Returns:
        distances: (N, ) numpy array of Euclidean distances from each point in
            scene to its nearest neighbor in model.
        indices: (N, ) numpy array of the indices in model of each
            scene point's nearest neighbor - these are the c_i's
    '''
    distances = np.empty(scene.shape[1], dtype=float)
    indices = np.empty(scene.shape[1], dtype=int)
    
    kdtree = KDTree(model.T)
    for i in range(model.shape[1]):
        distances[i], indices[i] = kdtree.query(scene[:,i], 1)

    return distances, indices


# ## Iterative Closest Point (ICP)
# Now you should be able to register two point clouds iteratively by first finding/updating the estimate of point correspondence with ```nearest_neighbors``` and then computing the transform using ```least_squares_transform```. You may refer to the explanation from [textbook](http://manipulation.csail.mit.edu/pose.html#icp).
# 
# **In the cell below, complete the implementation of ICP algorithm using the  ```nearest_neighbors``` and ```least_squares_transform``` methods from above.**

# In[ ]:


def icp(scene, model, max_iterations=20, tolerance=1e-3):
    '''
    Perform ICP to return the correct relative transform between two set of points.
    Args:
        scene: 3xN numpy array of points
        model: 3xM numpy array of points
        max_iterations: max amount of iterations the algorithm can perform.
        tolerance: tolerance before the algorithm converges.
    Returns:
      X_BA: A RigidTransform object that maps point_cloud_A on to point_cloud_B 
            such that
                        X_BA.multiply(model) ~= scene,
      mean_error: Mean of all pairwise distances. 
      num_iters: Number of iterations it took the ICP to converge. 
    '''
    X_BA = RigidTransform()

    mean_error = 0
    num_iters = 0
    prev_error = 0
    
    while True:
        num_iters += 1  
          
        # your code here
        ##################

        mean_error = np.inf # Modify to add mean error.
        ##################

        if abs(mean_error - prev_error) < tolerance or num_iters >= max_iterations:
            break

        prev_error = mean_error

        meshcat.SetTransform("red_bunny", X_BA)

    return X_BA, mean_error, num_iters


# In[ ]:


def icp(scene, model, max_iterations=20, tolerance=1e-3):
    '''
    Perform ICP to return the correct relative transform between two set of points.
    Args:
        scene: 3xN numpy array of points
        model: 3xM numpy array of points
        max_iterations: max amount of iterations the algorithm can perform.
        tolerance: tolerance before the algorithm converges.
    Returns:
      X_BA: A RigidTransform object that maps point_cloud_A on to point_cloud_B 
            such that
                        X_BA.multiply(model) ~= scene,
      mean_error: Mean of all pairwise distances. 
      num_iters: Number of iterations it took the ICP to converge. 
    '''
    X_BA = RigidTransform()

    mean_error = 0
    num_iters = 0
    prev_error = 0

    while True:
        num_iters += 1  

        distances, indices = nearest_neighbors(scene, X_BA.multiply(model))
        X_BA = RigidTransform(least_squares_transform(scene, model[:,indices]))
        mean_error = np.mean(distances)

        if abs(mean_error - prev_error) < tolerance or num_iters >= max_iterations:
            break
        prev_error = mean_error

        # TODO(russt): Make this an animation
        meshcat.SetTransform("red_bunny", X_BA)


    return X_BA, mean_error, num_iters


# Now you should be able to visualize the registration of the Stanford bunny! Have fun!

# In[ ]:


icp(pointcloud_scene, pointcloud_model, max_iterations=30, tolerance=1e-5);


# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must: 
# - Download and submit the notebook `bunny_icp.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [3 pts] `least_squares_transform` must be implemented correctly. 
# - [3 pts] `icp` must be implemented correctly.

# In[ ]:


from manipulation.exercises.pose.test_icp import TestICP
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestICP], [locals()], 'results.json')
Grader.print_test_results('results.json')


# In[ ]:




