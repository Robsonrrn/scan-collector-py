import boto3
from botocore.exceptions import ClientError
import os
import time

class SnapshotService:

    def __init__(self, file_name, bucket, object_name):
        self.file_name = file_name
        self.bucket = bucket
        self.object_name = object_name

    def upload_file(self):
        if self.object_name is None:
            self.object_name = self.file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(self.file_name, self.bucket, self.object_name, ExtraArgs={'ACL': 'public-read'})
            time.sleep(1)
            os.remove(self.file_name)
        except ClientError as e:
            return False
        return self.object_name
