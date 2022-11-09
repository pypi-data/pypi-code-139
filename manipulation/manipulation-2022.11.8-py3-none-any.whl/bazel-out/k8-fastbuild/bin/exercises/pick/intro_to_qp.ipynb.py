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

# # Introduction to QP

# In[ ]:


# python libraries
import numpy as np

from pydrake.all import (
    MathematicalProgram, Solve, eq, le, ge
)


# # Introduction to MathematicalProgram 
# 
# The purpose of this exercise is to get you familiar with the basics of what an instance of an optimization problem is, as well as how to solve it. 
# 
# An optimization problem is usually written as 
# 
# $$\begin{aligned} \min_x \quad & f(x) \\ \textrm{s.t.} \quad & g(x)\leq 0,\\ \quad &  h(x)=0 \end{aligned}$$
# 
# We call $x$ the **decision variable**, $f(x)$ the **cost function**, $g(x)\leq 0$ an **inequality constraint**, and $h(x)=0$ an **equality constraint**. We usually denote the optimal solution by $x^*$. Most of the times, the constraints are hard-constraints, meaning that they must be fulfilled by the optimal solution. 
# 
# Drake offers a very good interface to many solvers using `MathematicalProgram`. Let's try to solve a simple problem using `MathematicalProgram`: 
# 
# $$\begin{aligned} \min_x \quad & \frac{1}{2}x^2 \\ \textrm{s.t.} \quad & x\geq 3 \end{aligned}$$
# 
# Before we start coding, what do you expect the answer to be? You should persuade yourself that the optimal solution is $x^*=3$, since that is value at which minimum cost is achieved without violating the constraint.
# 
# 

# In[ ]:


'''
Steps to solve a optimization problem using Drake's MathematicalProgram
'''
# 1. Define an instance of MathematicalProgram 
prog = MathematicalProgram() 

# 2. Add decision varaibles
x = prog.NewContinuousVariables(1)

# 3. Add Cost function 
prog.AddCost(x.dot(x))

# 4. Add Constraints
prog.AddConstraint(x[0] >= 3)

# 5. Solve the problem 
result = Solve(prog)

# 6. Get the solution
if (result.is_success): 
  print("Solution: " + str(result.GetSolution()))


# You should have seen that we were successful in getting the expected solution of $x^*=3$. 
# 
# A particular class of problems that we want to focus on this problem are [Quadratic Programs (QP)](https://en.wikipedia.org/wiki/Quadratic_programming), which can be solved very efficiently in practice (even on the order of kHz).
# 
# The general formulation of these problems are defined as follows. 
# 
# $$\begin{aligned} \min_x \quad & \frac{1}{2}x^T\mathbf{Q}x + c^Tx \\ \textrm{s.t.} \quad & \mathbf{A}x\leq b,\\ \quad &  \mathbf{A}'x=b' \end{aligned}$$
# 
# where $\mathbf{Q}$ is a positive-definite, symmetric matrix. Note that the cost is a quadratic function of the decision variables, while the constraints are all linear. This is what defines a convex QP. 
# 
# Let's practice solving a simple QP: 
# 
# $$\begin{aligned} \min_{x_0,x_1,x_2} \quad & x_0^2 + x_1^2 + x_2^2 \\ \textrm{s.t.} \quad & \begin{pmatrix} 2 & 3 & 1 \\ 5 & 1 & 0 \end{pmatrix} \begin{pmatrix} x_0 \\ x_1 \\ x_2 \end{pmatrix} = \begin{pmatrix} 1 \\ 1 \end{pmatrix}\\  \quad &  \begin{pmatrix} x_0 \\ x_1 \\ x_2 \end{pmatrix} \leq \begin{pmatrix} 2 \\ 2 \\ 2\end{pmatrix} \end{aligned}$$
# 
# To conveniently write down constraints that are vector-valued, Drake offers `eq,le,ge` for elementwise constraints. It might take some time to learn the syntax of constraints. For a more well-written and in-depth introduction to `MathematicalProgram`, [this notebook tutorial](https://deepnote.com/workspace/Drake-0b3b2c53-a7ad-441b-80f8-bf8350752305/project/Tutorials-2b4fc509-aef2-417d-a40d-6071dfed9199/%2Fmathematical_program.ipynb) is incredibly useful. 
#  
# 

# In[ ]:


prog = MathematicalProgram()

x = prog.NewContinuousVariables(3)

prog.AddCost(x.dot(x)) 
prog.AddConstraint(eq(np.array([[2, 3, 1], [5, 1, 0]]).dot(x), [1, 1]))
prog.AddConstraint(le(x, 2 * np.ones(3)))

result = Solve(prog)

# 6. Get the solution
if (result.is_success()): 
  print("Solution: " + str(result.GetSolution()))


# 
# **Now, it's your turn to solve a simple problem!** 
# 
# You must solve the following problem and store the result in a variable named `result_submission`. 
# 
# $$\begin{aligned} \min_{x_0,x_1,x_2} \quad & 2x_0^2 + x_1^2 + 3x_2^2 \\ \textrm{s.t.} \quad & \begin{pmatrix} 1 & 2 & 3 \\ 2 & 7 & 4 \end{pmatrix} \begin{pmatrix} x_0 \\ x_1  \\ x_2 \end{pmatrix} = \begin{pmatrix} 1 \\ 1 \end{pmatrix} \\ \quad &  |x| \leq \begin{pmatrix} 0.35 \\ 0.35 \\ 0.35\end{pmatrix} \end{aligned}$$
# 
# NOTE: The last constraint says that the absolute value of `x[i]` must be less than the value of `b_bb[i]`. You cannot put an absolute value directly as a constraint, so there are two routes that you can take:
# - Break the constraints down to two constraints that don't involve the absolute value.  
# - Drake offers [`AddBoundingboxConstraint`](https://drake.mit.edu/pydrake/pydrake.solvers.html?highlight=addboundingboxconstraint#pydrake.solvers.MathematicalProgram.AddBoundingBoxConstraint) which you may use in your implementation.

# In[ ]:


prog = MathematicalProgram() 

# Modify here to get the solution to the above optimization problem. 

result_submission = None # store the result here. 


# ## How will this notebook be Graded?##
# 
# If you are enrolled in the class, this notebook will be graded using [Gradescope](www.gradescope.com). You should have gotten the enrollement code on our announcement in Piazza. 
# 
# For submission of this assignment, you must do as follows:
# - Download and submit the notebook `intro_to_qp.ipynb` to Gradescope's notebook submission section, along with your notebook for the other problems.
# 
# We will evaluate the local functions in the notebook to see if the function behaves as we have expected. For this exercise, the rubric is as follows:
# - [4 pts] `result_submission` must have the correct answer to the QP. 

# Below is our autograder where you can check the correctness of your implementations. 

# In[ ]:


from manipulation.exercises.pick.test_simple_qp import TestSimpleQP 
from manipulation.exercises.grader import Grader 

Grader.grade_output([TestSimpleQP], [locals()], 'results.json')
Grader.print_test_results('results.json')

