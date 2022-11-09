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


import time

import numpy as np
from pydrake.all import (PointCloud, Rgba, RigidTransform, RotationMatrix,
                         Sphere, StartMeshcat)
from scipy.spatial import KDTree

from manipulation import running_as_notebook
from manipulation.meshcat_utils import AddMeshcatTriad
from manipulation.mustard_depth_camera_example import MustardExampleSystem


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Estimating normals (and local curvature)
# 
# TODO: Add the version from depth images (nearest pixels instead of nearest neighbors), and implement it in DepthImageToPointCloud.

# In[ ]:


def normal_estimation():
    system = MustardExampleSystem()
    context = system.CreateDefaultContext()

    meshcat.Delete()
    meshcat.DeleteAddedControls()
    meshcat.SetProperty("/Background", "visible", False)

    point_cloud = system.GetOutputPort("camera0_point_cloud").Eval(context)
    cloud = point_cloud.Crop(lower_xyz=[-.3, -.3, -.3], upper_xyz=[.3, .3, .3])
    meshcat.SetObject("point_cloud", cloud)

    # Extract camera position
    plant = system.GetSubsystemByName("plant")
    p_WC = plant.GetFrameByName("camera0_origin").CalcPoseInWorld(
        plant.GetMyContextFromRoot(context)).translation()

    kdtree = KDTree(cloud.xyzs().T)

    num_closest = 40
    neighbors= PointCloud(num_closest)
    AddMeshcatTriad(meshcat, "least_squares_basis", length=0.03, radius=0.0005)

    meshcat.AddSlider("point",
                      min=0,
                      max=cloud.size() - 1,
                      step=1,
                      value=429, #4165,
                      decrement_keycode="ArrowLeft",
                      increment_keycode="ArrowRight")
    meshcat.AddButton("Stop Normal Estimation", "Escape")
    print(
        "Press ESC or the 'Stop Normal Estimation' button in Meshcat to continue"
    )
    last_index = -1
    while meshcat.GetButtonClicks("Stop Normal Estimation") < 1:
        index = round(meshcat.GetSliderValue("point"))
        if index == last_index:
            time.sleep(.1)
            continue
        last_index = index

        query = cloud.xyz(index)
        meshcat.SetObject("query", Sphere(0.001), Rgba(0, 1, 0))
        meshcat.SetTransform("query", RigidTransform(query))
        (distances, indices) = kdtree.query(query,
                                            k=num_closest,
                                            distance_upper_bound=0.1)

        neighbors.resize(len(distances))
        neighbors.mutable_xyzs()[:] = cloud.xyzs()[:, indices]

        meshcat.SetObject("neighbors", neighbors,
                          rgba=Rgba(0, 0, 1), point_size=0.001)

        neighbor_pts = neighbors.xyzs().T
        pstar = np.mean(neighbor_pts,axis=0)
        prel = neighbor_pts - pstar
        W = np.matmul(prel.T, prel)
        w, V = np.linalg.eigh(W)
        # V[:, 0] corresponds to the smallest eigenvalue, and V[:, 2] to the
        # largest.
        R = np.fliplr(V)
        # R[:, 0] corresponds to the largest eigenvalue, and R[:, 2] to the
        # smallest (the normal).

        # Handle improper rotations
        R = R @ np.diag([1, 1, np.linalg.det(R)])

        # If the normal is not pointing towards the camera...
        if (p_WC - -query).dot(R[:,2]) < 0:
            # then flip the y and z axes.
            R = R @ np.diag([1, -1, -1])

        meshcat.SetTransform("least_squares_basis", RigidTransform(
            RotationMatrix(R), query))

        if not running_as_notebook:
            break

    meshcat.DeleteAddedControls()

normal_estimation()


# In[ ]:




