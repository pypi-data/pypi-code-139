import datetime
import matplotlib.pyplot as plt


# Function slightly modified from polygon sample code to format the date string
def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime("%Y-%m-%d %H:%M:%S")

def plot(currency_pairs):
    # Create a subplot
    fig, axs = plt.subplots(10,figsize=(10,40))
    fig.tight_layout()

    # Variable to keep track of the total profit across currency pairs. 
    tot_profit = 0

    # Loop through the currency pairs
    for ind, currency in enumerate(currency_pairs):
        
        from_ = currency[0]
        to = currency[1]
        
        # The sublists in the following list represent each of the following:
        # hist_return, avg_return, std_return, avg_of_std_return, upper bollinger, lower bollinger
        returns_array = [[],[],[],[],[],[]]
        
        # Extract the data from the classes and put it into a single list for plotting
        for row in currency[2]:
            returns_array[0].append(row.hist_return)
            try:
                returns_array[1].append(row.avg_return)
            except:
                returns_array[1].append(0)
            try:
                returns_array[2].append(row.std_return)
            except:
                returns_array[2].append(0)
            try:
                returns_array[3].append(row.avg_of_std_return)
            except:
                returns_array[3].append(0)
            try:
                returns_array[4].append(row.avg_return + (1.5 * row.std_return))
            except:
                returns_array[4].append(0)
            try:
                returns_array[5].append(row.avg_return - (1.5 * row.std_return))
            except:
                returns_array[5].append(0)
                
        print("The profit/losses for "+from_+to+" calculated with numpy is: %f" % (currency[3].amount -1))
        tot_profit += currency[3].amount - 1
        
        # Plot the line graphs with bollinger bands using the propper formatting
        axs[ind].plot(range(0,len(returns_array[0])),returns_array[0]) # plot the historical returns
        axs[ind].plot(range(0,len(returns_array[4])),returns_array[4]) # plot the upper bollinger band for returns
        axs[ind].plot(range(0,len(returns_array[5])),returns_array[5]) # plot the lower bollinger band for returns
        axs[ind].set(xlabel='Time',ylabel='Return')
        axs[ind].set_title(from_+to+'  Returns Over Time')
        
    # Extra formatting to make sure the axis labels do not overlap the titles
    plt.subplots_adjust(left=0.1,
                        bottom=0.1, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.4, 
                        hspace=0.4)

    plt.show()