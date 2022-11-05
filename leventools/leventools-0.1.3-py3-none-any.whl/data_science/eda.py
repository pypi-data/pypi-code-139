"""
Module for Exploratory Data Analysis methods
"""

import pandas
import numpy
from scipy import stats


def identify_outliers(dataframe: pandas.DataFrame, column: str):
    """Identify and return outliers based on specific column.
    Cutoff : IQR*1.5 is used

    Parameters
    ----------
    dataframe: pandas.DataFrame :
    Input DataFrame
        
    column: str :
    Column for outlier detection

    Returns
    -------
    outliers: List :
    List of outliers based on input column

    lower: float :
    Lower boundary for outliers, values below this are outliers

    upper: float :
    Upper boundary for outliers, values above this are outliers
    """
    # calculate inter quartile range
    q25, q75 = numpy.percentile(dataframe[column], 25), numpy.percentile(dataframe[column], 75)
    iqr = q75 - q25
    print(f'COLUMN: {column}\nPercentiles: 25th={q25:.2f}, 75th={q75:.2f}, IQR={iqr:.2f}')
    # calculate the outlier cutoff
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    # identify outliers
    outliers = [x for x in dataframe[column] if x < lower or x > upper]
    print(f'Identified outliers: {len(outliers)} of {len(dataframe[column])} values')
    # return outliers and boundaries
    return outliers, lower, upper


def remove_outliers(dataframe: pandas.DataFrame, column: str):
    """Identify and remove outliers based on specific column

    Parameters
    ----------
    dataframe: pandas.DataFrame :
    Input DataFrame
        
    column: str :
    Column for outlier detection

    Returns
    -------
    dataframe: pandas.DataFrame :
    Output DataFrame with outliers removed

    """
    _, lower, upper = identify_outliers(dataframe, column)
    return dataframe[(dataframe[column] >= lower) & (dataframe[column] <= upper)]


def chi2_correlation(dataframe: pandas.DataFrame, column1: str, column2: str):
    """Check correlation between 2 categorical variables using chi2 test

    Parameters
    ----------
    dataframe: pandas.DataFrame :
    Input DataFrame
        
    column1: str :
        
    column2: str :

    Returns
    -------
    p-Value: float:
        p_value result of Chi2 test

    contingency_table: pandas.DataFrame:
        table showing counts among columns

    """
    contingency_table = pandas.crosstab(dataframe[column1], dataframe[column2], margins=False)
    stat, p, dof, expected = stats.chi2_contingency(contingency_table)
    return p, contingency_table
