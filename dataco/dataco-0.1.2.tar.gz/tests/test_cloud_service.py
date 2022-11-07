from src import S3, GDrive


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


class TestGDrive:
    credential_file = ".gtest.json"
    folder_id = "13XilEyMyhy-y6SHuhaMsnhDjcLSZQTUE"
    gdrive = GDrive(credential_file)
    csv_file = "cities.csv"
    csv_file_id = "12nOsIUrlhwe_rcrzhoRP6YzGW6COQZyU"
    excel_file = "foodsales.xlsx"
    excel_file_id = "1fDgts_GzYb5TFa_kynWfC1n-sMElQ0q6"
    excel_sheet = 1

    def test_read_csv(self):
        df = self.gdrive.read_csv(self.csv_file_id)
        assert len(df) == 128

    def test_read_excel(self):
        df = self.gdrive.read_excel(self.excel_file_id, sheet_name=self.excel_sheet)
        assert len(df) == 244

    def test_search_files_by_name(self):
        files = self.gdrive.search_files_by_name("cities.csv")
        assert len(files) == 1
        assert files[0]["id"] == "12nOsIUrlhwe_rcrzhoRP6YzGW6COQZyU"
