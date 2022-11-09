from collibra_core.paths.users_user_id.get import ApiForget
from collibra_core.paths.users_user_id.delete import ApiFordelete
from collibra_core.paths.users_user_id.patch import ApiForpatch


class UsersUserId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
