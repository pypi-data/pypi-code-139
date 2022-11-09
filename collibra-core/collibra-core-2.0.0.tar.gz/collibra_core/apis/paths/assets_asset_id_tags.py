from collibra_core.paths.assets_asset_id_tags.get import ApiForget
from collibra_core.paths.assets_asset_id_tags.put import ApiForput
from collibra_core.paths.assets_asset_id_tags.post import ApiForpost
from collibra_core.paths.assets_asset_id_tags.delete import ApiFordelete


class AssetsAssetIdTags(
    ApiForget,
    ApiForput,
    ApiForpost,
    ApiFordelete,
):
    pass
