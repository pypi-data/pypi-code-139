import abc
from algorithms.algorithm import IAlgorithm


class IAggregator(IAlgorithm):

	@abc.abstractmethod
	def aggregate(self, elements):
		"""
		Agregar varios elementos en uno solo.
		:param elements:
		:return:
		"""
		raise NotImplementedError
