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

# ## Stochastic Optimization

# In[ ]:


import matplotlib
import matplotlib.pyplot as plt
import mpld3
import numpy as np
from manipulation import running_as_notebook
from pydrake.all import (BaseField, Evaluate, Fields, PointCloud, Rgba,
                         RigidTransform, Sphere, StartMeshcat, Variable)

if running_as_notebook:
    mpld3.enable_notebook()

def loss(theta):
    x = theta[0]
    y = theta[1]
    eval = 2 * x ** 2 - 1.05 * x ** 4 + x ** 6 / 6 + x * y + y ** 2
    return 0.25 * eval

def generate_color_mat(color_vec, shape):
    color_mat = np.tile(np.array(color_vec).astype(np.float32).reshape(3,1), (1, shape[1]))
    return color_mat

def visualize_loss(meshcat, loss, colormap='viridis', spacing=0.01, clip_min=None, clip_max=None):
    # Create a grid of thetas and evaluate losses.
    points = []
    for i in np.arange(-3, 3, spacing):
        for j in np.arange(-3, 3, spacing):
            points.append([i,j,loss(np.array([i,j]))])
    points = np.array(points)

    # Normalize losses and color them according to colormap. 
    cmap = matplotlib.cm.get_cmap(colormap)
    min_loss = np.min(points[:,2]) if clip_min == None else clip_min
    max_loss = np.max(points[:,2]) if clip_max == None else clip_max

    colors = []
    for i in range(points.shape[0]):
        normalized_loss = (points[i,2] - min_loss) / (max_loss - min_loss)
        colors.append(list(cmap(normalized_loss))[0:3])

    cloud = PointCloud(points.shape[0], 
                       Fields(BaseField.kXYZs | BaseField.kRGBs))
    cloud.mutable_xyzs()[:] = points.T
    cloud.mutable_rgbs()[:] = 255 * np.array(colors).T

    meshcat.Delete()
    meshcat.SetProperty("/Background", 'visible', False)
    meshcat.SetObject("/loss", cloud, point_size=0.03)

def visualize_trajectory(trajectory):
    points = PointCloud(trajectory.shape[0])
    points.mutable_xyzs()[:] = trajectory.T
    meshcat.SetObject("/traj", points, rgba=Rgba(1, 0, 0), point_size=0.03)
    meshcat.SetLine("/traj_line", trajectory.T, rgba=Rgba(1, 0, 0))

    # Visualize the initial guess.
    meshcat.SetObject("/traj_initial", Sphere(0.05), Rgba(1, 0, 0))
    meshcat.SetTransform("/traj_initial", RigidTransform(trajectory[0,:]))

    # Visualize the final point of the iteration.
    meshcat.SetObject("/traj_final", Sphere(0.05), Rgba(0, 1, 0))
    meshcat.SetTransform("/traj_final", RigidTransform(trajectory[-1,:]))


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# ## The Three Hump Camel 
# In this exercise, we'll implement our own versions of gradient descent and stochastic gradient descent! 
# 
# Our goal is to find the minima of the following function:
# 
# $$l(x)=\frac{1}{4}\bigg(2x_1^2-1.05x_1^4+\frac{x_1^6}{6}+x_1x_2+x_2^2\bigg)$$
# 
# Note that you can access this function using `loss(x)`.
# 
# We have visualized the landscape of this function in meshcat if you run the cell below! You will notice the following things:
# 
# 1. This function has 3 local minima (hence, the name 'three hump camel')
# 2. The global minima is located at $f([0,0])=0$. 

# In[ ]:


# The parameters are optimized for best visualization in meshcat. 
# For faster visualization, try increasing spacing. 
visualize_loss(meshcat, loss, colormap = 'viridis', spacing=0.02, clip_max=2.0)


# ## Gradient Descent
# 
# As we saw in the lecture, one way of trying to find the minimum of $l(x)$ is to use explicit gradients and do gradient descent. 
# 
# $$x \leftarrow x - \eta\bigg(\frac{\partial l(x)}{\partial x}\bigg)^T$$
# 
# We've set up a basic outline of the gradient descent algoritm for you. Take a look at the following function `gradient_descent` that implements the following steps:
# 
# 1. Initialize $x\in\mathbb{R}^2$ at random from some bounded region.
# 2. Until maximum iteration, update $x$ according to the rule. 

# In[ ]:


def gradient_descent(rate, update_rule, initial_x=None, iter=1000):
  """gradient descent algorithm 
  @params: 
  - rate (float): eta variable of gradient descent.
  - update_rule: a function with a signature update_rule(x, rate). 
  - initial_x: initial position for gradient descent. 
  - iter: number of iterations to run gradient descent for.
  """
  # If no initial guess is supplied, then randomly choose one. 
  if initial_x is None:
    x = -3 + 6.0 * np.random.rand(2)
  else:
    x = initial_x
  # Compute loss for first parameter for visualization. 
  x_list = []
  x_list.append([x[0], x[1], loss(x)])
  # Loop through with gradient descent. 
  for i in range(iter):
    # Update the parameters using update rule.
    x = update_rule(x, rate)
    x_list.append([x[0], x[1], loss(x)])
  return np.array(x_list)


