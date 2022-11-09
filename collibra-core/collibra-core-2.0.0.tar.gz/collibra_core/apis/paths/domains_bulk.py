from collibra_core.paths.domains_bulk.post import ApiForpost
from collibra_core.paths.domains_bulk.delete import ApiFordelete
from collibra_core.paths.domains_bulk.patch import ApiForpatch


class DomainsBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
