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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/robot.html).  I recommend having both windows open, side-by-side!

# In[ ]:


from pydrake.all import FindResourceOrThrow, StartMeshcat

from manipulation import running_as_notebook
from manipulation.meshcat_utils import model_inspector


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Robot arms
# 
# The next two cells will give you a simple interface to move the joints around on a variety of robot arm models.
# 
# Have a favorite robot that I haven't included here?  If you send me a link to a properly licensed URDF or SDF description of the robot and it's mesh files, I'm happy to add it!  It's worth taking a look at the files quickly, to get a sense for how they work: [SDF](https://github.com/RobotLocomotion/drake/blob/master/manipulation/models/iiwa_description/sdf/iiwa14_no_collision.sdf), [URDF](https://github.com/RobotLocomotion/drake/blob/master/manipulation/models/iiwa_description/urdf/iiwa14_no_collision.urdf).
# 
# Note: The Jaco doesn't visualize properly in this renderer yet.  See drake issue [#13846](https://github.com/RobotLocomotion/drake/issues/13846).

# In[ ]:


# First pick your robot by un-commenting one of these:
robot = "Kuka LBR iiwa 7"
#robot = "Kuka LBR iiwa 14"
#robot = "Kinova Jaco Gen2 (7 DoF)"
#robot = "Franka Emika Panda"

def get_model_file(description):
  # Note: I could download remote model resources here if necessary.
  if description == "Kuka LBR iiwa 7":
    return FindResourceOrThrow("drake/manipulation/models/iiwa_description/iiwa7/iiwa7_no_collision.sdf")
  elif description == "Kuka LBR iiwa 14":
    return FindResourceOrThrow("drake/manipulation/models/iiwa_description/sdf/iiwa14_no_collision.sdf")
  elif description == "Kinova Jaco Gen2 (7 DoF)":
    return FindResourceOrThrow("drake/manipulation/models/jaco_description/urdf/j2s7s300.urdf")
  elif description == "Franka Emika Panda":
    return FindResourceOrThrow("drake/manipulation/models/franka_description/urdf/panda_arm_hand.urdf")
  raise Exception("Unknown model")

meshcat.Delete()

model_inspector(meshcat, get_model_file(robot))

meshcat.DeleteAddedControls()


# # Robot hands
# 
# I don't have the same smörgåsbord of robot models to offer for robot hands (yet).  We do have the allegro hand model available, and I'm happy to add more here (though many will require some care to handle their kinematic constraints).  For now, you can at least try out the [Allegro Hand](http://www.wonikrobotics.com/Allegro-Hand.htm).
# 
# TODO(russt): Consider porting Robotiq, Sandia, or IHY-hand from our [openhumanoids](https://github.com/openhumanoids/oh-distro/tree/master/software/models/common_components) project.

# In[ ]:


meshcat.Delete()

model_inspector(meshcat,
    FindResourceOrThrow(
        "drake/manipulation/models/allegro_hand_description/sdf/allegro_hand_description_right.sdf"
    ))

meshcat.DeleteAddedControls()


# In[ ]:




