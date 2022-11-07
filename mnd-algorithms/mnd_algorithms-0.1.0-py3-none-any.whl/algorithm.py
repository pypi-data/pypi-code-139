from abc import ABC, abstractmethod
from propsettings.configurable import get_dict_settings


class IAlgorithm(ABC):

    @abstractmethod
    def get_name(self):
        """
        Obtener el nombre del algoritmo.
        :return:
        """
        pass

    def configuration_string(self):
        """
        Devuelve un string que representa la configuración actual de este algoritmo.
        El principal objetivo de este método es obtener una representación (en un string) que diferencie
        a las instancias de este algoritmo que tengan diferentes configuraciones entre sí.
        :return:
        """
        settings = get_dict_settings(self)
        return str(settings)

    def __str__(self):
        return self.get_name()

    def __getstate__(self):
        d = self.__dict__.copy()

        try:
            super_d = super(IAlgorithm, self).__getstate__()
            d.update(super_d)
        except AttributeError:
            pass

        return d
