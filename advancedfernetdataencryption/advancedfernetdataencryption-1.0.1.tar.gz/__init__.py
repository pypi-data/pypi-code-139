from .AdvancedFernetDataEncryption import dataDecryption
from .AdvancedFernetDataEncryption import dataEncrpytion
from .AdvancedFernetDataEncryption import generateSessionToken
from .AdvancedFernetDataEncryption import decryption
try:
    from cryptography.fernet import Fernet
except ModuleNotFoundError:
    print("Please install pip install cryptography")

__version__ = "1.0.0"