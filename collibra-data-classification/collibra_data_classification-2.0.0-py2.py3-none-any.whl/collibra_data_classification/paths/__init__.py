# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from collibra_data_classification.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    DATA_CLASSIFICATION_CLASSIFICATION_MATCHES = "/dataClassification/classificationMatches"
    DATA_CLASSIFICATION_CLASSIFICATION_MATCHES_BULK = "/dataClassification/classificationMatches/bulk"
    DATA_CLASSIFICATION_CLASSIFICATION_MATCHES_CLASSIFICATION_MATCH_ID = "/dataClassification/classificationMatches/{classificationMatchId}"
    DATA_CLASSIFICATION_CLASSIFICATIONS = "/dataClassification/classifications"
    DATA_CLASSIFICATION_CLASSIFICATIONS_CLASSIFICATION_ID = "/dataClassification/classifications/{classificationId}"
    DATA_CLASSIFICATION_CLASSIFICATIONS_CLASSIFY = "/dataClassification/classifications/classify"
    DATA_CLASSIFICATION_CLASSIFICATIONS_BULK = "/dataClassification/classifications/bulk"
