import pytest


def test_encrypt():
    cryptor = pytest.importorskip("encryption.Cryptor").cryptor
    x, y, z = cryptor.encrypt("test")
    assert len(x) == 4
    assert len(y) == 16
    assert len(z) == 16


def test_decrypt():
    cryptor = pytest.importorskip("encryption.Cryptor").cryptor
    x, y, z = cryptor.encrypt("test")
    assert cryptor.decrypt(x, y, z) == b"test"
