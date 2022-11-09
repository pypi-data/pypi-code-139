from collibra_core.paths.relation_types_bulk.post import ApiForpost
from collibra_core.paths.relation_types_bulk.delete import ApiFordelete
from collibra_core.paths.relation_types_bulk.patch import ApiForpatch


class RelationTypesBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
