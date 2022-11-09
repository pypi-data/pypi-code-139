# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from collibra_importer.paths.import_excel_job import Api

from collibra_importer.paths import PathValues

path = PathValues.IMPORT_EXCELJOB