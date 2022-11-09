from collibra_core.paths.attributes_bulk.post import ApiForpost
from collibra_core.paths.attributes_bulk.delete import ApiFordelete
from collibra_core.paths.attributes_bulk.patch import ApiForpatch


class AttributesBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
