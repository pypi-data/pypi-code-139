from collibra_core.paths.domain_types_bulk.post import ApiForpost
from collibra_core.paths.domain_types_bulk.delete import ApiFordelete
from collibra_core.paths.domain_types_bulk.patch import ApiForpatch


class DomainTypesBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
