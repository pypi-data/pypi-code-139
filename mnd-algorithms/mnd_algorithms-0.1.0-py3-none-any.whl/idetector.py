import abc
from algorithms.algorithm import IAlgorithm


class IDetector(IAlgorithm):

	@abc.abstractmethod
	def detect(self, img):
		"""
		Detectar objetos en una imagen.
		:param img: imagen en la cual detectar.
		:return: lista de rectángulos con su respectiva certeza.
		"""
		raise NotImplementedError
