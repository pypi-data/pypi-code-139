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

# This notebook provides examples to go along with the [textbook](http://manipulation.csail.mit.edu/pose.html).  I recommend having both windows open, side-by-side!

# In[ ]:


import os

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import pydot
from IPython.display import HTML, SVG, display
from pydrake.all import (AbstractValue, AddMultibodyPlantSceneGraph, AngleAxis,
                         BaseField, ConstantValueSource, CsdpSolver,
                         DepthImageToPointCloud, DiagramBuilder,
                         DifferentialInverseKinematicsIntegrator,
                         FindResourceOrThrow, LeafSystem,
                         MakePhongIllustrationProperties, MathematicalProgram,
                         MeshcatPointCloudVisualizer, MeshcatVisualizer,
                         MeshcatVisualizerParams, Parser, PiecewisePolynomial,
                         PiecewisePose, PointCloud, RigidTransform,
                         RollPitchYaw, RotationMatrix, Simulator, StartMeshcat,
                         ge)

from manipulation import running_as_notebook
from manipulation.meshcat_utils import AddMeshcatTriad, draw_open3d_point_cloud
from manipulation.scenarios import (AddIiwaDifferentialIK, AddMultibodyTriad,
                                    AddRgbdSensor, MakeManipulationStation)
from manipulation.utils import AddPackagePaths, FindResource

if running_as_notebook:
    mpld3.enable_notebook()


# In[ ]:


# Start the visualizer.
meshcat = StartMeshcat()


# # Non-penetration constraints with nonlinear optimization

# In[ ]:


from pydrake.all import Solve
from functools import partial

def ConstrainedKnownCorrespondenceNonlinearOptimization(p_Om, p_s, chat):
    """ This version adds a non-penetration constraint (x,y >= 0) """

    p_Omc = p_Om[:2, chat]
    p_s = p_s[:2, :]
    Ns = p_s.shape[1]

    prog = MathematicalProgram()
    p = prog.NewContinuousVariables(2, 'p')
    theta = prog.NewContinuousVariables(1, 'theta')

    def position_model_in_world(vars, i):
        [p, theta] = np.split(vars, [2])
        R = np.array([[np.cos(theta[0]), -np.sin(theta[0])],
                      [np.sin(theta[0]), np.cos(theta[0])]])
        p_Wmci = p + R @ p_Omc[:,i]
        return p_Wmci

    def squared_distance(vars, i):
        p_Wmci = position_model_in_world(vars, i)
        err = p_Wmci - p_s[:,i]
        return err.dot(err)

    for i in range(Ns):
        prog.AddCost(partial(squared_distance, i=i),
                     np.concatenate([p[:], theta]))
        # forall i, p + R*mi >= 0.  
        prog.AddConstraint(partial(position_model_in_world, i=i), 
                           vars=np.concatenate([p[:], theta]),
                           lb=[0, 0], ub=[np.inf, np.inf])
    
    result = Solve(prog)
    
    theta_sol = result.GetSolution(theta[0])
    Rsol = np.array([[np.cos(theta_sol), -np.sin(theta_sol), 0],
                     [np.sin(theta_sol), np.cos(theta_sol), 0], 
                     [0, 0, 1]])
    psol = np.zeros(3)
    psol[:2] = result.GetSolution(p)

    return RigidTransform(RotationMatrix(Rsol), psol)

p_Om, p_s, X_O = MakeRectangleModelAndScenePoints(
    yaw_O=0.2,
    p_O = [1.5, 1.2],
)
c = range(p_Om.shape[1])  # perfect, known correspondences
Xhat_O = ConstrainedKnownCorrespondenceNonlinearOptimization(p_Om, p_s, c)
PlotEstimate(p_Om=p_Om, p_s=p_s, Xhat_O=Xhat_O, chat=c, X_O=X_O)
PrintResults(X_O, Xhat_O)
plt.gca().plot([0,0], [0, 2.5], 'g-', linewidth=3)
plt.gca().plot([0,4], [0, 0], 'g-', linewidth=3);


# # Non-penetration (half-plane) constraints with convex optimization

# In[ ]:


def ConstrainedKnownCorrespondenceConvexRelaxation(p_Om, p_s, chat):
    """ This version adds a non-penetration constraint (x,y >= 0) """

    p_Omc = p_Om[:2, chat]
    p_s = p_s[:2, :]
    Ns = p_s.shape[1]

    prog = MathematicalProgram()
    [a,b] = prog.NewContinuousVariables(2)
    # We use the slack variable as an upper bound on the cost of each point to make the objective linear.
    slack = prog.NewContinuousVariables(Ns)
    p = prog.NewContinuousVariables(2)
    prog.AddBoundingBoxConstraint(0,1,[a,b])  # This makes Csdp happier
    R = np.array([[a, -b],[b, a]])
    prog.AddLorentzConeConstraint([1.0, a, b])

    # Note: Could do this more efficiently, exploiting trace.  But I'm keeping it simpler here.
    prog.AddCost(np.sum(slack))
    for i in range(Ns):
        c = p + np.matmul(R,p_Omc[:,i]) - p_s[:,i]
        # forall i, slack[i]^2 >= |c|^2 
        prog.AddLorentzConeConstraint([slack[i], c[0], c[1]])
        # forall i, p + R*mi >= 0.  
        prog.AddConstraint(ge(p + np.matmul(R, p_Omc[:,i]), [0, 0]))
    
    result = CsdpSolver().Solve(prog)
    
    [a,b] = result.GetSolution([a,b])
    Rsol = np.array([[a, -b, 0],[b, a, 0], [0,0,1]])
    psol = np.zeros(3)
    psol[:2] = result.GetSolution(p)

    return RigidTransform(RotationMatrix(Rsol), psol)

p_Om, p_s, X_O = MakeRectangleModelAndScenePoints(
    yaw_O=0.2,
    p_O = [1.5, 1.2],
)
c = range(p_Om.shape[1])  # perfect, known correspondences
Xhat_O = ConstrainedKnownCorrespondenceConvexRelaxation(p_Om, p_s, c)
PlotEstimate(p_Om=p_Om, p_s=p_s, Xhat_O=Xhat_O, chat=c, X_O=X_O)
PrintResults(X_O, Xhat_O)
plt.gca().plot([0,0], [0, 2.5], 'g-', linewidth=3)
plt.gca().plot([0,4], [0, 0], 'g-', linewidth=3);

