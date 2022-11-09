from collibra_core.paths.assets_asset_id.get import ApiForget
from collibra_core.paths.assets_asset_id.delete import ApiFordelete
from collibra_core.paths.assets_asset_id.patch import ApiForpatch


class AssetsAssetId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
