import enum


@enum.unique
class FiddlerTimestamp(str, enum.Enum):
    """Supported timestamp formats for events published to Fiddler"""

    EPOCH_MILLISECONDS = 'epoch milliseconds'
    EPOCH_SECONDS = 'epoch seconds'
    ISO_8601 = '%Y-%m-%d %H:%M:%S.%f'
    TIMEZONE = ISO_8601 + '%Z %z'
    INFER = 'infer'


BINSIZE_2_SECONDS = {
    '5 minutes': 300000,
    '1 hour': 3600000,
    '1 day': 86400000,
    '7 days': 604800000,
}

COMPARE_PERIOD_2_SECONDS = {
    '1 day': 86400000,
    '7 days': 604800000,
    '30 days': 2629743000,
    '90 days': 7776000000,
}


@enum.unique
class FileType(str, enum.Enum):
    """Supported file types for ingestion"""

    CSV = '.csv'


@enum.unique
class ServerDeploymentMode(str, enum.Enum):
    F1 = 'f1'
    F2 = 'f2'


@enum.unique
class UploadType(str, enum.Enum):
    """To distinguish between dataset ingestion and event ingestion.
    Supposed to be only internally used.
    """

    DATASET = 'dataset'
    EVENT = 'event'


FIDDLER_CLIENT_VERSION_HEADER = 'X-Fiddler-Client-Version'
