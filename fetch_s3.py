import os
import boto3
import sys
import logging.config

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.ini")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("morpheusLogger")

# Initializing variables for the client
S3_BUCKET_NAME = "maes-bucket"  #Fill this in 
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')
S3_ENDPOINT_URL = "https://storage.ecmwf.europeanweather.cloud"  #Fill this in

class S3Connect:
    def __init__(self) -> None:
        self.s3 = boto3.client(
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
        except FileNotFoundError:
            print("File not found")

def main():
    s3_file_path = sys.argv[1]
    S3Connect().fetch_file(s3_file_path)


if __name__ == "__main__":
    main()