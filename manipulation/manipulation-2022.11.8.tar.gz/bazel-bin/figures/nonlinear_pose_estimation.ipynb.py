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

# In[ ]:


# Let's do all of our imports here.
import numpy as np
import matplotlib.pyplot as plt, mpld3

from pydrake.all import (RigidTransform, RollPitchYaw, RotationMatrix)

from manipulation import running_as_notebook

if running_as_notebook:
    mpld3.enable_notebook()


# In[ ]:


num_points_per_side=7
N = num_points_per_side*4
x = np.arange(-1, 1, 2/num_points_per_side)
half_width = 2
half_height = 1
top = np.vstack((half_width*x, half_height + 0*x))
right = np.vstack((half_width + 0*x, -half_height*x))
bottom = np.vstack((-half_width*x, -half_height + 0*x))
left = np.vstack((-half_width + 0*x, half_height*x))
p_m = np.vstack((np.hstack((top, right, bottom, left)), np.zeros((1, 4*num_points_per_side))))


# In[ ]:


def min_distance(x,y):
    return np.sqrt(np.min((x - p_m[0,:])**2 + (y-p_m[1,:])**2))
    
ax = plt.subplot()
ax.plot(p_m[0, :], p_m[1, :], 'b.')
ax.fill(p_m[0, :], p_m[1, :], 'lightblue', alpha=0.5)

X,Y = np.meshgrid(np.linspace(-3,3,150), np.linspace(-2,2,150))
MinDistance = np.vectorize(min_distance)
Z = MinDistance(X,Y)

CS = ax.contour(X, Y, Z, 3)
ax.clabel(CS, inline=True, fontsize=10);
ax.axis('equal')
ax.axis('off')
plt.savefig("rectangle_points_distance.svg")


# In[ ]:


def signed_distance(x,y):
    x = np.abs(x)
    y = np.abs(y)
    if (x>=2.0 and y>=1.0):
        return np.sqrt((x-2)**2 + (y-1)**2)
    if (y<=1.0 and x<=2.0):
        return np.max([x-2, y-1])
    if (x>2.0):
        return x-2
    return y-1

ax = plt.subplot()
p_m_closed = np.hstack((p_m, p_m[:,0].reshape(3,1)))  # close the box for this plot
ax.plot(p_m_closed[0, :], p_m_closed[1, :], 'b-')
ax.fill(p_m[0, :], p_m[1, :], 'lightblue', alpha=0.5)

X,Y = np.meshgrid(np.linspace(-3,3,150), np.linspace(-2,2,150))
SignedDistance = np.vectorize(signed_distance)
Z = SignedDistance(X,Y)

CS = ax.contour(X, Y, Z, 6)
ax.clabel(CS, inline=True, fontsize=10);
ax.axis('equal')
ax.axis('off')
plt.savefig("rectangle_signed_distance.svg")


# In[ ]:


ax = plt.subplot()
#ax.plot(p_m[0, :], p_m[1, :], 'b.')
ax.fill(p_m[0, :], p_m[1, :], 'lightsalmon', alpha=0.5)

Nv = 15
ax.plot(p_m[0, :Nv], p_m[1, :Nv], 'r.')
c = np.array([3,2])
o = np.hstack((p_m[:2,:Nv], c.reshape((2,1))))
for i in range(Nv):
    ax.plot([o[0,i], c[0]], [o[1, i],c[1]], 'r--', alpha=0.4)
ax.fill(o[0, :], o[1, :], 'lightgreen', alpha=0.5)
o_closed = np.hstack((c.reshape(2,1), o))
ax.plot(o_closed[0,:], o_closed[1,:], 'g-')
theta=0.8
R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
c_box = c + np.matmul(R,0.3*np.array([[0,1,1,0], [-1,-1,1,1]])).T
ax.fill(c_box[:,0], c_box[:,1], 'lightgray')
ax.text(-.3,-.1,'object',color='r')
ax.text(.5, 1.8, 'free space', color='g')
ax.text(2.15,2.25,'camera')
ax.axis('equal')
ax.axis('off')
plt.savefig("free_space.svg");


# In[ ]:




