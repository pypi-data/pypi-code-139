# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 13:45:29 2022

@author: DimitriBianco
"""

#Credit Risk Library

#Logistic Regression
import statsmodels.api as sm
import pandas as pd
import lxml
from statsmodels.stats.outliers_influence import variance_inflation_factor

#Setting up test data for building the package
data = pd.read_csv("C:/Users/DimitriBianco/OneDrive - AGORA Data/Documents/Python/Data/Credit_Test.csv")

# defining the dependent and independent variables
x_vars = data[['ltv', 'PastDefault', 'x']]
y_var = data[['y']]
   
# building the model and fitting the data
log_reg = sm.Logit(y_var, x_vars).fit()

#Search all attributes of a model.
for attr in dir(log_reg):
    if not attr.startswith('_'):
        print(attr)







#----Generates a more complete logistic regression with Wald Chi-Squared and VIF.----
def logistic_table(fitted):
    #Wald Chi-Squared
    log_sum = fitted.summary()
    results_as_html = log_sum.tables[1].as_html()
    log_results = pd.read_html(results_as_html, header=0, index_col=0)[0]
    log_results['WaldChiSq'] = (log_results['coef']/log_results['std err'])**2

    #VIF
    log_results['VIF'] = [variance_inflation_factor(x_vars.values, i) for i in range(len(x_vars.columns))]
    return log_results    
#Required
#import statsmodels.api as sm
#import pandas as pd
#import lxml
#from statsmodels.stats.outliers_influence import variance_inflation_factor

#Test the logistic output table
foobar = logistic_table(log_reg)









#----Build a Gains Table function----

#Dep_Var and Pred_Var need to be in one data set.
pred_data = pd.concat([data, pd.DataFrame(log_reg.fittedvalues)], axis=1)
pred_data.rename(columns = {0:'Pred'}, inplace = True)
print(pred_data.columns)

 

    
#---- Gains Table Function ----    
def gains_table(data, dep_var, pred_var):
    #pred_data = pred_data.sort_values('Pred')
    data['Decile_rank'] = pd.qcut(data[pred_var], 10, labels = False)
    data['Decile_rank'] = data['Decile_rank'] + 1

    #Aggregate the data.
    def gains_agg(x):
        d = {}
        d['Goods'] = x[dep_var].count() - x[dep_var].sum()
        d['Bads'] = x[dep_var].sum()
        d['Total'] = x[dep_var].count()
        d['Cum_Goods'] = d['Goods'].cumsum()
        d['Cum_Bads'] = d['Bads'].cumsum()
        d['Goods_Rate'] = d['Goods'] / d['Total']
        d['Bads_Rate'] = d['Bads'] / d['Total']
        return pd.Series(d, index=['Goods', 'Bads', 'Total', 'Cum_Goods', 'Cum_Bads', 'Goods_Rate', 'Bads_Rate'])
        
        
    gain_pred = data.groupby('Decile_rank').apply(gains_agg)

    gain_pred['Cum_Goods'] = gain_pred['Goods'].cumsum()
    gain_pred['Cum_Bads'] = gain_pred['Bads'].cumsum()
    gain_pred['Cum_Goods_Rate'] = gain_pred['Cum_Goods'] / gain_pred['Total'].cumsum()
    gain_pred['Cum_Bads_Rate'] = gain_pred['Cum_Bads'] / gain_pred['Total'].cumsum()
    return gain_pred
    

#Test example of "gains_table"
test_gains = gains_table(pred_data, 'y', 'Pred')


    



