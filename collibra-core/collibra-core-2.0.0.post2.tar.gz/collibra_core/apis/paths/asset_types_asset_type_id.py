from collibra_core.paths.asset_types_asset_type_id.get import ApiForget
from collibra_core.paths.asset_types_asset_type_id.delete import ApiFordelete
from collibra_core.paths.asset_types_asset_type_id.patch import ApiForpatch


class AssetTypesAssetTypeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
