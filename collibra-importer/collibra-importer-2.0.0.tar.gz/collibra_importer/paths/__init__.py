# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from collibra_importer.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    IMPORT_CSVJOB = "/import/csv-job"
    IMPORT_EXCELJOB = "/import/excel-job"
    IMPORT_JSONJOB = "/import/json-job"
    IMPORT_RESULTS_JOB_ID_ERRORS = "/import/results/{jobId}/errors"
    IMPORT_RESULTS_JOB_ID_SUMMARY = "/import/results/{jobId}/summary"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_EVICT = "/import/synchronize/{synchronizationId}/evict"
    IMPORT_SYNCHRONIZE_EXISTS_SYNCHRONIZATION_ID = "/import/synchronize/exists/{synchronizationId}"
    IMPORT_SYNCHRONIZE = "/import/synchronize"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID = "/import/synchronize/{synchronizationId}"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_CSVJOB = "/import/synchronize/{synchronizationId}/batch/csv-job"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_EXCELJOB = "/import/synchronize/{synchronizationId}/batch/excel-job"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_JSONJOB = "/import/synchronize/{synchronizationId}/batch/json-job"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_CSVJOB = "/import/synchronize/{synchronizationId}/csv-job"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_EXCELJOB = "/import/synchronize/{synchronizationId}/excel-job"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_FINALIZE_JOB = "/import/synchronize/{synchronizationId}/finalize/job"
    IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_JSONJOB = "/import/synchronize/{synchronizationId}/json-job"
