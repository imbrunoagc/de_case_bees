import os
import io
import json
from typing import Dict, List, Union

import boto3
import pandas as pd

class Client:
    """A Class the connection with s3 minio client"""
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=os.environ.get('MINIO_ENDPOINT'),
            aws_access_key_id=os.environ.get('MINIO_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('MINIO_SECRET_KEY'),
            region_name=os.environ.get('REGION_NAME'),
        )

class PandasBucket:
    """
    A Class that operation in s3 ( insert pandas objects ) 
    """

    def __init__(self, name: str):
        self.client = Client.client
        self.name = name
        self.create()
    
    def __put__(self, name: str, data: io.BytesIO) -> str:
        """Put an object into S3 storage. data is the content to upload."""
        self.client.put_object(
            Bucket=self.name, Key=name, Body=data.getvalue()
        )
        return name

    def __get__(self, name: str) -> io.BytesIO:  # noqa PLE302
        """Get an object from S3 storage. name is the key of the object."""
        response = self.client.get_object(Bucket=self.name, Key=name)
        data = io.BytesIO(response['Body'].read())
        data.seek(0)
        return data

    def read_parquet(self, name: str) -> Union[pd.Series, pd.DataFrame]:
        """Read a pandas DataFrame stored as parquet file from S3 storage."""
        data = self.__get__(name)
        return pd.read_parquet(data)

    def read_json(self, name: str) -> List:
        """Read JSON directly from S3 without pandas conversion"""
        data_io = self.__get__(name)
        return json.load(data_io)

    def read(self, name: str, **kwargs) -> Union[pd.Series, pd.DataFrame]:
        """Read a pandas.Series or pandas.Dataframe from S3 storage in the appropriate format."""
        if name.endswith('.parquet'):
            return self.read_parquet(name, **kwargs)
        elif name.endswith('.json'):
            return self.read_json(name, **kwargs)
        
    def write_json(self, data: Dict, name: str) -> None:
        """Write dictionary as JSON to S3 storage"""
        data_io = io.BytesIO(json.dumps(data, indent=4).encode('utf-8'))
        data_io.seek(0)
        return self.__put__(name, data=data_io)
    
    def write_parquet(self, data: pd.DataFrame, name: str, **kwargs) -> None:
        """"Write dataframe"""
        try:
            data.to_parquet(name, **kwargs)
            print(f"File saved with sucessufuly: {self.name}/{name}")
        except Exception as e:
            print(e)
    
    def put_parquet(
        self, df: Union[pd.Series, pd.DataFrame], name: str, **kwargs) -> str:
        """Store a pandas.Series or pandas.Dataframe in parquet format into S3 storage"""
        data = io.BytesIO()
        df.to_parquet(data, engine='pyarrow', **kwargs)
        data.seek(0)
        return self.__put__(name, data=data)