import requests
import os
from dotenv import load_dotenv
from logging_config import logger

dotenv_path = os.path.join(os.getenv("HOME"), ".env")
load_dotenv(dotenv_path)

DATAVISOR_SERVER_URL = os.getenv('DATAVISOR_SERVER_URL')
VM_UUID = os.getenv('VM_UUID')
DATAVISOR_LOG_PATH = os.getenv('DATAVISOR_LOG_PATH')
DATAVISOR_LOG_PATH_BKP = os.getenv('DATAVISOR_LOG_PATH_BKP')
APPLICATION_KEY = os.getenv('APPLICATION_KEY')

API_URL=f"{DATAVISOR_SERVER_URL}/api/v1/vms/{VM_UUID}/push-logs"


def backup_log(log_content):
    with open(DATAVISOR_LOG_PATH_BKP, 'a') as target_file:
        target_file.write(log_content)

with open(DATAVISOR_LOG_PATH, "r+") as file:
    log_content = file.read()
    json_data = {
        "vm_uuid_id": VM_UUID,
        "logs": log_content,
    }
    headers = {"Content-Type": "application/json", "X-Application-Key": APPLICATION_KEY}
    response = requests.patch(API_URL, json=json_data, headers=headers)

    if response.status_code == 200:
        logger.info("Log PATCH request successful")
        file.truncate(0) # clear content in the file
        backup_log(log_content)
    else:
        logger.error(f"Log PATCH request failed with status code: {response.status_code}")
        logger.error(response.text)






