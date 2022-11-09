from collibra_core.paths.relations_bulk.post import ApiForpost
from collibra_core.paths.relations_bulk.delete import ApiFordelete
from collibra_core.paths.relations_bulk.patch import ApiForpatch


class RelationsBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
