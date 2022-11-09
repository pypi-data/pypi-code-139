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


from functools import partial

import numpy as np
from pydrake.all import (AddMultibodyPlantSceneGraph, DiagramBuilder,
                         InverseKinematics, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, Rgba, RigidTransform,
                         Solve, Sphere, StartMeshcat)

from manipulation import running_as_notebook
from manipulation.scenarios import AddPlanarIiwa, AddShape, AddWsg
from manipulation.utils import FindResource


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Visualizing the configuration space
# 
# I've got the default sampling resolution set fairly fine; it will take a minute or so to run.

# In[11]:


def draw_configuration_space(shelves=True):
    builder = DiagramBuilder()

    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
    iiwa = AddPlanarIiwa(plant)
    wsg = AddWsg(plant, iiwa, roll=0.0, welded=True)
    sphere = AddShape(plant, Sphere(0.02), "sphere")
    X_WO = RigidTransform([0.6, 0, 0.65])
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("sphere"), X_WO)

    if shelves:
        parser = Parser(plant)
        bin = parser.AddModelFromFile(FindResource("models/shelves.sdf"))
        plant.WeldFrames(plant.world_frame(),
                         plant.GetFrameByName("shelves_body", bin),
                         RigidTransform([0.6, 0, 0.4]))

    plant.Finalize()

    #    visualizer = MeshcatVisualizer.AddToBuilder(
    #        builder,
    #        scene_graph,
    #        meshcat,
    #        MeshcatVisualizerParams(delete_prefix_initialization_event=False))

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMyContextFromRoot(context)

    q0 = plant.GetPositions(plant_context)
    gripper_frame = plant.GetFrameByName("body", wsg)
    sphere_frame = plant.GetFrameByName("sphere", sphere)

    ik = InverseKinematics(plant, plant_context)
    collision_constraint = ik.AddMinimumDistanceConstraint(0.001, 0.01)
    grasp_constraint = ik.AddPositionConstraint(
        gripper_frame, [0, 0.1, 0], sphere_frame, [0, 0, 0], [0, 0, 0])

    prog = ik.get_mutable_prog()
    q = ik.q()
    prog.SetInitialGuess(q, q0)
    result = Solve(ik.prog())
    if not result.is_success():
        print("IK failed")

    diagram.Publish(context)

    def eval(q0, q1, q2, c, tol):
        return float(c.evaluator().CheckSatisfied([q0, q1, q2], tol))

    meshcat.Delete()
    meshcat.SetProperty("/Background", "visible", False)
    meshcat.SetObject("initial_guess", Sphere(0.05), Rgba(.4, 1, 1, 1))
    meshcat.SetTransform("initial_guess", RigidTransform(q0))
    meshcat.SetObject("ik_solution", Sphere(0.05), Rgba(.4, .4, 1, 1))
    meshcat.SetTransform("ik_solution", RigidTransform(result.GetSolution(q)))

    low = plant.GetPositionLowerLimits()
    up = plant.GetPositionUpperLimits()
    N = 70 if running_as_notebook else 5
    vertices, triangles = mcubes.marching_cubes_func(
        tuple(low), tuple(up), N, N, N,
        partial(eval, c=grasp_constraint, tol=0.05), 0.5)
    meshcat.SetTriangleMesh("grasp_constraint", vertices.T, triangles.T,
        Rgba(.5, .9, .5))

    if shelves:
        vertices, triangles = mcubes.marching_cubes_func(
            tuple(low), tuple(up), N, N, N,
            partial(eval, c=collision_constraint, tol=0.0), 0.5)
        meshcat.SetTriangleMesh("collision_constraint",
                                vertices.T, triangles.T, Rgba(.9, .5, .5, 1))

# I've made pymcubes optional (it's a heavy dependency)
try:
    import mcubes
    draw_configuration_space(shelves=True)
except ImportError:
    pass

