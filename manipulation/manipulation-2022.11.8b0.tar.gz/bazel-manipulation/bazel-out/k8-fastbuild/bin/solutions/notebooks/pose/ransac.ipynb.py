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

# # Ransac and Outlier Removal

# In[ ]:


import numpy as np
from manipulation import FindResource, running_as_notebook
from pydrake.all import (Cylinder, PointCloud, Rgba, RigidTransform,
                         RollPitchYaw, RotationMatrix, StartMeshcat)


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()
meshcat.SetProperty("/Background",'visible', False)
meshcat.SetProperty("/Cameras/default/rotated/<object>","zoom", 10.5)


# In[ ]:


# Visualize Stanford Bunny 
xyzs = np.load(FindResource('models/bunny/bunny.npy'))

# point clouds of planar surface
grid_spec = 50
xy_axis = np.linspace(-0.5, 0.5, grid_spec)
plane_x, plane_y = np.meshgrid(xy_axis, xy_axis)
points_plane_xy = np.c_[plane_x.flatten(), plane_y.flatten(), 
                        np.zeros(grid_spec**2)]
bunny_w_plane = np.c_[points_plane_xy.T, xyzs]

def fit_plane(xyzs):
    '''
    Args:
      xyzs is (3, N) numpy array
    Returns:
      (4,) numpy array
    '''
    center = np.mean(xyzs, axis=1)
    cxyzs = xyzs.T - center
    U, S, V = np.linalg.svd(cxyzs)
    normal = V[-1]              # last row of V
    d = -center.dot(normal)
    plane_equation = np.hstack([normal, d])
    return plane_equation

# visualize a facet
def DrawFacet(abcd, name, center=None):
    # TODO(russt): Clean up the math in here.
    normal = np.array(abcd[:3]).astype(float)
    normal /= np.linalg.norm(normal)
    d = -abcd[3] / np.linalg.norm(normal)

    R = np.eye(3)
    R[:, 2] = normal
    z = normal
    if abs(z[0]) < 1e-8:
        x = np.array([0, -normal[2], normal[1]])
    else:
        x = np.array([-normal[1], normal[0], 0])
    x /= np.linalg.norm(x)
    R[:, 0] = x
    R[:, 1] = np.cross(z, x)

    X = np.eye(4)
    Rz = RollPitchYaw(np.pi/2, 0, 0).ToRotationMatrix().matrix()
    X[:3, :3] = R.dot(Rz)
    if center is None:
        X[:3, 3] = d * normal
    else:
        X[:3, 3] = center
              
    meshcat.SetObject("facets/"+name+"/plane", Cylinder(0.1, 0.005))
    meshcat.SetTransform("facets/"+name+"/plane", RigidTransform(X) @ RigidTransform(RotationMatrix.MakeXRotation(np.pi / 2.0)))
    
    meshcat.SetObject("facets/" + name + "/normal",
                      Cylinder(0.001, 0.2), Rgba(0, 0, 1))
    meshcat.SetTransform("facets/" + name + "/normal", RigidTransform(X) @ RigidTransform(RotationMatrix.MakeXRotation(np.pi / 2.0), [0, .1, 0]))

def visualize_point_clouds(points, name):
  cloud = PointCloud(points.shape[1])
  cloud.mutable_xyzs()[:] = points
  meshcat.SetObject(name, cloud, point_size=0.01, rgba=Rgba(1.0, 0, 0))


# # Problem Description
# In the lecture, we learned about the RANSAC algorithm. In this exercise, you will implement the RANSAC algorithm to separate the Stanford bunny from its environment!
# 
# **These are the main steps of the exercise:**
# 1. Implement the `ransac` method.
# 2. Implement the `remove_plane` method to remove the points that belong to the planar surface.
# 
# Let's first visualize the point clouds of Stanford bunny in meshcat!

# In[ ]:


visualize_point_clouds(bunny_w_plane, "bunny_w_plane")


# You should notice that now there is a planar surface underneath the bunny. You may assume the bunny is currently placed on a table, where the planar surface is the tabletop. In this exercise, your objective is to remove the planar surface.

# A straightforward way to achieve a better fit is to remove the planar surface underneath the bunny. To do so, we provide you a function to fit a planar surface. 
# 
# Recall that a plane equation is of the form
# $$a x + b y + c z + d = 0$$
# where $[a,b,c]^T$ is a vector normal to the plane and (if it's a unit normal) $d$ is the negative of the distance from the origin to the plane in the direction of the normal.  We'll represent a plane by the vector $[a,b,c,d]$.
# 
# The fitted planes are shown as translucent disks of radius $r$ centered at the points. The gray lines represent the planes' normals.

# In[ ]:


plane_equation = fit_plane(bunny_w_plane)
print(plane_equation)
DrawFacet(plane_equation, 'naive_plane', center=[0,0,-plane_equation[-1]])


