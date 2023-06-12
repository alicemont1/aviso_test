import os
import boto3
from botocore.exceptions import ClientError
import sys
import logging.config
from dotenv import load_dotenv
import os

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.ini")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("morpheusLogger")

# Load env file with credentials for S3 bucket
dotenv_path = '.env'
load_dotenv(dotenv_path)

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
S3_ENDPOINT_URL = "https://storage.ecmwf.europeanweather.cloud"

class S3Connect:
    def __init__(self):
        self.s3 = self.connect()
    
    def connect(self):
        return boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY
        )

    def fetch_file(self, file_path):
        # Downloading a file from the bucket
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

def main():
    if S3_ACCESS_KEY and S3_SECRET_ACCESS_KEY:
        logger.info(f"Access variables were succesfully retrieved for {S3_BUCKET_NAME}.")
    else:
        logger.error(f"{S3_BUCKET_NAME} access variables are missing from env.")
    
    try:
        s3_file_path = sys.argv[1]
        s3 = S3Connect()
        s3.fetch_file(s3_file_path)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()