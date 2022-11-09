from collibra_core.paths.roles_role_id.get import ApiForget
from collibra_core.paths.roles_role_id.delete import ApiFordelete
from collibra_core.paths.roles_role_id.patch import ApiForpatch


class RolesRoleId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
