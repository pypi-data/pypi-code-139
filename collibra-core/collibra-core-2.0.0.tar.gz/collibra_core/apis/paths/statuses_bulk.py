from collibra_core.paths.statuses_bulk.post import ApiForpost
from collibra_core.paths.statuses_bulk.delete import ApiFordelete
from collibra_core.paths.statuses_bulk.patch import ApiForpatch


class StatusesBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
