from collibra_core.paths.communities_bulk.post import ApiForpost
from collibra_core.paths.communities_bulk.delete import ApiFordelete
from collibra_core.paths.communities_bulk.patch import ApiForpatch


class CommunitiesBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
