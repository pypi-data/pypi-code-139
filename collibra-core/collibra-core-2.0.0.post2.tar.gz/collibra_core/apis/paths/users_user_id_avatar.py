from collibra_core.paths.users_user_id_avatar.get import ApiForget
from collibra_core.paths.users_user_id_avatar.delete import ApiFordelete
from collibra_core.paths.users_user_id_avatar.patch import ApiForpatch


class UsersUserIdAvatar(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
