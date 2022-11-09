from collibra_core.paths.relation_types_relation_type_id.get import ApiForget
from collibra_core.paths.relation_types_relation_type_id.delete import ApiFordelete
from collibra_core.paths.relation_types_relation_type_id.patch import ApiForpatch


class RelationTypesRelationTypeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
