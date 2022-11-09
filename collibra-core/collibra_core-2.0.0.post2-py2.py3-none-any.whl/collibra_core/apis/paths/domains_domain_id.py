from collibra_core.paths.domains_domain_id.get import ApiForget
from collibra_core.paths.domains_domain_id.delete import ApiFordelete
from collibra_core.paths.domains_domain_id.patch import ApiForpatch


class DomainsDomainId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