# You should notice that the planar surface cannot be fitted exactly either. This is because it takes account of all points in the scene to fit the plane. Since a significant portion of the point cloud belongs to the bunny, the fitted plane is noticeably elevated above the ground. 
# 
# To improve the result of the fitted plane, you will use RANSAC!

# ## RANSAC
# With the presence of outliers (bunny), we can use RANSAC to get more reliable estimates. The idea is to fit a plane using many random choices of a minimal set of points (3), fit a plane for each one, count how many points are within a distance tolerance to that plane (the inliers), and return the estimate with the most inliers.
# 
# **Complete the function `ransac`.  It takes a data matrix, a tolerance, a value of iterations, and a model regressor. It returns an equation constructed by the model regressor and a count of inliers.**

# In[ ]:


def ransac(point_cloud, model_fit_func, tolerance=1e-3, max_iterations=500):
    """
    Args:
      point_cloud is (3, N) numpy array
      tolerance is a float
      max_iterations is a (small) integer
      model_fit_func: the function to fit the model (point clouds)

    Returns:
      (4,) numpy array
    """
    best_ic = 0                 # inlier count
    best_model = np.ones(4)     # plane equation ((4,) array)

    ##################
    # your code here
    ##################

    return  best_ic, best_model


# In[ ]:


def ransac(point_cloud, model_fit_func, tolerance=1e-3, max_iterations=500):
    """
    Args:
      point_cloud is (3, N) numpy array
      tolerance is a float
      max_iterations is a (small) integer
      model_fit_func: the function to fit the model (point clouds)

    Returns:
      (4,) numpy array
    """
    best_ic = 0                 # inlier count
    best_model = None           # plane equation ((4,) array)
    N = point_cloud.shape[1]           # number of points

    sample_size = 3

    point_cloud_1 = np.ones((N, 4))
    point_cloud_1[:, :3] = point_cloud.T
    for i in range(max_iterations):
        s = point_cloud[:, np.random.randint(N, size=sample_size)]
        m = model_fit_func(s)
        abs_distances = np.abs(np.dot(m, point_cloud_1.T)) # 1 x N
        inliner_count = np.sum(abs_distances < tolerance)

        if inliner_count > best_ic:
            best_ic = inliner_count
            best_model = m

    return  best_ic, best_model


# Now you should have a lot better estimate of the planar surface with the use of RANSAC! Let's visualize the plane now!

# In[ ]:


inlier_count, ransac_plane = ransac(bunny_w_plane, fit_plane, 0.001, 500)
print(ransac_plane)
DrawFacet(ransac_plane, 'ransac_plane', center=[0,0,-ransac_plane[-1]])


# ## Remove Planar Surface
# 
# Now all you need to do is to remove the points that belong to the planar surface. You may do so by rejecting all points that are 
# $$|| a x + b y + c z + d || < tol$$
# 
# Note that since you are fitting a plane, the bunny is this case is the "outlier". Your job, however, is to keep the bunny and remove the planar surface.
# 
# **Complete the function below to remove the points that belongs to the planar surface**.

# In[ ]:


def remove_plane(point_cloud, ransac, tol=1e-4):
    """
    Args:
        point_cloud: 3xN numpy array of points
        ransac: The RANSAC function to use (call ransac(args))
        tol: points less than this distance tolerance should be removed
    Returns:
        point_cloud_wo_plane: 3xN numpy array of points
    """
    point_cloud_wo_plane = np.zeros((3,100))
    return point_cloud_wo_plane


# In[ ]:


def remove_plane(point_cloud, ransac_method, tol=1e-4):
    """
    Args:
        point_cloud: 3xN numpy array of points
        ransac: The RANSAC function to use (call ransac(args))
        tol: points less than this distance tolerance should be removed
    Returns:
        point_cloud_wo_plane: 3xN numpy array of points
    """
    inlier_count, plane_equation = ransac_method(point_cloud, fit_plane, 0.001, 500)
    
    point_cloud_wo_plane = []
    
    dst = plane_equation[0:3].dot(point_cloud) + plane_equation[3]
    
    for i in range(len(dst)):
        if abs(dst[i]) > tol:
            point_cloud_wo_plane.append(point_cloud[:,i])
    
    return np.asarray(point_cloud_wo_plane).T


# In[ ]:


meshcat.Delete()
bunny_wo_plane = remove_plane(bunny_w_plane, ransac)
visualize_point_clouds(bunny_wo_plane, "bunny")


# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must: 
# - Download and submit the notebook `ransac.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [4 pts] `ransac` must be implemented correctly. 
# - [2 pts] `remove_plane` must be implemented correctly.

# In[ ]:


from manipulation.exercises.pose.test_ransac import TestRANSAC
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestRANSAC], [locals()], 'results.json')
Grader.print_test_results('results.json')


# In[ ]:




