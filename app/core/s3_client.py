import boto3

from app.core.config import config


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id = config.aws_access_key_id,
            aws_secret_access_key = config.aws_secret_access_key,
            region_name = config.aws_region_name,
            endpoint_url = config.aws_url
        )

s3_client = S3Client()