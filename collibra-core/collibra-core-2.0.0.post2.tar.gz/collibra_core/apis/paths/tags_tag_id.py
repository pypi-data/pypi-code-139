from collibra_core.paths.tags_tag_id.get import ApiForget
from collibra_core.paths.tags_tag_id.delete import ApiFordelete
from collibra_core.paths.tags_tag_id.patch import ApiForpatch


class TagsTagId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
