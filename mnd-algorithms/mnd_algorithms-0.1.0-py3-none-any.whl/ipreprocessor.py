import abc
from algorithms.algorithm import IAlgorithm


class IPreprocessor(IAlgorithm):

	@abc.abstractmethod
	def preprocess(self, img, **kwargs):
		"""
		Realizarle algún preprocesamiento a una imagen.
		:param img: imagen a preprocesar.
		:return: imagen preprocesda.
		"""
		raise NotImplementedError
