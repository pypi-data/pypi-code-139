from collibra_core.paths.user_groups_user_group_id.get import ApiForget
from collibra_core.paths.user_groups_user_group_id.delete import ApiFordelete
from collibra_core.paths.user_groups_user_group_id.patch import ApiForpatch


class UserGroupsUserGroupId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
