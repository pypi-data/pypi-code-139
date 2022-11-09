from collibra_core.paths.asset_types_bulk.post import ApiForpost
from collibra_core.paths.asset_types_bulk.delete import ApiFordelete
from collibra_core.paths.asset_types_bulk.patch import ApiForpatch


class AssetTypesBulk(
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
