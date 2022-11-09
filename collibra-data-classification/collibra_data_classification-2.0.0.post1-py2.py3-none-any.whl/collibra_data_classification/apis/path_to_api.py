import typing_extensions

from collibra_data_classification.paths import PathValues
from collibra_data_classification.apis.paths.data_classification_classification_matches import DataClassificationClassificationMatches
from collibra_data_classification.apis.paths.data_classification_classification_matches_bulk import DataClassificationClassificationMatchesBulk
from collibra_data_classification.apis.paths.data_classification_classification_matches_classification_match_id import DataClassificationClassificationMatchesClassificationMatchId
from collibra_data_classification.apis.paths.data_classification_classifications import DataClassificationClassifications
from collibra_data_classification.apis.paths.data_classification_classifications_classification_id import DataClassificationClassificationsClassificationId
from collibra_data_classification.apis.paths.data_classification_classifications_classify import DataClassificationClassificationsClassify
from collibra_data_classification.apis.paths.data_classification_classifications_bulk import DataClassificationClassificationsBulk

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.DATA_CLASSIFICATION_CLASSIFICATION_MATCHES: DataClassificationClassificationMatches,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATION_MATCHES_BULK: DataClassificationClassificationMatchesBulk,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATION_MATCHES_CLASSIFICATION_MATCH_ID: DataClassificationClassificationMatchesClassificationMatchId,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS: DataClassificationClassifications,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS_CLASSIFICATION_ID: DataClassificationClassificationsClassificationId,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS_CLASSIFY: DataClassificationClassificationsClassify,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS_BULK: DataClassificationClassificationsBulk,
    }
)

path_to_api = PathToApi(
    {
        PathValues.DATA_CLASSIFICATION_CLASSIFICATION_MATCHES: DataClassificationClassificationMatches,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATION_MATCHES_BULK: DataClassificationClassificationMatchesBulk,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATION_MATCHES_CLASSIFICATION_MATCH_ID: DataClassificationClassificationMatchesClassificationMatchId,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS: DataClassificationClassifications,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS_CLASSIFICATION_ID: DataClassificationClassificationsClassificationId,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS_CLASSIFY: DataClassificationClassificationsClassify,
        PathValues.DATA_CLASSIFICATION_CLASSIFICATIONS_BULK: DataClassificationClassificationsBulk,
    }
)
