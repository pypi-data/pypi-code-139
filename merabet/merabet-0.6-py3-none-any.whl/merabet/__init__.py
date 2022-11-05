import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from math import *
from typing import Union       
           

from mpl_toolkits.mplot3d import Axes3D
#Set up up figure size and DPI for screen demo
plt.rcParams['figure.figsize'] = (6,4)
plt.rcParams['figure.dpi'] = 70

def data_to_df(data : Union[str, list]) -> pd.DataFrame :   
    '''
    Transforms input data into a pandas dataframe.
    
    Parameters:
      data(str) : string describing a function, such as 'y = x + 2'.
      data(list): list of tuples (x,y) representing the data points
      data(list): list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).

    Returns: 
      result(pd.DataFrame): Pandas DataFrame of input data.
    '''
    
    if type(data) == str:
        equal_sign_pos = data.find('=')
        new_str = data[equal_sign_pos + 1:].lstrip()

        numbers = np.arange(1,10)
        y_values = []
        
        for x in numbers:
          y_values.append(eval(new_str))
        
        #Create DF:
        df = pd.DataFrame({'x': numbers, 'y': y_values})
        
    elif type(data) == list:
        
        if type(data[0]) == tuple:
            x_values = [pair[0] for pair in data]
            y_values = [pair[1] for pair in data]

            df = pd.DataFrame({'x': x_values, 'y': y_values})
        
        elif type(data) == list and all(isinstance(x, list) for x in data) and len(data) >= 3 and len({len(i) for i in data}) == 1:

            name_columns = ['y']
            for i in range(1, len(data)):
                name_columns.append(f'x{i}')

            data = np.array(data).T

            df = pd.DataFrame(data, columns = name_columns)
        
        elif type(data) == list and all(isinstance(x, list) for x in data) and len(data) == 2 and len({len(i) for i in data}) == 1:
          y = data[0]
          x = data[1]
          df = pd.DataFrame({'x': x, 'y': y})
        
    return df

def r_squared_and_RMSD(data : Union[str, list]) -> pd.DataFrame :

    '''
    Obtains Coefficient of Determination (r^2) and root-mean-square deviation 
    (RMSD) of given Pandas DataFrame from "y" and "prediction" columns.


    Parameters:
      data(str) : string describing a function, such as 'y = x + 2'.
      data(list): list of tuples (x,y) representing the data points
      data(list): list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).

    Returns: 
      result(pd.DataFrame): Pandas DataFrame of inputted list with new "R_squared" and "RMSD" columns.   
    '''
    #CALCULATE R_SQUARED WITH NUMPY AND ADD IT TO DATAFRAME
    actual = data['y']
    predict = data['prediction']
    ssr = ((actual - predict) ** 2).sum()
    sst = ((actual - np.mean(actual)) ** 2).sum()
    R_sq = 1 - (ssr / sst)
    data['R_squared'] = '--'
    data.at[0,'R_squared'] = R_sq

    #CALCULATE 
    N = data.shape[0]
    RMSD = math.sqrt( ((data['y'] - data['prediction'])**2).sum() / N)
    
    data['RMSD'] = '--'
    data.at[0,'RMSD'] = RMSD
    
    return data

def simple_linear_regression(data : list) -> pd.DataFrame:
    '''
    Fits a linear equation to observed data following the least squares method, obtaining  y = m * x + n  as final result.
    
    Parameters:
      data(str) : string describing a function, such as 'y = x + 2'.
      data(list): list of tuples (x,y) representing the data points
      data(list): list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).
    
    Returns: 
      result(pd.DataFrame): Pandas DataFrame of inputted data with new "prediction" column, among others.
    '''
    
    df = data_to_df(data)
    df['x * y'] = df['x'] * df['y']
    df['x**2'] = (df['x']) ** 2
    
    ones_array = np.ones_like(df['y'])
    df.insert(loc = 1, column = 'ones', value = ones_array)
    matrix = np.array(df.iloc[:, 0:2])

    # Beta = (Xt * X)**-1 * Xt*Y     where Xt is the transposed matrix
    Xt = matrix.T
    beta = np.matmul(np.linalg.inv(np.matmul(Xt, matrix)), np.matmul(Xt, df['y'])) #coefficients
    m, n = (beta[0], beta[1])

    if n >= 0 :
        equation = f'LINEAL: y = {round(m,3)} * x + {round(n,3)}'
    else:
        equation = f'LINEAL: y = {round(m,3)} * x - {abs(round(n,3))}'
    
    df['prediction'] = df['x'] * m + n
    x = df['x']
    y = df['y']
    prediction = df['prediction']
    r_squared_and_RMSD(df)
    
    plt.rcParams['text.color'] = 'blue'
    plt.scatter(x, y)
    plt.plot(x, prediction, color = 'red')
    plt.title(equation)
    plt.show()
    
    return df

