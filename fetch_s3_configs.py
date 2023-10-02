import requests
import os
from dotenv import load_dotenv
from logging_config import logger

dotenv_path = os.path.join(os.getenv("HOME"), ".env")
load_dotenv(dotenv_path)

DATAVISOR_SERVER_URL = os.getenv('DATAVISOR_SERVER_URL')
VM_UUID = os.getenv('VM_UUID')
DATAVISOR_LOG_PATH = os.getenv('DATAVISOR_LOG_PATH')
APPLICATION_KEY = os.getenv('APPLICATION_KEY')

API_URL=f"{DATAVISOR_SERVER_URL}/api/v1/vms/{VM_UUID}/s3-configs"

def append_env(s3_configs):
    logger.info("Writing S3 vars to .env file")
    with open(dotenv_path, "a") as file:
        for key, value in s3_configs.items():
            file.write(f'{key.upper()}={value}')

headers = {"Content-Type": "application/json", "X-Application-Key": APPLICATION_KEY}
response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    append_env()
    logger.info("PATCH request successful")
else:
    logger.error("PATCH request failed with status code:", response.status_code)
