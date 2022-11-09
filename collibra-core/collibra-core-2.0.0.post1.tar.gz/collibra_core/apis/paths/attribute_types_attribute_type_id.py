from collibra_core.paths.attribute_types_attribute_type_id.get import ApiForget
from collibra_core.paths.attribute_types_attribute_type_id.delete import ApiFordelete
from collibra_core.paths.attribute_types_attribute_type_id.patch import ApiForpatch


class AttributeTypesAttributeTypeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