def multiple_linear_regression(data : list) -> pd.DataFrame:
    '''
    Model that estimates the relationship between a quantitative dependent 
    variable and two or more independent variables using a straight line.
    Follows the matrix approach, using the formula defined in the beta variable.
    If using Jupyter Notebook, please write "%matplotlib notebook" in the same cell
    when executing for a better representation.
    
    Parameters:
      data(list): list of lists, where first list contains all values of the dependant variable (Y), and
      the remaining lists contain values of the independent variables (x1, x2 ...). 
      All listS must have same length and must be INDEPENDENT (a list can not be obtained from the product of another list with a number).
    
    Returns: 
      result(pd.DataFrame): Pandas DataFrame of inputted data with new "prediction" column, among others.
    '''
    initial_df = data_to_df(data)
    df = initial_df.copy()

    ones_array = np.ones_like(df['y'])
    df.insert(loc = 1, column = 'ones', value = ones_array)
    matrix = np.array(df.iloc[:, 1:])

    # Beta = (Xt * X)**-1 * Xt*Y     where Xt is the transposed matrix
    Xt = matrix.T
    beta = np.matmul(np.linalg.inv(np.matmul(Xt, matrix)), np.matmul(Xt, df['y'])) #coefficients

    df['prediction'] = (beta * df.iloc[:, 1:]).sum(axis = 1)

    plane_variables = ['x', 'y', 'z', 't', 's']
    beta_0, beta_1, beta_2 = beta

    plane = 'MULTIPLE: '

    plane += str(round(beta_0, 3)) + plane_variables[0]

    for i in range(1, len(beta)):
        aprox_beta = round(beta[i], 3)
        if aprox_beta >= 0:
            plane += ' + ' + str(aprox_beta) + plane_variables[i] 
        else:
            plane += ' - ' + str(abs(aprox_beta)) + plane_variables[i]

    r_squared_and_RMSD(df)

    #3D Axes
    if initial_df.shape[1] == 3:  #only plot if there are 3 variables (3D)
        x1 = df['x1']
        x2 = df['x2']
        y = df['y']

        #GENERATE PLANE

        max_value_prediction = int(df['prediction'].max()) * 2

        x1_s = np.tile(np.arange(max_value_prediction), (max_value_prediction,1))
        x2_s = np.tile(np.arange(max_value_prediction), (max_value_prediction,1)).T
        beta_0, beta_1, beta_2 = beta
        z = beta_0 + beta_1 * x1_s + beta_2 * x2_s

        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(x1, x2, y, color = 'red')
        ax.plot_surface(x1_s, x2_s, z , alpha=0.2)
        ax.set_title(plane)
        ax.view_init(40, -70)
        plt.show()

    return df

