from collibra_core.paths.domain_types_domain_type_id.get import ApiForget
from collibra_core.paths.domain_types_domain_type_id.delete import ApiFordelete
from collibra_core.paths.domain_types_domain_type_id.patch import ApiForpatch


class DomainTypesDomainTypeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
