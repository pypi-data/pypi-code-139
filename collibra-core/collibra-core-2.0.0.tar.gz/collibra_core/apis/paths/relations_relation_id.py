from collibra_core.paths.relations_relation_id.get import ApiForget
from collibra_core.paths.relations_relation_id.delete import ApiFordelete
from collibra_core.paths.relations_relation_id.patch import ApiForpatch


class RelationsRelationId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
