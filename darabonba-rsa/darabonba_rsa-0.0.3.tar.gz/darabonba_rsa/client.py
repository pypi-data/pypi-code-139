from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class Key:
    def __init__(self, private_key: bytes, public_key: bytes):
        self.private_key = private_key
        self.public_key = public_key


class Client:

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
        return Key(private_key, public_key)

    @classmethod
    def encrypt(cls, public_key: str, data: bytes) -> bytes:
        """
        通过公钥加密数据
        :param public_key:
        :param data:
        :return:
        """
        public_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(public_key)
        data = cipher.encrypt(data)
        return data

    @classmethod
    def decrypt(cls, private_key: str, data: bytes) -> bytes:
        """
        通过私钥解密数据
        :param private_key: 
        :param data:
        :return:
        """
        privateKey = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(privateKey)
        data = cipher.decrypt(data)
        return data