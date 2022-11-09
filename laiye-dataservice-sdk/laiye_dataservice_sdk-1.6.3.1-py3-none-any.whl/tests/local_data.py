import threading
from laiye_dataservice.enums import AuthorizationType

# 创建全局ThreadLocal对象:
_local_data = threading.local()

_base_url_key = 'base_url'
_auth_type_key = 'auth_type'
_username_key = 'username'
_password_key = 'password'


def clean_all_data():
    if is_exist_base_url():
        delattr(_local_data, _base_url_key)

    if is_exist_auth_type():
        delattr(_local_data, _auth_type_key)

    if is_exist_username():
        delattr(_local_data, _username_key)

    if is_exist_password():
        delattr(_local_data, _password_key)


# ---- Methods for user info ----

def is_exist_base_url() -> bool:
    return hasattr(_local_data, _base_url_key)


def set_base_url(user):
    setattr(_local_data, _base_url_key, user)


def get_base_url():
    if not is_exist_base_url():
        return None

    return getattr(_local_data, _base_url_key)


# ---- Methods for organization info ----

def is_exist_auth_type() -> bool:
    return hasattr(_local_data, _auth_type_key)


def set_auth_type(auth_type):
    setattr(_local_data, _auth_type_key, AuthorizationType[auth_type])


def get_auth_type():
    if not is_exist_auth_type():
        return None

    return getattr(_local_data, _auth_type_key)


# ---- Methods for organization info ----

def is_exist_username() -> bool:
    return hasattr(_local_data, _username_key)


def set_username(org):
    setattr(_local_data, _username_key, org)


def get_username():
    if not is_exist_username():
        return None

    return getattr(_local_data, _username_key)


# ---- Methods for organization info ----

def is_exist_password() -> bool:
    return hasattr(_local_data, _password_key)


def set_password(org):
    setattr(_local_data, _password_key, org)


def get_password():
    if not is_exist_password():
        return None

    return getattr(_local_data, _password_key)
