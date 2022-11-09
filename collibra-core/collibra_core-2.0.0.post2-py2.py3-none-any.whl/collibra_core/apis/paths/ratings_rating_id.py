from collibra_core.paths.ratings_rating_id.get import ApiForget
from collibra_core.paths.ratings_rating_id.delete import ApiFordelete
from collibra_core.paths.ratings_rating_id.patch import ApiForpatch


class RatingsRatingId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
