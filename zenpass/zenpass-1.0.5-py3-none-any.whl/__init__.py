"""Generate a strong password which includes alphabets, numbers, special characters"""

from .password import PasswordGenerator, ZenPass
from .exception import ZenpassException

randpass = ZenPass.generate

__author__ = 'srg'
__version__ = '1.0.5'

__all__ = [
    'PasswordGenerator',
    'ZenpassException',
    'randpass'
]
