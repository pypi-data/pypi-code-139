from io import BytesIO

import boto3
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class S3:
    def __init__(self, bucket_name):
        self.bucket = boto3.resource("s3").Bucket(bucket_name)

    def read_csv(self, key, **kwargs):
        obj = self.bucket.Object(key)
        with BytesIO(obj.get()["Body"].read()) as data:
            df = pd.read_csv(data, **kwargs)
        return df

    def read_excel(self, key, **kwargs):
        obj = self.bucket.Object(key)
        with BytesIO(obj.get()["Body"].read()) as data:
            df = pd.read_excel(data, **kwargs)
        return df


class GDrive:
    def __init__(self, key_file_location):
        credentials = service_account.Credentials.from_service_account_file(
            key_file_location
        )
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        scoped_credentials = credentials.with_scopes(scopes)
        api_name = "drive"
        api_version = "v3"
        self.service = build(api_name, api_version, credentials=scoped_credentials)

    def read_file(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        file = BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%")
        file.seek(0)
        return file

    def read_csv(self, file_id, **kwargs):
        file = self.read_file(file_id)
        return pd.read_csv(file, **kwargs)

    def read_excel(self, file_id, **kwargs):
        file = self.read_file(file_id)
        return pd.read_excel(file, **kwargs)

    def search_files_by_name(self, name, page_size=50):
        files = []
        page_token = None
        while True:
            q = f"name contains '{name}'"
            response = (
                self.service.files()
                .list(
                    pageSize=page_size,
                    q=q,
                    fields="nextPageToken,files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        return files
