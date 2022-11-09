from pyspark.sql import DataFrame
from typing import Dict, Any

from pyspark.sql.session import SparkSession
from p360_export.data.pick.DataPickerInterface import DataPickerInterface
from p360_export.export.sfmc.FieldNameFixer import FieldNameFixer


class SFMCDataPicker(DataPickerInterface):
    def __init__(self, spark: SparkSession, field_name_fixer: FieldNameFixer):
        self.__spark = spark
        self.__field_name_fixer = field_name_fixer

    @property
    def export_destination(self):
        return "sfmc"

    def pick(self, df: DataFrame, query: str, table_id: str, config: Dict[str, Any]) -> DataFrame:
        df.createOrReplaceTempView(table_id)

        result_df = self.__spark.sql(query)

        new_column_names = self.__field_name_fixer.fix(result_df.columns)

        return result_df.toDF(*new_column_names)
