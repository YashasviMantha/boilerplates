import boto3
from io import BytesIO
from utils import logger
import botocore

log = logger.get_module_logger(__name__)


class S3Wrapper:
    def __init__(self, prefix):
        self.client = boto3.client(
            "s3",
            endpoint_url=S3_URL,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )
        self.bucket = S3_BUCKET
        self.prefix = prefix

    def fetch_all_file_names(self):
        file_names = self.client.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
        return file_names

    def count_files(self, prefix_dir):
        dir_path = f"{self.prefix}/{prefix_dir}"
        response = self.client.list_objects_v2(Bucket=self.bucket, Prefix=dir_path)
        count = response.get("KeyCount", 0)
        if count > 950:
            log.warning(
                f"High number of files in S3 prefix '{dir_path}': {count} files found. Consider implementing pagination for listing files."
            )
        return count

    def upload_file(self, file_obj, file_name):
        """
        Takes a file obj and uploads inside the prefix that is set on initialization.

        """
        log.debug(f"Uploading file: {self.prefix}/{file_name}")
        file_key = f"{self.prefix}/{file_name}"
        self.client.upload_fileobj(file_obj, Bucket=self.bucket, Key=file_key)

    def download_fileobj(self, file_name):
        file_key = f"{self.prefix}/{file_name}"

        log.debug(f"Downloading File: {file_key}")
        fileobj = BytesIO()
        self.client.download_fileobj(Bucket=self.bucket, Key=file_key, Fileobj=fileobj)
        log.debug(f"Download complete: {file_name}")
        return fileobj

    def download_latest_fileobj(self):
        def get_last_modified_date(obj):
            """Return the LastModified date of the given object."""
            return obj["LastModified"]

        file_names = self.fetch_all_file_names()["Contents"]
        file_obj_meta_data = [
            obj for obj in sorted(file_names, key=get_last_modified_date, reverse=True)
        ][0]

        file_obj = self.download_fileobj(file_obj_meta_data["Key"])
        last_modified = file_obj_meta_data["LastModified"]

        return (file_obj, last_modified)

    def download_file(self, file_name, save_file_as):
        file_key = f"{self.prefix}/{file_name}"

        log.debug(f"Downloading File: {file_key}")
        with open(save_file_as, "wb") as f:
            self.client.download_fileobj(Bucket=self.bucket, Key=file_key, Fileobj=f)
        log.debug(f"Download complete: {file_name}")

    def delete_file(self, file_name):
        file_key = f"{self.prefix}/{file_name}"
        log.debug(f"Deleting {file_key}")
        # log.critical(file_key)
        self.client.delete_object(Bucket=self.bucket, Key=file_key)
        
    def check_if_file_exists(self, file_name):
        file_key = f"{self.prefix}/{file_name}"
        
        try:
            self.client.head_object(Bucket=self.bucket, Key=file_key)
            log.info(f"found file: {file_key}")
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                log.warning(f'file not found: {file_key}')
                return False
            
