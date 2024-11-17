import io
import uuid

import urllib3
from botocore.session import get_session

from bookworm.settings import S3_ACCESS_KEY, S3_SECRET_KEY
from logger.log import logger


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    def get_client(self):
        return self.session.create_client("s3", **self.config)

    def generate_file_name(self):
        random_file_name = str(uuid.uuid4())
        return random_file_name

    def read_file(self, file):
        try:
            buffer = io.BytesIO()
            chunk_size = 1024
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                buffer.write(chunk)
            buffer.seek(0)
            return buffer
        except Exception as er:
            logger.warning(f"Error read file {er}")

    def upload_file(self, file, file_name, folder: str):
        client = self.get_client()
        key = f"{folder}/{file_name}"
        try:
            client.put_object(
                Body=file,
                Bucket=self.bucket_name,
                Key=key
            )
            logger.info(f"File {file_name} upload to {self.bucket_name}")
            return file_name
        except Exception as er:
            logger.warning(f"Error uploading file: {er}")

    def upload_local_file_to_s3(
            self,
            file_path,
            folder: str,
            file_name: str = None
    ):
        if not file_name:
            file_name = file_path.split("/")[-1]
        try:
            with open(file_path, "rb") as file:
                self.upload_file(file, file_name, folder)
            return file_name
        except Exception as er:
            logger.warning(f"Error open file: {er}")

    def upload_web_file_to_s3(
            self,
            file_url: str,
            folder: str,
            file_name: str = None,
    ):
        if not file_name:
            file_name = file_url.split("/")[-1]
        http = urllib3.PoolManager()
        response = http.request("GET", file_url, preload_content=False)
        buffer = self.read_file(response)
        self.upload_file(buffer, file_name, folder)
        return file_name

    def delete_file_from_s3(self, file_name: str, folder: str):
        client = self.get_client()
        key = f"{folder}/{file_name}"
        try:
            client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(
                f"File {file_name} deleted from "
                f"{self.bucket_name}, folder-{folder}"
            )
        except Exception as er:
            logger.warning(f"Error deleting file {file_name=}: {er}")


bookworm_s3_client = S3Client(
    access_key=S3_ACCESS_KEY,
    secret_key=S3_SECRET_KEY,
    endpoint_url="https://s3.storage.selcloud.ru",
    bucket_name="bookworm-cont",
)
