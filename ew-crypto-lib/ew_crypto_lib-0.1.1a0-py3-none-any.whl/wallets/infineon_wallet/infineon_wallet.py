from ew_crypto_lib.wallets.ew_wallet import Wallet
import ew_crypto_lib.wallets.infineon_wallet.cmd_lib_wrapper as cmd_lib
from hashlib import sha256
import os
import logging
from logging.config import fileConfig

# Setup logger
log_file_path = os.path.join(os.path.abspath('./'), 'logging.conf')
fileConfig(log_file_path)
logger = logging.getLogger('signer')


class InfineonWallet(Wallet):
    def __init__(self, path: str = '/dev/i2c-1') -> None:
        self._path = path
        self.set_key_slot()
        cmd_lib.init()
    
    def set_key_slot(self, slot=1) -> None:
        self._key_slot=slot
    
    def get_public_key(self) -> str:
        cmd_lib.block2go_select()
        public_key = None
        try:
            key_index = self._key_slot
            pub_key = cmd_lib.block2go_get_pub_key(key_index)
            public_key = bytes(pub_key).hex()
        except Exception:
            return self.generate_key()
        return public_key

    def generate_key(self) -> str:
        cmd_lib.block2go_select()
        key_index = cmd_lib.block2go_gen_key()
        self._key_slot=key_index
        pub_key = cmd_lib.block2go_get_pub_key(key_index)
        return bytes(pub_key).hex()
    
    def sign(self, payload: str) -> bytes:
        hashed = sha256(payload.encode())
        return self.sign_digest(hashed.digest())
        
    def sign_digest(self,payload:bytes) -> bytes:
        key_index = self._key_slot
        byte_data = bytearray(payload)
        err_count = 0
        while True:
            try: 
                cmd_lib.block2go_select()
                logger.debug("Sign digest %s",payload.hex())
                signature = bytes(cmd_lib.block2go_sign(key_index, byte_data))
                logger.debug("Signature %s",signature.hex())
                return signature
            except Exception as err:
                err_count += 1
                logger.error('Sign_digest failure', exc_info=True)
                if err_count>=3:
                    raise err

    @property
    def path(self):
        return self._path
    @property
    def key_slot(self) -> int:
        return self._key_slot
    
    def verify(self, signature: str, message:str, public_key: str = None) -> bool:
        return False
