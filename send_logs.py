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
DATAVISOR_LOG_PATH = os.getenv('DATAVISOR_LOG_PATH')

API_URL=f"{DATAVISOR_SERVER_URL}/api/v1/vms/{VM_UUID}/push-logs"

with open(DATAVISOR_LOG_PATH, "r") as file:
    logs_content = file.read()

json_data = {
    "vm_uuid_id": VM_UUID,
    "logs": logs_content,
}

headers = {"Content-Type": "application/json", "X-Application-Key": APPLICATION_KEY}
response = requests.patch(API_URL, json=json_data, headers=headers)

if response.status_code == 200:
    logger.info("PATCH request successful")
else:
    logger.error("PATCH request failed with status code:", response.status_code)
