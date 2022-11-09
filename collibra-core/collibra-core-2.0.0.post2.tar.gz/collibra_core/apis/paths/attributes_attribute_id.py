from collibra_core.paths.attributes_attribute_id.get import ApiForget
from collibra_core.paths.attributes_attribute_id.delete import ApiFordelete
from collibra_core.paths.attributes_attribute_id.patch import ApiForpatch


class AttributesAttributeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
