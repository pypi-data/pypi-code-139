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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/trajectories.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import time

import numpy as np
from pydrake.all import (AddMultibodyPlantSceneGraph, Box, DiagramBuilder,
                         MeshcatVisualizer, RigidTransform, StartMeshcat)

from manipulation import running_as_notebook
from manipulation.scenarios import AddShape


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Basic RRT
# 
# Note that I've inserted a `sleep` command in the visualization to slow things down so you can watch the tree grow.
# 
# TODO(russt): Consider adding the voronoi visualization, but it would add a dependency on scipy.  (That's a big dependency for a little example!)

# In[ ]:


def basic_rrt():
    N = 10000 if running_as_notebook else 3
    Q = np.empty((N,2))
    rng = np.random.default_rng()
    Q[0] = rng.random((1,2))

    meshcat.Delete()
    meshcat.Set2dRenderMode(xmin=0, xmax=1, ymin=0, ymax=1)

    start = np.empty((N,3))
    end = np.empty((N,3))
    id = 0
    for n in range(1,N):
        q_sample = rng.random((1,2))[0]
        distance_sq = np.sum((Q[:n] - q_sample)**2, axis=1)
        closest = np.argmin(distance_sq)
        distance = np.sqrt(distance_sq[closest])
        if (distance > .1):
            q_sample = (Q[closest]+(.1/distance)*(q_sample - Q[closest]))
        start[n] = [Q[closest, 0], 0, Q[closest,1]]
        end[n] = [q_sample[0], 0, q_sample[1]]
        if (n < 1000 and n % 100 == 1) or n % 1000 == 1:
            meshcat.SetLineSegments("rrt", start[:n+1].T, end[:n+1].T)
            time.sleep(0.1)  # sleep to slow things down.
        Q[n] = q_sample

basic_rrt()


# # RRT Bug trap
# 
# For bonus points, I'll use SceneGraph for the collision checking.
# 
# TODO(russt):
# - Take bigger steps, but check collisions at subsamples along an edge.
# - Add a goal + goal-bias
# - Make a version where the robot has geometry, and the collision checks call `plant.SetPosition()`, then `query.HasCollisions()`

# In[ ]:


def rrt_bugtrap():
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    thickness = .05
    MITred = [.6, .2, .2, 1]
    wall = AddShape(plant, Box(.8, 1.0, thickness), "bottom", color=MITred)
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("bottom", wall),
                     RigidTransform([0.5, 0, 0.1+thickness/2]))
    wall = AddShape(plant, Box(0.8, 1.0, thickness), "top", color=MITred)
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("top", wall),
                     RigidTransform([0.5, 0, 0.9-thickness/2]))
    wall = AddShape(plant,
                    Box(thickness, 1.0, .8 - thickness),
                    "left",
                    color=MITred)
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("left", wall),
                     RigidTransform([0.1+thickness/2, 0, 0.5]))
    wall = AddShape(plant, Box(thickness, 1.0, .34), "right_top", color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("right_top", wall),
                     RigidTransform([0.9 - thickness / 2, 0, 0.9 - .17]))
    wall = AddShape(plant,
                    Box(thickness, 1.0, .34),
                    "right_bottom",
                    color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("right_bottom", wall),
                     RigidTransform([0.9 - thickness / 2, 0, 0.1 + .17]))
    wall = AddShape(plant, Box(0.36, 1.0, thickness), "trap_top", color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("trap_top", wall),
                     RigidTransform([0.9 - .18, 0, .9 - thickness / 2 - .33]))
    wall = AddShape(plant, Box(0.36, 1.0, thickness), "trap_bottom", color=MITred)
    plant.WeldFrames(plant.world_frame(),
                     plant.GetFrameByName("trap_bottom", wall),
                     RigidTransform([0.9 - .18, 0, .1 + thickness / 2 + .33]))
    plant.Finalize()

    meshcat.Delete()
    meshcat.Set2dRenderMode(xmin=0, xmax=1, ymin=0, ymax=1)

    visualizer = MeshcatVisualizer.AddToBuilder(
        builder, scene_graph, meshcat)

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    diagram.Publish(context)
    query = scene_graph.get_query_output_port().Eval(
        scene_graph.GetMyContextFromRoot(context))

    q_init = [.3, .3]

    N = 10000 if running_as_notebook else 3
    Q = np.empty((N,2))
    rng = np.random.default_rng()
    Q[0] = q_init

    start = np.empty((N,3))
    end = np.empty((N,3))

    max_length = thickness/4
    n = 1
    while n < N:
        q_sample = rng.random((1,2))[0]
        distance_sq = np.sum((Q[:n] - q_sample)**2, axis=1)
        closest = np.argmin(distance_sq)
        distance = np.sqrt(distance_sq[closest])
        if (distance > max_length):
            q_sample = (Q[closest]+(max_length/distance)*(q_sample - Q[closest]))
        if query.ComputeSignedDistanceToPoint([q_sample[0], 0, q_sample[1]], 0.0):
            # Then the sample point is in collision...
            continue
        start[n] = [Q[closest, 0], 0, Q[closest,1]]
        end[n] = [q_sample[0], 0, q_sample[1]]
        if (n < 1000 and n % 100 == 1) or n % 1000 == 1:
            meshcat.SetLineSegments("rrt", start[:n+1].T, end[:n+1].T)
            time.sleep(0.1)  # sleep to slow things down.

        Q[n] = q_sample
        n += 1


rrt_bugtrap()


# In[ ]:




