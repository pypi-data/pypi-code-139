from collibra_core.paths.attribute_types_bulk.post import ApiForpost
from collibra_core.paths.attribute_types_bulk.delete import ApiFordelete
from collibra_core.paths.attribute_types_bulk.patch import ApiForpatch


class AttributeTypesBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
