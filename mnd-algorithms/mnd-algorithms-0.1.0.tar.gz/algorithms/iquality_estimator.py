import abc
from algorithms import IAlgorithm


class IQualityEstimator(IAlgorithm):

    @abc.abstractmethod
    def estimate(self, img, *args, **kwargs):
        """
        Estimate the quality of an image.
        :param img:
        :return:
        """
        pass
