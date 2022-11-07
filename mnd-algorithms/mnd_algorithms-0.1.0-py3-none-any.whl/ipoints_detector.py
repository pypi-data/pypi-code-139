import abc
from algorithms import IAlgorithm


class IPointsDetector(IAlgorithm):

    @abc.abstractmethod
    def detect_points(self, img, roi=None, **kwargs):
        """
        Detectar puntos en una imagen
        :param img:
        :param roi:
        :return:
        """
        raise NotImplementedError
