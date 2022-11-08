import io
import os
import uuid


class CDNClient:
    class ContentType:
        CSV = "application/csv"
        EXCEL = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        PDF = "application/pdf"

    def __init__(self):
        self.client = None
        self.bucket = None
        self.endpoint = None
        self.env = "development"

    def create_client(self, conf_):
        try:
            import boto3

            assert getattr(conf_, "CDN"), "set CDN"
            self.client = boto3.client(
                "s3",
                region_name=conf_.CDN["REGION"],
                endpoint_url=conf_.CDN["ENDPOINT_URL"],
                aws_access_key_id=conf_.CDN["SPACES_KEY"],
                aws_secret_access_key=conf_.CDN["SPACES_SECRET"],
            )
            self.bucket = conf_.CDN["BUCKET"]
            self.endpoint = conf_.CDN["ENDPOINT_URL"]
            self.env = conf_.ENV
        except KeyError:
            print("CDN configuration is not full")
        except ImportError:
            print("Install boto3 in order to work with upload/download files.")

    def upload(self, path, body: io.BytesIO, content_type):
        assert self.client, "initialize client"
        if self.env == "testing":
            if os.environ.get('save_file', False):
                filename = path.split("/")[-1]
                with open(filename, "wb") as file:
                    file.write(body.getvalue())
            return
        self.client.upload_fileobj(
            body,
            Key=path,
            Bucket=self.bucket,
            ExtraArgs={"ACL": "public-read", "ContentType": content_type},
        )

    @staticmethod
    def generate_key(company_unique_serial, ext):
        return f"c/{company_unique_serial}/template/{uuid.uuid4()}.{ext}"

    def download(self, key):
        file = io.BytesIO()
        assert self.client, "initialize client"
        if self.env == "testing":
            local_file = open(key, "rb")
            file.write(local_file.read())
        else:
            self.client.download_fileobj(self.bucket, key, file)
        file.seek(0)
        return file


cdn_client = CDNClient()
