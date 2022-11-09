from collibra_core.paths.statuses_status_id.get import ApiForget
from collibra_core.paths.statuses_status_id.delete import ApiFordelete
from collibra_core.paths.statuses_status_id.patch import ApiForpatch


class StatusesStatusId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
