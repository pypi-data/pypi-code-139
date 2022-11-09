from collibra_core.paths.auth_sessions_current.get import ApiForget
from collibra_core.paths.auth_sessions_current.delete import ApiFordelete


class AuthSessionsCurrent(
    ApiForget,
    ApiFordelete,
):
    pass
