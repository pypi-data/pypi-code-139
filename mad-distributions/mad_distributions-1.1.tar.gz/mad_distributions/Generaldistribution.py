class Distribution:
	
	def __init__(self, mu=0, sigma=1):
		""" Generic distribution class for calculating and 
		visualizing a probability distribution.
	
		Attributes:
			mean (float) representing the mean value of the distribution
			stdev (float) representing the standard deviation of the distribution
			data_list (list of floats) a list of floats extracted from the data file
			"""
		
		self.mean = mu
		self.stdev = sigma
		self.data = []


	def read_data_file(self, file_name: str) -> None:
	
		"""Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute.
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			None
		
		"""
			
		with open(file_name) as file:
			data_list = []
			line = file.readline()
			while line:
				data_list.append(int(line))
				line = file.readline()
		file.close()
	
		self.data = data_list

	def factorial(self, n: int) -> int:
		"""
		Computes factorial of n

		Args:
			(int) n

		Returns: 
			(int) factorial of n
		"""

		f = 1 

		for i in range(1, n+1): f *= i

		return f

	def nCk(self, n: int, k: int) -> int:
		"""
		Compute n ways to choose k

		Args:
			(int) n the maximum population to be chosen from
			(int) k the number to be chosen from n

		Returns:
			(int) the number of k combinations from n
		"""
		
		return self.factorial(n)//(self.factorial(n - k)*self.factorial(k))

	def nPk(self, n: int, k: int) -> int:
		"""
		Compute n permute k

		Args:
			(int) n the maximum population to be permuted
			(int) k the number to be permuted from n

		Returns:
			(int) the number of k permutations from n 
			
		"""
		
		return self.factorial(n)//self.factorial(n - k)

	def nTok(self, n: int, k: int) -> int:
		"""
		Compute n raised to the power k

		Args:
			(int) n the base number
			(int) k the exponential number

		Returns:
			(int) the number n^k
		"""

		return n**k

	def n_sigma(self, n: int) -> int:
		"""
		Sum up to n (Sigma)

		Args:
			(int) n the number to sum up to

		Returns:
			(int) the number n(n+1)/2        
		"""

		if n <= 1: return n

		return self.n_sigma(n-1) + n

	def nSk(self, n: int, k: int) -> int:
		"""
		Compute n ways to choose identical k

		Args:
			(int) n the maximum population to be chosen from
			(int) k the indentical number to be chosen from n

		Returns:
			(int) the number of k combinations from n
		"""
		
		if k == 0: k = 1

		return self.factorial(n)//(self.factorial(n//k)**k)
