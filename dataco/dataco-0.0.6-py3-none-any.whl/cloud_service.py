import pandas as pd
from io import BytesIO
import boto3


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
