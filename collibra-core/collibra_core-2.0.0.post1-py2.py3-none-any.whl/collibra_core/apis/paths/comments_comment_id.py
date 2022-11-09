from collibra_core.paths.comments_comment_id.get import ApiForget
from collibra_core.paths.comments_comment_id.delete import ApiFordelete
from collibra_core.paths.comments_comment_id.patch import ApiForpatch


class CommentsCommentId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