def non_linear_exponential_regression(data : Union[str, list]) -> pd.DataFrame :
    '''
    This function finds the equation of the exponential function that fits best for a set of data. 
    As a result, we get an equation of the form y = a * e ^ (bx) where a ≠ 0 
    
    Parameters:
      data(str) : string describing a function, such as 'y = x + 2'.
      data(list): list of tuples (x,y) representing the data points
      data(list): list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).
    
    Returns: 
      result(pd.DataFrame): Pandas DataFrame of inputted data with new "prediction" column, among others.
    '''
    
    df = data_to_df(data)
    df['z = ln(y)'] = np.log(df['y'])
    df['xz'] = df['x'] * df['z = ln(y)']
    df['x^2'] = df['x'] ** 2
    
    n = df.shape[0]
    a1 = (n * df['xz'].sum() - df['x'].sum() * df['z = ln(y)'].sum()) / \
    (n * df['x^2'].sum() - (df['x'].sum())**2 )
    
    a0 = (df['z = ln(y)'].sum() / n) - a1 * (df['x'].sum() / n)

    A = math.e ** a0
    b = a1
    
    df['prediction'] = A * math.e ** (b * df['x'])
    r_squared_and_RMSD(df)
    
    equation = f'EXPONENTIAL: y = {round(A,5)} * {round(math.e, 3)} ^ ({round(b,3)}x)'
    
    plt.scatter(df['x'],df['y'])
    plt.plot(df['x'], df['prediction'], color = 'red')
    plt.title(equation)
    plt.show()
    
    return df

def non_linear_logarithmic_regression(data : Union[str, list]) -> pd.DataFrame :
    '''
    Returns logarithmic regression of the data, getting as a result the curve y = a*ln(x) + b.
    
    Parameters:
      data(str) : string describing a function, such as 'y = x + 2'.
      data(list): list of tuples (x,y) representing the data points
      data(list): list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).
    
    Returns: 
      result(pd.DataFrame): Pandas DataFrame of inputted data with new "prediction" column, among others.
    '''
    
    np.seterr(divide = 'ignore') 
    df = data_to_df(data)
  
    df["x' = lnX"] = np.log(df['x'])
    df["x'y"] = df["x' = lnX"] * df['y']
    df["x'^2"] = df["x' = lnX"] ** 2
    
    # Remove data points with x greater than 1 since ln cant take values lower than 0and ln(1) = 0, and we must avoid dividing by this value.
    df = df[df['x'] > 1].reset_index(drop=True)      
    n = df.shape[0]
    
    b = ( n * df["x'y"].sum() - df["x' = lnX"].sum() * df['y'].sum() ) /\
    (n * df["x'^2"].sum() - (df["x' = lnX"].sum())**2 )
    
    a = (df['y'].sum() / n) - b * (df["x' = lnX"].sum() / n)
    df['prediction'] = a + b * df["x' = lnX"]
    
    if b >= 0 :
        equation = f'LOGARITHMIC: y = {round(a,3)} * ln(x) + {round(b,3)}'
    else:
        equation = f'LOGARITHMIC: y = {round(a,3)} * ln(x) - {abs(round(b,3))}'
    
    r_squared_and_RMSD(df)
    
    plt.scatter(df['x'], df['y'], color = 'blue')
    plt.plot(df['x'], df['prediction'], color = 'red')
    plt.title(equation)
    plt.show()
    
    return df

