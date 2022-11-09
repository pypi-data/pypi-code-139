import typing_extensions

from collibra_importer.paths import PathValues
from collibra_importer.apis.paths.import_csv_job import ImportCsvJob
from collibra_importer.apis.paths.import_excel_job import ImportExcelJob
from collibra_importer.apis.paths.import_json_job import ImportJsonJob
from collibra_importer.apis.paths.import_results_job_id_errors import ImportResultsJobIdErrors
from collibra_importer.apis.paths.import_results_job_id_summary import ImportResultsJobIdSummary
from collibra_importer.apis.paths.import_synchronize_synchronization_id_evict import ImportSynchronizeSynchronizationIdEvict
from collibra_importer.apis.paths.import_synchronize_exists_synchronization_id import ImportSynchronizeExistsSynchronizationId
from collibra_importer.apis.paths.import_synchronize import ImportSynchronize
from collibra_importer.apis.paths.import_synchronize_synchronization_id import ImportSynchronizeSynchronizationId
from collibra_importer.apis.paths.import_synchronize_synchronization_id_batch_csv_job import ImportSynchronizeSynchronizationIdBatchCsvJob
from collibra_importer.apis.paths.import_synchronize_synchronization_id_batch_excel_job import ImportSynchronizeSynchronizationIdBatchExcelJob
from collibra_importer.apis.paths.import_synchronize_synchronization_id_batch_json_job import ImportSynchronizeSynchronizationIdBatchJsonJob
from collibra_importer.apis.paths.import_synchronize_synchronization_id_csv_job import ImportSynchronizeSynchronizationIdCsvJob
from collibra_importer.apis.paths.import_synchronize_synchronization_id_excel_job import ImportSynchronizeSynchronizationIdExcelJob
from collibra_importer.apis.paths.import_synchronize_synchronization_id_finalize_job import ImportSynchronizeSynchronizationIdFinalizeJob
from collibra_importer.apis.paths.import_synchronize_synchronization_id_json_job import ImportSynchronizeSynchronizationIdJsonJob

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.IMPORT_CSVJOB: ImportCsvJob,
        PathValues.IMPORT_EXCELJOB: ImportExcelJob,
        PathValues.IMPORT_JSONJOB: ImportJsonJob,
        PathValues.IMPORT_RESULTS_JOB_ID_ERRORS: ImportResultsJobIdErrors,
        PathValues.IMPORT_RESULTS_JOB_ID_SUMMARY: ImportResultsJobIdSummary,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_EVICT: ImportSynchronizeSynchronizationIdEvict,
        PathValues.IMPORT_SYNCHRONIZE_EXISTS_SYNCHRONIZATION_ID: ImportSynchronizeExistsSynchronizationId,
        PathValues.IMPORT_SYNCHRONIZE: ImportSynchronize,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID: ImportSynchronizeSynchronizationId,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_CSVJOB: ImportSynchronizeSynchronizationIdBatchCsvJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_EXCELJOB: ImportSynchronizeSynchronizationIdBatchExcelJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_JSONJOB: ImportSynchronizeSynchronizationIdBatchJsonJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_CSVJOB: ImportSynchronizeSynchronizationIdCsvJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_EXCELJOB: ImportSynchronizeSynchronizationIdExcelJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_FINALIZE_JOB: ImportSynchronizeSynchronizationIdFinalizeJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_JSONJOB: ImportSynchronizeSynchronizationIdJsonJob,
    }
)

path_to_api = PathToApi(
    {
        PathValues.IMPORT_CSVJOB: ImportCsvJob,
        PathValues.IMPORT_EXCELJOB: ImportExcelJob,
        PathValues.IMPORT_JSONJOB: ImportJsonJob,
        PathValues.IMPORT_RESULTS_JOB_ID_ERRORS: ImportResultsJobIdErrors,
        PathValues.IMPORT_RESULTS_JOB_ID_SUMMARY: ImportResultsJobIdSummary,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_EVICT: ImportSynchronizeSynchronizationIdEvict,
        PathValues.IMPORT_SYNCHRONIZE_EXISTS_SYNCHRONIZATION_ID: ImportSynchronizeExistsSynchronizationId,
        PathValues.IMPORT_SYNCHRONIZE: ImportSynchronize,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID: ImportSynchronizeSynchronizationId,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_CSVJOB: ImportSynchronizeSynchronizationIdBatchCsvJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_EXCELJOB: ImportSynchronizeSynchronizationIdBatchExcelJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_BATCH_JSONJOB: ImportSynchronizeSynchronizationIdBatchJsonJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_CSVJOB: ImportSynchronizeSynchronizationIdCsvJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_EXCELJOB: ImportSynchronizeSynchronizationIdExcelJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_FINALIZE_JOB: ImportSynchronizeSynchronizationIdFinalizeJob,
        PathValues.IMPORT_SYNCHRONIZE_SYNCHRONIZATION_ID_JSONJOB: ImportSynchronizeSynchronizationIdJsonJob,
    }
)