# ## Determinisitc Exact Gradients
# 
# **Problem 9.1.a** [2 pts]: Let's first use the vanilla gradient descent algorithm with exact gradients. Below, you must implement the simple update function:
# 
# $$x \leftarrow x - \eta\bigg(\frac{\partial l(x)}{\partial x}\bigg)^T$$
# 
# HINT: You can write down the gradient yourself, but remember you can also use drake's symbolic differentiation!
# 

# In[ ]:


def exact_gradient(x, rate):
  """
  Update rule. Receive theta and update it with the next theta.
  @params
  - x: input variable x.
  - rate: rate of descent, variable "eta". 
  @returns:
  - updated variable x. 
  """
  return x


# When you've completed the function, you can run the below cell to check the visualization! For this problem, the visualization has the following convention:
# - Red sphere is the initial guess 
# - Green sphere is the final point after `iter` iterations. 
# - Every updated parameter is drawn as smaller red cubes. 

# In[ ]:


# Compute the trajectory. 
trajectory = gradient_descent(0.1, exact_gradient)
visualize_trajectory(trajectory)


# If you've implemented it correctly, run the cell multiple times to see the behavior of gradient descent from different initial conditions. You should note that depending on where you started, you are deterministically stuck in the local minima that corresponds to its attraction region. 

# ## Stochastic Approximation to Gradients
# 
# **Problem 9.1.b** [2 pts]: One of the mindblowing facts we learned from the lecture was that we can actually do gradient descent without ever having true gradients of the loss function $l(x)$! 
# 
# Your job is to write down the following update function for gradient descent:
# 
# $$x \leftarrow x - \eta\big[l(x+w)-l(x)\big]w$$
# 
# where $w\in\mathbb{R}^2$ drawn from a Gaussian distribution, $w\sim\mathcal{N}(0,\sigma^2=0.25)$. You can use `np.random.normal()` to draw from this distribution.

# In[ ]:


def approximated_gradient(x, rate):
  """
  Update rule. Receive theta and update it with the next theta.
  @params
  - x: input variable x.
  - rate: rate of descent, variable "eta". 
  @returns:
  - updated varaible x. 
  """
  return x


# Again, once you've implemented the function, run the below cell to visualize the trajectory.

# In[ ]:


trajectory = gradient_descent(0.01, approximated_gradient, iter=10000)
visualize_trajectory(trajectory)


# If you've implemented it correctly, take a moment to run it from multiple different conditions - the results are somewhat shocking.
# - With the right parameters ($\sigma,\eta$), this version of gradient descent is much better than the deterministic exact version at converging to global minima. (In fact, you'll sometimes see it hop out of one of the local minimas and converge to a global minima?)
# - But we never explicitly took derivatives!
# - (Side note): does this mean this way approximating gradients is the magical tool to everything? not quite. This version can be prone to getting stuck in saddle points!

# ## Baselines 
# 
# **Problem 9.1.c** [4 pts]: We don't necessarily have to take finite differences to estimate the gradient. In fact, we could have subtracted our perturbed estimate from any function, as long as it is not a function of $w$! 
# 
# $$x \leftarrow x - \eta\big[l(x+w)-b(x)\big]w$$
# 
# As a written problem, the problem is as follows: prove that on average, the difference in the updates (call it $\mathbb{E}_w[\Delta x$]) is approximately equal to the true analytical gradient. 
# 
# HINT: Use first-order taylor approximation of $l(x+w)$ (i.e. you may assume $w$ is quite small)

# **Problem 9.1.d** [1 pts]: Finally, implement the update law above. The update rule is almost identical to 9.1.b except for the implementation of the baseline, so this is like a bonus question.  

# In[ ]:


def approximated_gradient_with_baseline(x, rate, baseline):
  """
  Update rule. Receive theta and update it with the next theta.
  @params
  - x: input variable x.
  - rate: rate of descent, variable "eta". 
  - baseline: float for baseline.
  @returns:
  - updated varaible x. 
  """
  return x


# As you proved in 9.1.c, adding a baseline does not change the mean of the update. However, it does change the variance!
# 
# In the below code, you can play around with different values of the baseline to see what happens. Remember that the optimal value (smallest variance) of the baseline is $l(x)$. 
# 
# You should see that if the baseline is close to `loss(x)` (e.g. baseline is uniformly zero), there is no big difference with the solution you wrote on 9.1.b. However, when the baseline is far from `loss(x)` (e.g. baseline is uniformly 5), our path starts to look more like a random walk due to high variance.

# In[ ]:


def baseline(x):
  return 5 # feel free to modify here!

def reduced_function(x, rate):
  return approximated_gradient_with_baseline(x, rate, baseline)

trajectory = gradient_descent(0.01, reduced_function, iter=10000)
visualize_trajectory(trajectory)


# ## How will this notebook be Graded?
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do two things. 
# - Download and submit the notebook `stochastic_optimization.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# - Write down your answers to 9.1.c in your PDF submission to Gradescope. 
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [2 pts] 9.1.a must be implemented correctly.
# - [2 pts] 9.1.b must be implemented correctly.
# - [4 pts] 9.1.c is answered correctly.
# - [1 pts] 9.1.d must be implemented correctly.

# In[ ]:


from manipulation.exercises.rl.test_stochastic_optimization import TestStochasticOptimization
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestStochasticOptimization], [locals()], 'results.json')
Grader.print_test_results('results.json')


# In[ ]:




