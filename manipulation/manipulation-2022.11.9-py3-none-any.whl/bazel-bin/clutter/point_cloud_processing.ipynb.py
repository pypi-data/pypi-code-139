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
from pydrake.all import (Box, Concatenate, PointCloud, RotationMatrix,
                         StartMeshcat)

from manipulation.mustard_depth_camera_example import MustardExampleSystem


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Point cloud processing
# 
# I've produced a scene with multiple cameras looking at our favorite YCB mustard bottle.  I've taken the individual point clouds, estimated their normals, merged the point clouds, cropped then point clouds (to get rid of the geometry from the other cameras), then down-sampled the point clouds.  (The order is important!)
# 
# I've pushed all of the point clouds to meshcat, but with many of them set to not be visible by default.  Use the drop-down menu to turn them on and off, and make sure you understand basically what is happening on each of the steps.

# In[ ]:


def point_cloud_processing_example():
    # This just sets up our mustard bottle with three depth cameras positioned
    # around it.
    system = MustardExampleSystem()

    plant = system.GetSubsystemByName("plant")

    # Evaluate the camera output ports to get the images.
    context = system.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    meshcat.Delete()
    meshcat.SetProperty("/Background", "visible", False)

    pcd = []
    for i in range(3):
        cloud = system.GetOutputPort(f"camera{i}_point_cloud").Eval(
            context)
        meshcat.SetObject(f"pointcloud{i}", cloud, point_size=0.001)
        meshcat.SetProperty(f"pointcloud{i}", "visible", False)

        # Crop to region of interest.
        pcd.append(cloud.Crop(lower_xyz=[-.3, -.3, -.3], upper_xyz=[.3, .3,
                                                                    .3]))
        meshcat.SetObject(f"pointcloud{i}_cropped", pcd[i], point_size=0.001)
        meshcat.SetProperty(f"pointcloud{i}_cropped", "visible", False)

        pcd[i].EstimateNormals(radius=0.1, num_closest=30)

        camera = plant.GetModelInstanceByName(f"camera{i}")
        body = plant.GetBodyByName("base", camera)
        X_C = plant.EvalBodyPoseInWorld(plant_context, body)
        pcd[i].FlipNormalsTowardPoint(X_C.translation())

    # Merge point clouds.  (Note: You might need something more clever here for
    # noisier point clouds; but this can often work!)
    merged_pcd = Concatenate(pcd)
    meshcat.SetObject("merged", merged_pcd, point_size=0.001)

    # Voxelize down-sample.  (Note that the normals still look reasonable)
    down_sampled_pcd = merged_pcd.VoxelizedDownSample(voxel_size=0.005)
    meshcat.SetObject("down_sampled", down_sampled_pcd, point_size=0.001)
    meshcat.SetLineSegments(
        "down_sampled_normals", down_sampled_pcd.xyzs(),
        down_sampled_pcd.xyzs() + 0.01 * down_sampled_pcd.normals())

point_cloud_processing_example()


# In[ ]:




