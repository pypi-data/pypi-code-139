from typing import Literal
from pyspedfiscal.models import Registro
from pyspedfiscal.campos import CampoEnumerate
from typing import List
from pydantic import Field

from .registro_0200 import Registro0200
from .registro_0460 import Registro0460


class IndMov(CampoEnumerate):
    """ Indicador de movimento """
    com_movimento = '0'
    sem_movimento = '1'


class Registro0001(Registro):
    """ ABERTURA DO BLOCO 0 """

    reg: Literal['0001']
    ind_mov: IndMov

    # Registros filhos nivel 2
    registros_0200: List[Registro0200] = Field(
        default_factory=list, exclude=True)
    registros_0460: List[Registro0460] = Field(
        default_factory=list, exclude=True)
