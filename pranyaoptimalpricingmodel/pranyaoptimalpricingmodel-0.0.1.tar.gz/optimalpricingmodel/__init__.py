
# importing in-built libraries
import scipy.optimize
import math

def calc_new_prod_price(var_cost_list, max_qty, max_price, fixed_cost, profit_margin=0):
  
  variable_cost = sum(var_cost_list)        # Adding up the variable costs (per product)
  
  x_bounds = (0,None)                       # Setting bounds for x and y
  y_bounds = (0,None)

  # max. objective = log(target_price) + log(quantity)
  # subject to constraints,
  # target_price >= variable_cost
  # quantity <= max_quantity
  # target_price <= max_price
  # target_price >= 0
  # quantity >= 0

  result = scipy.optimize.linprog(          # x = target price for product (note: this is simply a base price and not the optimal price)
      [-1,-1],                              # y = quantity of product produced
      A_ub=[[-1,0],[0,1],[1,0]],
      b_ub=[-math.log(variable_cost),math.log(max_qty),math.log(max_price)],
      bounds = [x_bounds,y_bounds]
  )

  if result.success:
    
    target_price = round(math.exp(result.x[0]),2)     # converting back from logarithmic values
    quantity = round(math.exp(result.x[1]),2)

    total_cost = variable_cost * quantity + fixed_cost    # calculating total cost and revenue
    total_revenue = target_price * quantity

    total_profit = total_revenue - total_cost         # calculating total profit

    if profit_margin<=0:                              # user has been allowed to input their own profit margin required
      profit_margin = (total_profit/total_revenue)      # in case they don't, we use the default profit margin that we calculated
    
    optimal_price = round(variable_cost / (1 - profit_margin),2)      # calculating the optimal price

    break_even_qty = round(fixed_cost / (optimal_price - variable_cost)) # calculating the minimum quantity of product that needs to be sold to break even with the fixed costs

    print("             MODEL SUMMARY               ")
    print("----------------------------------------------------------------------------------------------------------------")
    print("The optimal price for the product is: ",optimal_price)
    print("Profit margin is: ", round((profit_margin*100),2), "%")
    print("The minimum quantity of product required to be sold to break even is: ", break_even_qty)
    print("----------------------------------------------------------------------------------------------------------------")

    return optimal_price

  else:
    
    return



def loan_alloc(total_fund, percent_alloc, i, signs):
  """ Function to find loan amount allotments in different banks. Takes 4 inputs. 
  total bank fund, percentage allotment for each loan, rate of interest and the signs for the constraints."""

  c=[] #for storing constraint inequalities
  coeff=[] #for storing the constraint coefficients according to sign

  for j in range(len(percent_alloc)):
    pa=(percent_alloc[j]/100)*total_fund #Value of the total amount to be alloted to the loan

    if signs[j]=='>=': #changes the constraint to positive or negative according to sign
      c.append(-pa)
      coeff.append(-1)
    
    elif signs[j]=='<=': 
      c.append(pa)
      coeff.append(1)

    for j in range(len(i)): #divided the rate of interest percentage by 100
      i[j]=i[j]/100

  result=scipy.optimize.linprog(
      [i[0],i[1],i[2],i[3],i[4],i[5],i[6]],
      A_ub=[[coeff[0],coeff[1],coeff[2],coeff[3],coeff[4],coeff[5],coeff[6]],[coeff[0],0,0,0,0,0,0],[0,coeff[1],0,0,0,0,0],[0,0,coeff[2],0,0,0,0],[0,0,0,coeff[3],0,0,0],[0,0,0,0,coeff[4],0,0],[0,0,0,0,0,coeff[5],0],[0,0,0,0,0,0,coeff[6]]],
      b_ub=[150,c[0],c[1],c[2],c[3],c[4],c[5],c[6]]
  ) #uses linear programming to find optimal solution

  if result.success:
      X=[]
      print("------------ The loan allotments in sequence are: -------------")
      for a in range(7):
        X.append(result.x[a])
        print(f" {round(result.x[a],2)} amount")
      tot_prof=0
      for a in range(7):
        tot_prof+=X[a]*i[a]
      print("The total profit is:------")
      print(tot_prof)

  else:
      print("No solution!")

