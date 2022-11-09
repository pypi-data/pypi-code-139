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

# # Solving for static equilibrium
# This notebook will help you assess in simulation which of the sphere configurations in the problem represent configurations at equilibrium and which. **You do not need to turn in this notebook, and there is no autograded component.** It is just to help you build intuition, show you how to use Drake for problems like this, and check your answers!
# 
# ## Imports and function definitions

# In[ ]:


# python libraries
import numpy as np
import pydrake
from manipulation import running_as_notebook
from manipulation.scenarios import AddShape
from pydrake.all import (AddMultibodyPlantSceneGraph, DiagramBuilder,
                         FixedOffsetFrame, MeshcatVisualizer,
                         RigidTransform, RotationMatrix, Simulator, Solve,
                         Sphere, StartMeshcat, StaticEquilibriumProblem)


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# ## Initialization

# In[ ]:


mu = 0.5
r = 0.3
m = 1

builder = DiagramBuilder()
plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=1e-4)
plant.set_name("plant")

world_offset_frame = pydrake.multibody.tree.FixedOffsetFrame(
                        "world_joint_frame",
                        plant.world_frame(),
                        RigidTransform(
                            RotationMatrix.MakeXRotation(np.pi/2),
                            [0, 0, 0]))
plant.AddFrame(world_offset_frame)

# Create the sphere bodies
spheres = []
sphere_joints = []
for i in range(3):
    sphere_name = "sphere_{}".format(i)

    color = [0, 0, 0, 1]
    color[i] = 1
    spheres.append(AddShape(plant, pydrake.geometry.Sphere(r), name=sphere_name, mass=m, mu=mu, color=color))

    # Set up planar joint
    sphere_joints.append(plant.AddJoint(pydrake.multibody.tree.PlanarJoint(
        "sphere_{}_joint".format(i),
        world_offset_frame,
        plant.GetFrameByName(sphere_name))))

ground = AddShape(plant, pydrake.geometry.Box(10,10,2.0), name="ground", mu=mu)
plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("ground"), RigidTransform(p=[0,0,-1.0]))

plant.Finalize()

visualizer = MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)

diagram = builder.Build()
context = diagram.CreateDefaultContext()
plant_context = plant.GetMyMutableContextFromRoot(context)


# # Using the plant
# This is the main of the notebook for you to edit. (The other spot is where the system parameters are defined near the top of the script.) There are three sections:
# 
# 1. **Initializing your guess for a static equilibrium position**: You can specify the $xyz$ position of each of the sphere. (To answer the question, you'll want to make it match one of the configurations from the problem, but feel free to experiment/try others.)
# 2. **Computing the static equilibrium position**: The `StaticEquilibriumProblem` class allows us to automatically set up the optimization problem for static equilibrium for a given plant. We use this class to compute an actual equilibrium position.
# 3. **Simulating the plant.** Given a configuration for the system, simulate how it evolves over time.

# ## Initializing your guess for a static equilibrium position
# Specify the x and z of the center of mass of each of the spheres. (The spheres are fixed in the $xz$ plane, so that's all you have to specify.)

# In[ ]:


#########
# REPLACE WITH YOUR CODE
guesses = [
    [0, r], # Red sphere xz
    [2*r, r], # Green sphere xz
    [4*r, r] # Blue sphere xz
]
#########


# ### Visualizing your guess
# Run the following cell to see your guess rendered in meshcat. **This does not check for static equilibrium or run any physics simulation,** but it will let you verify you've set your pose how you intended.

# In[ ]:


for i, guess in enumerate(guesses):
    sphere_joints[i].set_translation(plant_context, guess)
diagram.Publish(context)


# ## Computing the static equilibrium position
# This cell computes a static equilibrium postion. If it's close to your original guess, then you initialized the system at equilibrium. If not, your guess is not an equilibrium.

# In[ ]:


# The StaticEquilibriumProblem needs an "autodiff" version of the diagram/multibody plant to 
# use gradient-based optimization.
autodiff_diagram = diagram.ToAutoDiffXd()
autodiff_context = autodiff_diagram.CreateDefaultContext()
autodiff_plant = autodiff_diagram.GetSubsystemByName("plant")
static_equilibrium_problem = StaticEquilibriumProblem(autodiff_plant, autodiff_plant.GetMyContextFromRoot(autodiff_context), set())

initial_guess = np.zeros(plant.num_positions())

for i, guess in enumerate(guesses):
    initial_guess[3*i] = guess[0] # x
    initial_guess[3*i+1] = guess[1] # z

static_equilibrium_problem.get_mutable_prog().SetInitialGuess(
    static_equilibrium_problem.q_vars(), initial_guess)

result = Solve(static_equilibrium_problem.prog())
result.is_success()
q_sol = result.GetSolution(static_equilibrium_problem.q_vars())

for i, guess in enumerate(guesses):
    print("Guess for position of {}:".format(i), guess, "\tEquilibrium position of sphere {}:".format(i), q_sol[3*i:3*i+2])

for wrench in static_equilibrium_problem.GetContactWrenchSolution(result):
    print(f"Spatial force at world position {wrench.p_WCb_W} between {wrench.bodyA_index} and {wrench.bodyB_index}:")
    print(f"  translational: {wrench.F_Cb_W.translational()}")
    print(f"  rotational: {wrench.F_Cb_W.rotational()}")


# ### Visualizing the solution configuration
# This doesn't yet run the dynamics for the system (so the objects won't move), but it *will* update their poses to match the results of `StaticEquilibriumProblem`.

# In[ ]:


plant.SetPositions(plant_context, q_sol)
diagram.Publish(context)


# ## Simulating the solution
# 
# You may see simulations of the static equilibrium that result in the spheres moving.  Why is that?
# 
# Keep in mind that
# - A static equilibrium might not be a *stable* equilibrium.  States close to the equilibrium might diverge.
# - The optimization solver satisfies the equations only up to a numerical tolerance.

# In[ ]:


simulator = Simulator(diagram)
plant.SetPositions(plant.GetMyContextFromRoot(simulator.get_mutable_context()), q_sol)
if running_as_notebook:
  simulator.set_target_realtime_rate(1.0)
  simulator.AdvanceTo(5.0);
else:
  simulator.AdvanceTo(0.1);


# In[ ]:





# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=da179554-1a2d-4268-85aa-b1e5b071712b' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>
