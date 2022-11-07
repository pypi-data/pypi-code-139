import abc
from algorithms.algorithm import IAlgorithm


class ITracker(IAlgorithm):

	@abc.abstractmethod
	def track(self, img):
		"""
		Devuelve una lista de rectángulos con su respectivo id.
		:param img:
		:return: lista de elementos en la forma (box, id) => ((int, int, int, int), int)
		"""
		raise NotImplementedError

	@abc.abstractmethod
	def reset(self):
		"""
		Limpiar estado actual del tracker. Debe ser usado para cuando se quiera limpiar cualquier tipo de información
		que el tracker mantenga (usualmente información temporal).
		:return:
		"""
		raise NotImplementedError
