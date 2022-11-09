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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/rl.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import sys

import gym
import numpy as np
import torch
from pydrake.all import Rgba, RigidTransform, Sphere, StartMeshcat

from manipulation.meshcat_utils import plot_surface
from manipulation.utils import LoadDataResource, running_as_notebook


# In[ ]:


meshcat = StartMeshcat()


# First, let's define a few interesting cost functions that have multiple local minima.

# In[ ]:


def three_hump_camel(x, y, path=None):
    z = (2 * x**2 - 1.05 * x**4 + x**6 / 6 + x * y + y**2) / 4
    if path:
        pt = f"{path}/{x}_{y}"
        meshcat.SetObject(pt, Sphere(0.01), Rgba(0, 0, 1, 1))
        meshcat.SetTransform(pt, RigidTransform([x, y, z]))
    return z

def plot_three_hump_camel():
    X, Y = np.meshgrid(np.arange(-2.5, 2.5, 0.05), np.arange(-3, 3, 0.05))
    Z = three_hump_camel(X,Y)
    # TODO(russt): Finish the per-vertex coloring variant.
    plot_surface(meshcat, "three_hump_camel", X, Y, Z, wireframe=True)

def six_hump_camel(x, y, path=None):
    z = x**2 * (4 - 2.1 * x**2 + x**4 / 3) + x * y + y**2 * (-4 + 4 * y**2)
    if path:
        pt = f"{path}/{x}_{y}"
        meshcat.SetObject(pt, Sphere(0.01), Rgba(0, 0, 1, 1))
        meshcat.SetTransform(pt, RigidTransform([x, y, z]))
    return z

def plot_six_hump_camel():
    X, Y = np.meshgrid(np.arange(-2, 2, 0.05), np.arange(-1.2, 1.2, 0.05))
    Z = six_hump_camel(X,Y)
    # TODO(russt): Finish the per-vertex coloring variant.
    plot_surface(meshcat, "six_hump_camel", X, Y, Z, wireframe=True)


# # Black-box optimization
# 
# Let's explore a few of the algorithms from Nevergrad on these simple cost landscapes

# In[ ]:


# Treat nevergrad as an optional dependency.
# TODO(russt): Consume nevergrad without the (heavy) bayesian-optimization dependency.
if 'nevergrad' in sys.modules:
    import nevergrad as ng

    meshcat.Delete()
    plot_six_hump_camel()

    # Note: You can print nevergrad's available optimizers using
    # print(sorted(ng.optimizers.registry.keys()))

    # Uncomment some of these to try...
    #solver='NGOpt'
    #solver='RandomSearch'
    solver='CMA'
    optimizer = ng.optimizers.registry[solver](parametrization=2, budget=100)
    recommendation = optimizer.minimize(
        lambda x: six_hump_camel(x[0], x[1], "NGOpt"))
    xstar = recommendation.value
    meshcat.SetObject("recommendation", Sphere(0.02), Rgba(0, 1, 0, 1))
    meshcat.SetTransform("recommendation", RigidTransform(
        [xstar[0], xstar[1], six_hump_camel(xstar[0], xstar[1])]))
    print(xstar)  # recommended value


# In[ ]:


meshcat.Delete()


# # RL for box flip-up
# 
# ## State-feedback policy via PPO (with stiffness control)

# In[ ]:


gym.envs.register(id="BoxFlipUp-v0",
                  entry_point="manipulation.envs.box_flipup:BoxFlipUpEnv")


# In[ ]:


from stable_baselines3 import PPO

observations = "state"
env = gym.make("BoxFlipUp-v0", observations=observations)

use_pretrained_model = False
if use_pretrained_model:
    # Note: Models saved in stable baselines are version specific.  This one 
    # requires python3.6 (and cloudpickle==1.6.0).
    # TODO(russt): Save a trained model that works on Deepnote.
    model = PPO.load(LoadDataResource('box_flipup_ppo_state_3.zip'), env)
elif running_as_notebook:
    # This is a relatively small amount of training.  See rl_train_boxflipup.py 
    # for a version that runs the heavyweight version with multiprocessing.
    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=100000)
else:
    # For testing this notebook, we simply want to make sure that the code runs.
    model = PPO('MlpPolicy', env, n_steps=4, n_epochs=2, batch_size=8)
    model.learn(total_timesteps=4)

# Make a version of the env with meshcat.
env = gym.make("BoxFlipUp-v0", meshcat=meshcat, observations=observations)

if running_as_notebook:
    env.simulator.set_target_realtime_rate(1.0)

obs = env.reset()
for i in range(500 if running_as_notebook else 5):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
      obs = env.reset()


# In[ ]:


obs = env.reset()
Q, Qdot = np.meshgrid(np.arange(0, np.pi, 0.05), np.arange(-2, 2, 0.05))
# TODO(russt): tensorize this...
V = 0*Q
for i in range(Q.shape[0]):
    for j in range(Q.shape[1]):
        obs[2] = Q[i,j]
        obs[7] = Qdot[i,j]
        with torch.no_grad():
            V[i, j] = model.policy.predict_values(
                model.policy.obs_to_tensor(obs)[0])[0].cpu().numpy()[0]
V = V - np.min(np.min(V))
V = V / np.max(np.max(V))

meshcat.Delete()
meshcat.ResetRenderMode()
plot_surface(meshcat, "Critic", Q, Qdot, V, wireframe=True)


# In[ ]:




