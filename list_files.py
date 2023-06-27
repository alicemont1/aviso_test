import os

import boto3
from dotenv import load_dotenv

# Load env file with credentials for S3 bucket
dotenv_path = ".env"
load_dotenv(dotenv_path)
LOG_DIR = os.getenv("LOG_DIR")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = "https://storage.ecmwf.europeanweather.cloud"

# Create an S3 client
s3 = boto3.client("s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY)


# List objects in the bucket
response = s3.list_objects(Bucket=S3_BUCKET_NAME)
sorted_list = sorted(response["Contents"], key=lambda x: x["LastModified"])

for obj in sorted_list:
    print(f"""{obj["LastModified"]} {obj["Key"]}""")

