"""mse_lib_crypto.aead module."""

import shutil
from pathlib import Path
from typing import List

import nacl.utils
from nacl.secret import SecretBox

AEAD_KEY_LENGHT: int = nacl.secret.SecretBox.KEY_SIZE


def random_key() -> bytes:
    """Generate a random symmetric key for XSalsa20-Poly1305.

    Returns
    -------
    bytes
        Random symmetric key of length AEAD_KEY_LENGHT.

    """
    return nacl.utils.random(AEAD_KEY_LENGHT)


def encrypt(data: bytes, key: bytes) -> bytes:
    """Encrypt bytes `data` using XSalsa20-Poly1305.

    Parameters
    ----------
    data : bytes
        Data to be encrypted.
    key : bytes
        Symmetric key used for encryption.

    Returns
    -------
    bytes
        Ciphertext of `data` using `key`.

    """
    box: SecretBox = SecretBox(key)

    return box.encrypt(data)


def encrypt_file(path: Path, key: bytes, ext: str = ".enc") -> Path:
    """Encrypt file `path` using XSalsa20-Poly1305.

    Parameters
    ----------
    path : Path
        Path to the data to be encrypted.
    key : bytes
        Symmetric key used for encryption.
    ext : str
        Extension for the encrypted file.

    Returns
    -------
    Path
        Path to the encrypted file `path`.

    """
    if not path.is_file():
        raise FileNotFoundError

    out_path: Path = path.with_suffix(f"{path.suffix}{ext}")
    out_path.write_bytes(encrypt(path.read_bytes(), key))

    return out_path


def encrypt_directory(dir_path: Path, patterns: List[str], key: bytes,
                      exceptions: List[str], dir_exceptions: List[str],
                      out_dir_path: Path) -> bool:
    """Encrypt the content of directory `dir_path` using XSalsa20-Poly1305.

    Parameters
    ----------
    dir_path : Path
        Path to the directory to be encrypted.
    patterns: List[str]
        List of patterns to be matched in the directory.
    exceptions: List[str]
        List of files which won't be encrypted.
    dir_exceptions: List[str]
        List of directories which won't be encrypted recursively.
    key : bytes
        Symmetric key used for encryption.
    out_dir_path: Path
        Output directory path.

    Returns
    -------
    bool
        True if success, raise an exception otherwise.

    """
    if not dir_path.is_dir():
        raise NotADirectoryError

    if out_dir_path.exists():
        shutil.rmtree(out_dir_path)

    shutil.copytree(dir_path, out_dir_path)

    for pattern in patterns:  # type: str
        for path in out_dir_path.rglob(pattern):  # type: Path
            if path.is_file() and path.name not in exceptions and all(
                    directory not in path.parts
                    for directory in dir_exceptions):
                encrypt_file(path, key)
                path.unlink()

    return True


def decrypt(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypt bytes `encrypted_data` using XSalsa20-Poly1305.

    Parameters
    ----------
    encrypted_data : bytes
        Encrypted data to be decrypted.
    key : bytes
        Symmetric key used for encryption.

    Returns
    -------
    bytes
        Cleartext of `encrypted_data`.

    """
    box: SecretBox = SecretBox(key)

    return box.decrypt(encrypted_data)


def decrypt_file(path: Path, key: bytes, ext: str = ".enc") -> Path:
    """Decrypt file `path` using XSalsa20-Poly1305.

    Parameters
    ----------
    path : Path
        Path to the data to be decrypted.
    key : bytes
        Symmetric key used for decryption.
    ext : str
        Extension of encrypted file.

    Returns
    -------
    Path
        Path to the decrypted file `path`.

    """
    if not path.is_file():
        raise FileNotFoundError

    if ext not in path.suffixes:
        raise Exception(f"Extension {ext} not found in {path}")

    out_path: Path = path.with_suffix("")
    out_path.write_bytes(decrypt(path.read_bytes(), key))

    return out_path


def decrypt_directory(dir_path: Path, key: bytes, ext: str = ".enc") -> bool:
    """Decrypt the content of directory `dir_path` using XSalsa20-Poly1305.

    Parameters
    ----------
    dir_path : Path
        Path to the directory to be decrypted.
    key : bytes
        Symmetric key used for decryption.
    ext : str
        File extension of encrypted files.

    Returns
    -------
    bool
        True if success, raise an exception otherwise.

    """
    if not dir_path.is_dir():
        raise NotADirectoryError

    for path in dir_path.rglob(f"*{ext}"):  # type: Path
        if path.is_file():
            decrypt_file(path, key)
            path.unlink()

    return True
