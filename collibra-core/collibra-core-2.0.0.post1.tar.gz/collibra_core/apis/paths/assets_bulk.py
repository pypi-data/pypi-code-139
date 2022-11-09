from collibra_core.paths.assets_bulk.post import ApiForpost
from collibra_core.paths.assets_bulk.delete import ApiFordelete
from collibra_core.paths.assets_bulk.patch import ApiForpatch


class AssetsBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
