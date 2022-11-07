import abc
from algorithms.algorithm import IAlgorithm


class IDescriptor(IAlgorithm):

	@abc.abstractmethod
	def features(self, img):
		"""
		Extraer rasgos de una imagen.
		:param img imagen a la que se le desea extraer los rasgos.
		:return: vector de rasgos.
		"""
		raise NotImplementedError
