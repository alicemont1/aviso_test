import os
import boto3
from botocore.exceptions import ClientError
import sys
from dotenv import load_dotenv
from logging_config import logger

dotenv_path = os.path.join(os.getenv("HOME"), ".env")
load_dotenv(dotenv_path)

# Load env file with credentials for S3 bucket
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')


class S3FileFetcher:
    def __init__(self):
        self.s3 = self.connect()
    
    def connect(self):
        return boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY
        )
    
    def check_file_exists(self, file_path: str) -> bool:
        """Checks if the file exists in the bucket.

        :param file_path: Path of the file on the s3 bucket.
        :return: True if the file is in the bucket, false otherwise.
        """

        response = self.s3.list_objects(Bucket=S3_BUCKET_NAME)
        file_contents = [item["Key"] for item in response["Contents"]]
        if file_path in file_contents:
            return True
        else:
            logger.error(f"{file_path} file not found in {S3_BUCKET_NAME} bucket")
            logger.debug(file_contents)
            return False

    def fetch_file(self, file_path: str) -> None:
        """Downloads a file from the s3 bucket, given a file path.

        :param file_path: Path of the file on the s3 bucket.
        """
        try:
            with open(file_path, "wb") as f:
                self.s3.download_fileobj(
                    S3_BUCKET_NAME, file_path, f)
                logger.info(f"{file_path} file was downloaded to {os.environ.get('PWD')}")
        except ClientError as e:
            if e.response['Error']['Message'] == 'Not Found':
                logger.error(f"{file_path} file not found")
            else:
                logger.error(f"Unexpected error: {e.response['Error']['Message']}")

def parse_loc_arguments(loc):
    loc = loc.lstrip("s3://")
    bucket_name = loc.split("/")[0]
    if bucket_name != S3_BUCKET_NAME:
        logger.error(f"Location {bucket_name} is incorrect and do not match the configured credentials for {S3_BUCKET_NAME}.")
    location = loc.lstrip("s3://" + bucket_name)
    return location

def main():
    if S3_ACCESS_KEY and S3_SECRET_ACCESS_KEY:
        logger.info(f"Access variables were succesfully retrieved for {S3_BUCKET_NAME}.")
    else:
        logger.error(f"{S3_BUCKET_NAME} access variables are missing from env.")
    
    try:
        s3_file_path = parse_loc_arguments(sys.argv[1])
        s3 = S3FileFetcher()
        if s3.check_file_exists(s3_file_path):
            s3.fetch_file(s3_file_path)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()