import unittest
from pyspark.sql import DataFrame

from pysparkbundle.test.PySparkTestCase import PySparkTestCase

from p360_export.data.pick.ColumnMappingGetter import ColumnMappingGetter
from p360_export.data.pick.DataPlatformDataPicker import DataPlatformDataPicker
from p360_export.data.pick.FacebookDataPicker import FacebookDataPicker
from p360_export.data.pick.GoogleAdsDataPicker import GoogleAdsDataPicker
from p360_export.data.pick.SFMCDataPicker import SFMCDataPicker
from p360_export.exceptions.data_picker import UserIdMappingMissingException
from p360_export.export.sfmc.FieldNameFixer import FieldNameFixer

TABLE_ID = "table_12345"
QUERY = f"SELECT email_col, gen_col, phone_col from {TABLE_ID}"

CONFIG = {"params": {"mapping": {"Email": "email_col", "Gender": "gen_col", "Phone": "phone_col"}}}

BASE_DF_DATA = [
    ["client_id1", "email1", "m", "unwanted", "phone1", "unwanted2"],
    ["client_id2", "email2", "f", "unwanted", "phone2", "unwanted2"],
    ["client_id3", "email3", "m", "unwanted", "phone3", "unwanted2"],
]
BASE_DF_SCHEMA = ["client_id", "email_col", "gen_col", "unwanted_col", "phone_col", "emailo_col"]

EXPECTED_DF_DATA = [
    ["email1", "m", "phone1"],
    ["email2", "f", "phone2"],
    ["email3", "m", "phone3"],
]
EXPECTED_LIST_BASED_SCHEMA = ["email_col", "gen_col", "phone_col"]
EXPECTED_MAPPING_BASED_SCHEMA = ["EMAIL", "GEN", "PHONE"]


class DataPickerTest(PySparkTestCase):
    @property
    def base_df(self) -> DataFrame:
        return self.spark.createDataFrame(BASE_DF_DATA, BASE_DF_SCHEMA)

    def expected_df(self, schema: list) -> DataFrame:
        return self.spark.createDataFrame(EXPECTED_DF_DATA, schema)

    def test_data_platform_data_frame_builder(self):
        data_picker = DataPlatformDataPicker(self.spark)
        df = data_picker.pick(df=self.base_df, query=QUERY, table_id=TABLE_ID, config=CONFIG)
        self.compare_dataframes(df, self.expected_df(EXPECTED_LIST_BASED_SCHEMA), ["email_col"])

    def test_facebook_data_picker(self):
        data_picker = FacebookDataPicker(self.spark, ColumnMappingGetter())
        df = data_picker.pick(df=self.base_df, query=QUERY, table_id=TABLE_ID, config=CONFIG)
        self.compare_dataframes(df, self.expected_df(EXPECTED_MAPPING_BASED_SCHEMA), ["EMAIL"])

    def test_google_ads_data_picker(self):
        data_picker = GoogleAdsDataPicker(self.spark, ColumnMappingGetter())
        google_ads_schema = ["user_id", "gen_col", "phone_col"]

        google_ads_config = {"params": {"mapping": {"user_id": "email_col", "Gender": "gen_col", "Phone": "phone_col"}}}

        df = data_picker.pick(df=self.base_df, query=QUERY, table_id=TABLE_ID, config=google_ads_config)
        self.compare_dataframes(df, self.expected_df(google_ads_schema), ["user_id"])

    def test_sfmc_data_picker(self):
        data_picker = SFMCDataPicker(self.spark, FieldNameFixer())
        long_column_name = "a" * 200
        expected_column_name = "a" * 128

        query = f"SELECT {long_column_name} from {TABLE_ID}"

        df = self.spark.createDataFrame([["value1"], ["value2"]], [long_column_name])
        expected_df = self.spark.createDataFrame([["value1"], ["value2"]], [expected_column_name])

        picked_df = data_picker.pick(df, query, TABLE_ID, {})
        self.compare_dataframes(picked_df, expected_df, [expected_column_name])

    def test_google_ads_missing_user_id(self):
        data_picker = GoogleAdsDataPicker(self.spark, ColumnMappingGetter())
        with self.assertRaises(UserIdMappingMissingException):
            data_picker.pick(df=self.base_df, query=QUERY, table_id=TABLE_ID, config=CONFIG)


if __name__ == "__main__":
    unittest.main()