def non_linear_polynomial_regression(data : Union[str, list] , polynomial_degree : int ) -> pd.DataFrame:
    '''
    Returns the polynomial regression of the input data and the given degree.
    
    Parameters:
      data(str) : string describing a function, such as 'y = x + 2'.
      data(list): list of tuples (x,y) representing the data points
      data(list): list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).
      polynomial_degree(int) : integer representing the desired degree of polynomial regression equation.

    Returns: 
      result(pd.DataFrame): Pandas DataFrame of inputted data with new "prediction" column, among others.
    '''
    if polynomial_degree == 1:   #a polynomial regression equation of degree 1 is equal to a linear regression equation
        return simple_linear_regression(data)
    
    else:
        df = data_to_df(data)

        for i in range(polynomial_degree * 2 + 1):
            df['x^' + str(i)] = df['x']**i

        values_a = []
        for i in range(2 * polynomial_degree + 1):
            values_a.append(round(df['x^' + str(i)].sum(), 3))

        matrix = []
        for i in range(polynomial_degree + 1):
            matrix.append(values_a[i: i + polynomial_degree + 1 :])

        matrix_a = np.array(matrix)

        for e in range(1, polynomial_degree + 1):
            df['x^'+str(e)+' * y'] = df['x^'+str(e)] * df['y']

        values_b = [df['y'].sum()]
        for j in range(1, polynomial_degree + 1):
            values_b.append(round(df['x^'+str(j)+' * y'].sum(), 3))
        matrix_b = np.array(values_b)

        solution = np.linalg.solve(matrix_a, matrix_b)

        df['prediction'] =  (solution * df.iloc[:, 2: 3 + polynomial_degree]).sum(axis = 1)
        r_squared_and_RMSD(df)
        
        eq_variables = []    
        for col in (df.iloc[:, 2: 3 + polynomial_degree]).columns:
            eq_variables.append(col)
        
        equation = 'POLYNOMIAL: '
        
        equation += str(round(solution[0], 3))
        
        for i in range(1, len(solution)):
            
            coeff = round(solution[i], 3)
            var = eq_variables[i]
            
            if coeff >= 0:
                equation += ' + ' + str(coeff) + var
            
            elif var == 'x^1':
                equation += ' + ' + str(coeff) + 'x'
            
            else:
                equation += ' - ' + str(abs(coeff)) + var
        
        plt.scatter(df['x'], df['y'], color = 'blue')
        plt.plot(df['x'], df['prediction'], color = 'red')
        plt.title(equation)
        
        return df

def best_regression_model(data : Union[str, list]) -> pd.DataFrame :
    '''
    Returns best regression model by R-squared measurement.
    
    Parameters:
      data(str) : string describing a function, such as 'y = x + 2'.
      data(list): list of tuples (x,y) representing the data points
      data(list): list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).
    
    Returns: 
      result(pd.DataFrame): Pandas DataFrame of inputted data comparing every model by the coefficient of determination.
    '''
    models = ['simple_linear_regression', 'multiple_linear_regression', 'non_linear_exponential_regression', 'non_linear_logarithmic_regression', 'non_linear_polynomial_regression']
    r_sq = []
   
    if len(data) < 3 or type(data) == str:    
        for model in models:
            if model not in ['multiple_linear_regression', 'non_linear_polynomial_regression']:
                r_sq.append(eval(model+'(data)').at[0,'R_squared'])
                plt.show()

            elif model == 'multiple_linear_regression':
                r_sq.append(0)   

            elif model == 'non_linear_polynomial_regression':  
                #obtain best degree
                flag = 0
                rsq_polynomial = 0
                max_rsq = 0
                degree = 1

                while flag == 0:
                    rsq_polynomial = (eval(model+'(data, degree)').at[0,'R_squared'])

                    if rsq_polynomial > max_rsq:
                        max_rsq = rsq_polynomial
                        degree += 1
                        plt.cla()  #clear plot of non-optimal degrees
                    else:
                        flag = -1
                optimal_degree = degree - 1            
                r_sq.append(max_rsq)
      
      #FIND BEST MODEL:
        sorted_rsq = sorted(r_sq, reverse=True)

        greatest_rsq = sorted_rsq[0]
        second_greatest = sorted_rsq[1]

        greatest_rsq_position = r_sq.index(greatest_rsq)
        sec_greatest_rsq_position =  r_sq.index(second_greatest)

        best_model = models[greatest_rsq_position]
        sec_best_model = models[sec_greatest_rsq_position]                             

        results = pd.DataFrame([r_sq], columns = ['simple', 'multiple', 'exponential', 'logarithmic', 'polynomial (degree = ' + str(optimal_degree) + ')'],
                              index = ['R_Squared'])

        if best_model == 'non_linear_polynomial_regression':
            response = f'Best model is {best_model}, with an optimal degree of {optimal_degree}.\nThe second best model is {sec_best_model}'
        
        else:
            response =  f'Best model is {best_model}'
        plt.show()
        print()
        print(response)
        print()
        return(results)
         
    elif len(data) >= 3 and type(data) != str:
        
        print('Only Multiple Linear Regression can be applied')
        print()
        return (multiple_linear_regression(data))