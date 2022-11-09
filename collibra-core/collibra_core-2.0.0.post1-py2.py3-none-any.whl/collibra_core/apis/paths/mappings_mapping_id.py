from collibra_core.paths.mappings_mapping_id.get import ApiForget
from collibra_core.paths.mappings_mapping_id.delete import ApiFordelete
from collibra_core.paths.mappings_mapping_id.patch import ApiForpatch


class MappingsMappingId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
