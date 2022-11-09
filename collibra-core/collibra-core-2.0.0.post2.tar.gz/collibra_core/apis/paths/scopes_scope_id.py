from collibra_core.paths.scopes_scope_id.get import ApiForget
from collibra_core.paths.scopes_scope_id.delete import ApiFordelete
from collibra_core.paths.scopes_scope_id.patch import ApiForpatch


class ScopesScopeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
