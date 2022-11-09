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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/force.html).  I recommend having both windows open, side-by-side!
# 

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from pydrake.all import (DiagramBuilder, Evaluate, LogVectorOutput, Simulator,
                         SymbolicVectorSystem, Variable)

q = Variable('q')
v = Variable('v')
t = Variable('t')
kp = 10
kd = 1
m = 1
g = 10
c = 10  # amplitude.  set to zero to see the steady-state response.
q_d = c*np.sin(t)
v_d = c*np.cos(t)
a_d = -c*np.sin(t)
# PD control:
#u = kp*(q_d - q) + kd*(v_d - v)
# Stiffness control:
#u = kp*(q_d - q) + kd*(v_d - v) + m*g
# Inverse dynamics control:
u = m*(a_d + kp*(q_d - q) + kd*(v_d - v)) + m*g

sys = SymbolicVectorSystem(state=[q, v],
                           time=t,
                           dynamics=[v, -g + u / m],
                           output=[q])

builder = DiagramBuilder()
system = builder.AddSystem(sys)
logger = LogVectorOutput(system.get_output_port(0), builder)
diagram = builder.Build()

context = diagram.CreateDefaultContext()
context.SetContinuousState([0.9, 0])

simulator = Simulator(diagram, context)
simulator.AdvanceTo(10)

# Plot the results.
log = logger.FindLog(context)
plt.figure()
plt.plot(log.sample_times(),
         log.data().transpose(), log.sample_times(),
         c * np.sin(log.sample_times()))
plt.legend(['q(t)', 'q_d(t)'])
plt.xlabel('t');


# In[ ]:




