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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/pick.html).  I recommend having both windows open, side-by-side!

# In[ ]:


from pydrake.all import FindResourceOrThrow, MultibodyPlant, Parser


# # Don't assume $\dot{q} \equiv v$
# 
# Let's just add a single object into the scene.  We won't weld it to the world frame, so it is a "free body" or has a "floating base".

# In[ ]:


def num_positions_velocities_example():
    plant = MultibodyPlant(time_step = 0.0)
    Parser(plant).AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf"))
    plant.Finalize()

    context = plant.CreateDefaultContext()
    print(context)

    print(f"plant.num_positions() = {plant.num_positions()}")
    print(f"plant.num_velocities() = {plant.num_velocities()}")

num_positions_velocities_example()


# Looking at the `Context` you can see that this system has 13 total state variables.  7 of them are positions, $q$; this is due to our pose representation using unit quaternions.  But only 6 of them are velocities, $v$; this is because a six-element spatial velocity provides a better (unconstrained) representation of the rate of change of the unit quaternion.  But clearly, if the length of the vectors don't even match, we do *not* have $\dot{q} = v$.

# In[ ]:




