import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
    """      

    def __init__(self, p:float=.5, n:int=20):
        Distribution.__init__(self)
        self.p = p
        self.n = n
        self.calculate_mean()
        self.calculate_stdev()



    def calculate_mean(self) -> float:
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """

        self.mean = self.n * self.p
        return self.mean
         

    def calculate_stdev(self) -> float:
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

        self.stdev = math.sqrt(self.calculate_mean()*(1 - self.p))
        return self.stdev

    def replace_stats_with_data(self) -> tuple:
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
        self.n = len(self.data)
        self.p = self.data.count(1)/self.n
        self.calculate_mean()
        self.calculate_stdev()

        return self.p, self.n
    
    def plot_bar(self) -> None:
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        plt.bar(self.data, height=max(self.data))
        plt.title('Histogram of Data')
        plt.xlabel('data')
        plt.ylabel('count')
    
    def pdf(self, k:float) -> float:
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        return self.nCk(self.n, k)*self.p**k*(1-self.p)**(self.n-k)

    def plot_bar_pdf(self) -> tuple:
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """

        mu = self.mean
        sigma = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)

        # calculates the interval between x values
        interval = (max_range - min_range) // self.n

        x = []
        y = []

        # calculate the x values to visualize
        for i in range(self.n):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].bar(self.data, height=1.0)
        axes[0].set_title('Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Binomial Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y
                
    def __add__(self, other:object) -> object:
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise Exception(error)
                
        result = Binomial()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
        result.p = 1/2*(self.p + other.p)
        result.n = self.n + other.n

        return result
                        
    def __repr__(self) -> str:
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial
        
        """
        return "p {}, n {}, mean {}, standard deviation {}".format(self.p, self.n, self.mean, self.stdev)
