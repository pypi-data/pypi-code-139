from .enums import AuthorizationType


class UnsupportedAuthorizationType(Exception):
    def __init__(self, auth_type):
        super().__init__(
            f"Unsupported authorization type {auth_type}, it just support " 
            f"[{AuthorizationType.UserCenter}, {AuthorizationType.BuiltInUser}, {AuthorizationType.JwtToken}]"
        )
