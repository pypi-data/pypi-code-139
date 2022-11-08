from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class KeyObject:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key


class PythonRSA:

    @classmethod
    def generate(cls, size: int) -> KeyObject:
        """
        生成指定长度的秘钥
        :param size:
        :return:
        """
        key = RSA.generate(size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return KeyObject(private_key, public_key)

    @classmethod
    def encrypt(cls, public_key: str, data: str) -> bytes:
        public_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(public_key)
        data = cipher.encrypt(data.encode())
        return data

    @classmethod
    def decrypt(cls, private_key: str, data: bytes) -> bytes:
        privateKey = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(privateKey)
        data = cipher.decrypt(data)
        return data