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


import pydot
from IPython.display import SVG, display
from pydrake.all import FindResourceOrThrow, MultibodyPlant, Parser


# # Inspecting the kinematic tree
# 
# Here is a simple example that demonstrates how to inspect the kinematic tree stored in a `MultibodyPlant`.

# In[ ]:


def kinematic_tree_example():
    plant = MultibodyPlant(time_step=0.0)
    parser = Parser(plant)
    parser.AddModelFromFile(FindResourceOrThrow(
        "drake/manipulation/models/allegro_hand_description/sdf/allegro_hand_description_right.sdf"))
    parser.AddModelFromFile(FindResourceOrThrow(
        "drake/examples/manipulation_station/models/061_foam_brick.sdf"))
    plant.Finalize()

    # TODO(russt): Add floating base connections
    # TODO(russt): Consider a more interactive javascript rendering?
    display(SVG(pydot.graph_from_dot_data(plant.GetTopologyGraphvizString())[0].create_svg()))

kinematic_tree_example()


# In[ ]:




