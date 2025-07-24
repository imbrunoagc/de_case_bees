import os
import io
import json
import boto3
from loguru import logger

from typing import Dict, List


class S3Client:
    def __init__(self) -> boto3.client:
        """
        Creates an S3 client using the provided AWS access key, secret key, and endpoint URL.
        Args:
            access_key (str): AWS access key ID.
            secret_key (str): AWS secret access key.
            endpoint_url (str): The endpoint URL for the S3 service.
        Returns:
            boto3.client: A Boto3 S3 client object.
        """
        self.s3_client = boto3.client(
                "s3",
                endpoint_url=os.environ['MINIO_ENDPOINT'],
                aws_access_key_id=os.environ['MINIO_ACCESS_KEY'],
                aws_secret_access_key=os.environ['MINIO_SECRET_KEY'],
                #region_name=os.environ.get('REGION_NAME', 'us-east-1'),
                )
            
    def conn(self):
        # Create and return your S3 client here using access_key and secret_key
        try:
            logger.info("Creating S3 client")
            self.s3_client
            logger.success("S3 client created")
            return self.s3_client
        except Exception as e:
            logger.error(f"Failed to create S3 client: {e}")


class PandasBucket:
    """
    A class to perform operations on S3 (MinIO) with pandas-compatible formats.
    """

    def __init__(self, name: str):
        self.client = S3Client().conn()
        self.name = name

    def __get__(self, name: str) -> io.BytesIO:
        """Get an object from S3."""
        response = self.client.get_object(Bucket=self.name, Key=name)
        data = io.BytesIO(response['Body'].read())
        data.seek(0)
        return data
    
    def __put__(self, name: str, data: io.BytesIO) -> str:
        """Put an object into S3 (MinIO)."""
        self.client.put_object(
            Bucket=self.name, Key=name, Body=data.getvalue()
        )
        return name

    def read_json(self, name: str) -> List:
        """Read a JSON file from S3 as a list/dict (raw)."""
        data_io = self.__get__(name)
        return json.load(data_io)

    def write_json(self, data: Dict, name: str) -> None:
        """Write dictionary as JSON to S3."""
        data_io = io.BytesIO(json.dumps(data, indent=4).encode('utf-8'))
        data_io.seek(0)
        self.__put__(name, data=data_io)