from datetime import datetime, timedelta
from venv import logger

import boto3
from botocore.config import Config
from botocore.signers import generate_presigned_url
from app.core.config import config


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id = config.aws_access_key_id,
            aws_secret_access_key = config.aws_secret_access_key,
            region_name = config.aws_region_name,
            endpoint_url = config.aws_url,
            config = Config(signature_version="s3v4")
        )
        self.cache = {}

    def upload_file(self, file, bucket_name, path):
        self.s3.upload_fileobj(file, bucket_name, path)

    def generate_presigned_url(self, bucket_name, path, expiration=3600):
        cache_key = f"{bucket_name}/{path}"
        if cache_key in self.cache:
            url, expiry_time = self.cache[cache_key]
            if datetime.now() < expiry_time:
                return url

        url = self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": path},
            ExpiresIn=expiration
        )
        expiry_time = datetime.now() + timedelta(seconds=expiration)
        self.cache[cache_key] = (url, expiry_time)
        return url

    def get_object(self, bucket_name, path):
        url = self.generate_presigned_url(bucket_name, path)
        return url

    def download_file(self, bucket_name, path, file):
        self.s3.download_fileobj(bucket_name, path, file)

s3_client = S3Client()