import boto3

from app.core.config import config


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name = config.aws_region_name,
        )

