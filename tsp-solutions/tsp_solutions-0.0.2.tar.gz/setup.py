from setuptools import setup 

setup(name = 'tsp_solutions',
version='0.0.2',
description='The travelling salesman problem is a np-hard problem with application in supply chain and computer science',
long_description='''
 The code uses PuLP module to formulate the problem and CPLEX, GUROBI, COIN_CMD, and PULP_solver to find the exact solution of the TSP. 
 The module also includes heuristics and metaheuristics functions that can be used for large instances.
 More functions will be added.
 If you find an error or want to solve problems together write to me @shamikpushkar92@gmail.com.

 The module has two parts:

1. Exact Solution
tsp_exact uses PuLP module to formulate the problem and CPLEX, GUROBI, COIN_CMD, and PULP_solver to find the exact solution of the TSP. To setup an external solver follow this link.

2. Heuristics & Metaheuristics
heuristics & metaheuristic functions are local search algorithms that can be used for large instances.
 
 Dependencies include pulp, numpy, pandas, scipy, and copy.
''',
author='Shamik Pushkar',
author_email='shamikpushkar92@gmail.com',
url = 'https://github.com/projektdexter/tsp',
packages=['tsp_solutions'],
install_requires=['numpy','pandas','pulp','scipy'],
keywords=['python', 'travelling-salesman-problem', 'combinatorial-optimization', 'linear-programming', 'integer-programming', 'pulp', 'optimization', 'heuristics','metaheuristics','vrp','vehicle-routing-problem']
)