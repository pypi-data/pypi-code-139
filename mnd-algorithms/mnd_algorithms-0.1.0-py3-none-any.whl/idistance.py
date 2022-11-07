import abc
from algorithms.algorithm import IAlgorithm


class IDistance(IAlgorithm):
	dissimilarity = True  # dice si la distancia es de disimilitud

	@abc.abstractmethod
	def measure(self, a, b):
		"""
		Calcular distancia (o similitud) entre 2 elementos.
		:param a:
		:param b:
		:return:
		"""
		raise NotImplementedError
