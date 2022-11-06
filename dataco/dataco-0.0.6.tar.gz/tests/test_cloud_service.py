from src.cloud_service import S3


class TestS3:

    test_bucket = "test-data-connector"
    s3 = S3(test_bucket)
    csv_file = "cities.csv"
    excel_file = "foodsales.xlsx"
    excel_sheet = 1

    def test_read_csv(self):
        df = self.s3.read_csv(self.csv_file)
        assert len(df) == 128

    def test_read_excel(self):
        df = self.s3.read_excel(self.excel_file, sheet_name=self.excel_sheet)
        assert len(df) == 244
