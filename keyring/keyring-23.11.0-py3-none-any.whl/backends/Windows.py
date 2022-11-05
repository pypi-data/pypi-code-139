import logging

from .._compat import properties
from ..backend import KeyringBackend
from ..credentials import SimpleCredential
from ..errors import PasswordDeleteError, ExceptionRaisedContext


with ExceptionRaisedContext() as missing_deps:
    try:
        # prefer pywin32-ctypes
        from win32ctypes.pywin32 import pywintypes
        from win32ctypes.pywin32 import win32cred

        # force demand import to raise ImportError
        win32cred.__name__
    except ImportError:
        # fallback to pywin32
        import pywintypes
        import win32cred

        # force demand import to raise ImportError
        win32cred.__name__

log = logging.getLogger(__name__)


class Persistence:
    def __get__(self, keyring, type=None):
        return getattr(keyring, '_persist', win32cred.CRED_PERSIST_ENTERPRISE)

    def __set__(self, keyring, value):
        """
        Set the persistence value on the Keyring. Value may be
        one of the win32cred.CRED_PERSIST_* constants or a
        string representing one of those constants. For example,
        'local machine' or 'session'.
        """
        if isinstance(value, str):
            attr = 'CRED_PERSIST_' + value.replace(' ', '_').upper()
            value = getattr(win32cred, attr)
        setattr(keyring, '_persist', value)


class DecodingCredential(dict):
    @property
    def value(self):
        """
        Attempt to decode the credential blob as UTF-16 then UTF-8.
        """
        cred = self['CredentialBlob']
        try:
            return cred.decode('utf-16')
        except UnicodeDecodeError:
            decoded_cred_utf8 = cred.decode('utf-8')
            log.warning(
                "Retrieved an UTF-8 encoded credential. Please be aware that "
                "this library only writes credentials in UTF-16."
            )
            return decoded_cred_utf8


class WinVaultKeyring(KeyringBackend):
    """
    WinVaultKeyring stores encrypted passwords using the Windows Credential
    Manager.

    Requires pywin32

    This backend does some gymnastics to simulate multi-user support,
    which WinVault doesn't support natively. See
    https://github.com/jaraco/keyring/issues/47#issuecomment-75763152
    for details on the implementation, but here's the gist:

    Passwords are stored under the service name unless there is a collision
    (another password with the same service name but different user name),
    in which case the previous password is moved into a compound name:
    {username}@{service}
    """

    persist = Persistence()

    @properties.classproperty
    def priority(cls):
        """
        If available, the preferred backend on Windows.
        """
        if missing_deps:
            raise RuntimeError("Requires Windows and pywin32")
        return 5

    @staticmethod
    def _compound_name(username, service):
        return f'{username}@{service}'

    def get_password(self, service, username):
        # first attempt to get the password under the service name
        res = self._get_password(service)
        if not res or res['UserName'] != username:
            # It wasn't found so attempt to get it with the compound name
            res = self._get_password(self._compound_name(username, service))
        if not res:
            return None
        return res.value

    def _get_password(self, target):
        try:
            res = win32cred.CredRead(
                Type=win32cred.CRED_TYPE_GENERIC, TargetName=target
            )
        except pywintypes.error as e:
            if e.winerror == 1168 and e.funcname == 'CredRead':  # not found
                return None
            raise
        return DecodingCredential(res)

    def set_password(self, service, username, password):
        existing_pw = self._get_password(service)
        if existing_pw:
            # resave the existing password using a compound target
            existing_username = existing_pw['UserName']
            target = self._compound_name(existing_username, service)
            self._set_password(
                target,
                existing_username,
                existing_pw.value,
            )
        self._set_password(service, username, str(password))

    def _set_password(self, target, username, password):
        credential = dict(
            Type=win32cred.CRED_TYPE_GENERIC,
            TargetName=target,
            UserName=username,
            CredentialBlob=password,
            Comment="Stored using python-keyring",
            Persist=self.persist,
        )
        win32cred.CredWrite(credential, 0)

    def delete_password(self, service, username):
        compound = self._compound_name(username, service)
        deleted = False
        for target in service, compound:
            existing_pw = self._get_password(target)
            if existing_pw and existing_pw['UserName'] == username:
                deleted = True
                self._delete_password(target)
        if not deleted:
            raise PasswordDeleteError(service)

    def _delete_password(self, target):
        try:
            win32cred.CredDelete(Type=win32cred.CRED_TYPE_GENERIC, TargetName=target)
        except pywintypes.error as e:
            if e.winerror == 1168 and e.funcname == 'CredDelete':  # not found
                return
            raise

    def get_credential(self, service, username):
        res = None
        # get the credentials associated with the provided username
        if username:
            res = self._get_password(self._compound_name(username, service))
        # get any first password under the service name
        if not res:
            res = self._get_password(service)
            if not res:
                return None
        return SimpleCredential(res['UserName'], res.value)
