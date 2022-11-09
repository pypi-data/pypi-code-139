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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/pose.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import os

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import pydot
from IPython.display import HTML, SVG, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, AngleAxis,
                         BaseField, ConstantValueSource, CsdpSolver,
                         DepthImageToPointCloud, DiagramBuilder,
                         DifferentialInverseKinematicsIntegrator,
                         FindResourceOrThrow, LeafSystem,
                         MakePhongIllustrationProperties, MathematicalProgram,
                         MeshcatPointCloudVisualizer, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, PiecewisePolynomial,
                         PiecewisePose, PointCloud, RigidTransform,
                         RollPitchYaw, RotationMatrix, Simulator, StartMeshcat,
                         ge)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import AddMeshcatTriad, draw_open3d_point_cloud
from manipulation.scenarios import (AddIiwaDifferentialIK, AddMultibodyTriad,
                                    AddRgbdSensor, MakeManipulationStation)
from manipulation.utils import AddPackagePaths, FindResource

if running_as_notebook:
    mpld3.enable_notebook()


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Point cloud registration with known correspondences

# In[ ]:


def MakeRandomObjectModelAndScenePoints(
    num_model_points=20, 
    noise_std=0, 
    num_outliers=0, 
    yaw_O=None,
    p_O=None, 
    num_viewable_points=None, 
    seed=None):
    """ Returns p_Om, p_s """
    random_state = np.random.RandomState(seed)

    # Make a random set of points to define our object in the x,y plane
    theta = np.arange(0, 2.0*np.pi, 2.0*np.pi/num_model_points)
    l = 1.0 + 0.5*np.sin(2.0*theta) + 0.4*random_state.rand(1, num_model_points)
    p_Om = np.vstack((l * np.sin(theta), l * np.cos(theta), 0 * l))

    # Make a random object pose if one is not specified, and apply it to get the scene points.
    if p_O is None:
        p_O = [2.0*random_state.rand(), 2.0*random_state.rand(), 0.0]
    if len(p_O) == 2:
        p_O.append(0.0)
    if yaw_O is None:
        yaw_O = 0.5*random_state.random()
    X_O = RigidTransform(RotationMatrix.MakeZRotation(yaw_O), p_O)
    if num_viewable_points is None:
        num_viewable_points = num_model_points
    assert num_viewable_points <= num_model_points
    p_s = X_O.multiply(p_Om[:,:num_viewable_points])
    p_s[:2, :]  += random_state.normal(scale=noise_std, size=(2, num_viewable_points))
    if num_outliers:
        outliers = random_state.uniform(low=-1.5, high=3.5, size=(3, num_outliers))
        outliers[2,:] = 0
        p_s = np.hstack((p_s, outliers))

    return p_Om, p_s, X_O

def MakeRectangleModelAndScenePoints(
    num_points_per_side=7,
    noise_std=0, 
    num_outliers=0, 
    yaw_O=None,
    p_O=None, 
    num_viewable_points=None, 
    seed=None):
    random_state = np.random.RandomState(seed)
    if p_O is None:
        p_O = [2.0*random_state.rand(), 2.0*random_state.rand(), 0.0]
    if len(p_O) == 2:
        p_O.append(0.0)
    if yaw_O is None:
        yaw_O = 0.5*random_state.random()
    X_O = RigidTransform(RotationMatrix.MakeZRotation(yaw_O), p_O)
    if num_viewable_points is None:
        num_viewable_points = 4*num_points_per_side
    
    x = np.arange(-1, 1, 2/num_points_per_side)
    half_width = 2
    half_height = 1
    top = np.vstack((half_width*x, half_height + 0*x))
    right = np.vstack((half_width + 0*x, -half_height*x))
    bottom = np.vstack((-half_width*x, -half_height + 0*x))
    left = np.vstack((-half_width + 0*x, half_height*x))
    p_Om = np.vstack((np.hstack((top, right, bottom, left)), np.zeros((1, 4*num_points_per_side))))
    p_s = X_O.multiply(p_Om[:,:num_viewable_points])
    p_s[:2, :]  += random_state.normal(scale=noise_std, size=(2, num_viewable_points))
    if num_outliers:
        outliers = random_state.uniform(low=-1.5, high=3.5, size=(3, num_outliers))
        outliers[2,:] = 0
        p_s = np.hstack((p_s, outliers))

    return p_Om, p_s, X_O


def PlotEstimate(p_Om, p_s, Xhat_O=RigidTransform(), chat=None, X_O=None, ax=None):
    p_m = Xhat_O.multiply(p_Om)
    if ax is None:
        ax = plt.subplot()
    Nm = p_Om.shape[1]
    artists = ax.plot(p_m[0, :], p_m[1, :], 'bo')
    artists += ax.fill(p_m[0, :], p_m[1, :], 'lightblue', alpha=0.5)
    artists += ax.plot(p_s[0, :], p_s[1, :], 'ro')
    if chat is not None:
        artists += ax.plot(np.vstack((p_m[0, chat], p_s[0, :])), np.vstack((p_m[1, chat], p_s[1, :])), 'g--')
    if X_O:
        p_s = X_O.multiply(p_Om)
    artists += ax.fill(p_s[0, :Nm], p_s[1, :Nm], 'lightsalmon')
    ax.axis('equal')
    return artists

def PrintResults(X_O, Xhat_O):
    p = X_O.translation()
    aa = X_O.rotation().ToAngleAxis()
    print(f"True position: {p}")
    print(f"True orientation: {aa}")
    p = Xhat_O.translation()
    aa = Xhat_O.rotation().ToAngleAxis()
    print(f"Estimated position: {p}")
    print(f"Estimated orientation: {aa}")

def PoseEstimationGivenCorrespondences(p_Om, p_s, chat):
    """ Returns optimal X_O given the correspondences """
    # Apply correspondences, and transpose data to support numpy broadcasting
    p_Omc = p_Om[:, chat].T
    p_s = p_s.T

    # Calculate the central points
    p_Ombar = p_Omc.mean(axis=0)
    p_sbar = p_s.mean(axis=0)

    # Calculate the "error" terms, and form the data matrix
    merr = p_Omc - p_Ombar
    serr = p_s - p_sbar
    W = np.matmul(serr.T, merr)

    # Compute R
    U, Sigma, Vt = np.linalg.svd(W)
    R = np.matmul(U, Vt)
    if np.linalg.det(R) < 0:
       print("fixing improper rotation")
       Vt[-1, :] *= -1
       R = np.matmul(U, Vt)

    # Compute p
    p = p_sbar - np.matmul(R, p_Ombar)

    return RigidTransform(RotationMatrix(R), p)


p_Om, p_s, X_O = MakeRandomObjectModelAndScenePoints(num_model_points=20)
#p_Om, p_s, X_O = MakeRectangleModelAndScenePoints()
Xhat = RigidTransform()
c = range(p_Om.shape[1])  # perfect, known correspondences
fig, ax = plt.subplots(1, 2)
PlotEstimate(p_Om, p_s, Xhat, c, ax=ax[0])
Xhat = PoseEstimationGivenCorrespondences(p_Om, p_s, c)
ax[1].set_xlim(ax[0].get_xlim())
ax[1].set_ylim(ax[0].get_ylim());
PlotEstimate(p_Om, p_s, Xhat, c, ax=ax[1])
ax[0].set_title('Original Data')
ax[1].set_title('After Registration')
PrintResults(X_O, Xhat)

