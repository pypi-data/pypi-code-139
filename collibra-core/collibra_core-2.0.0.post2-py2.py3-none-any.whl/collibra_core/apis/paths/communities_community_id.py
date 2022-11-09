from collibra_core.paths.communities_community_id.get import ApiForget
from collibra_core.paths.communities_community_id.delete import ApiFordelete
from collibra_core.paths.communities_community_id.patch import ApiForpatch


class CommunitiesCommunityId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
