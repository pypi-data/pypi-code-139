import abc
from algorithms.algorithm import IAlgorithm


class IClassifier(IAlgorithm):

	@abc.abstractmethod
	def classify(self, img) -> dict:
		"""
		Clasificar una imagen retornando una lista de etiquetas y su correspondiente certeza.
		:param img:
		:return: diccionario de la forma { label: confidence } => { string: float}
		"""
		raise NotImplementedError

	@abc.abstractmethod
	def labels(self):
		"""
		Retorna lista de etiquetas en asociadas a las predicciones que devuelve el método classify.
		El índice de cada etiqueta debe ser el mismo índice de su predicción asociada.
		:return:
		"""
		raise NotImplementedError

	def classification_label(self, img) -> str:
		"""
		Obtener etiqueta con mayor certeza
		:return:
		"""
		c = self.classify(img)
		return str(max(c.items(), key=lambda x: x[1])[0])

	@staticmethod
	def classification_dict(labels, predictions) -> dict:
		"""
		Método útil para crear un diccionario a partir de las etiquetas y las predicciones.
		:param labels:
		:param predictions:
		:return:
		"""
		lc = len(labels)
		pc = len(predictions)
		assert lc == pc, f'Labels count must be equal to predictions count. (labels) {lc} != {pc} (predictions).'
		clasf_dict = {labels[i]: predictions[i] for i in range(lc)}
		return clasf_dict


