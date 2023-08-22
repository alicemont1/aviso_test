import os
import sys
from dotenv import load_dotenv
import requests
import json
from pyaviso import NotificationManager
from pyaviso.user_config import UserConfig
# from logging_config import logger


# Load env file with credentials for S3 bucket
# dotenv_path = os.path.join(os.getenv("HOME"), ".env")
# load_dotenv(dotenv_path)
# S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
# S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
# VM_UUID = os.getenv('VM_UUID')

VM_UUID = "032fca87-c92e-4d68-ba33-63938ffd672e"
CONFIG_URL = f"http://136.156.129.120:80/api/v1/aviso-config-for-vm/{VM_UUID}"
# CONFIG_URL = f"http://127.0.0.1:8001/api/v1/aviso-config-for-vm/{VM_UUID}"



def run_aviso(aviso_config):
    user_conf = UserConfig(
        notification_engine=aviso_config.get('notification_engine'),
        configuration_engine=aviso_config.get('configuration_engine'),
        schema_parser=aviso_config.get('schema_parser'),
        remote_schema=aviso_config.get('remote_schema'),
        auth_type=aviso_config.get('auth_type'),
        username=aviso_config.get('username'),
        key_file=aviso_config.get('key_file')
    )
    aviso = NotificationManager()

    try:
        aviso.listen(
            listeners=aviso_config.get('listeners'),
            config=user_conf,
            from_date=aviso_config.get('from_date'),
            to_date=aviso_config.get('to_date'),
            now=aviso_config.get('now'),
            catchup=False
            )
    except Exception as e:
        logger.error(e)
        raise e
    
    
    

def fetch_configs(application_key):
    headers = {
        'X-Application-Key': application_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(CONFIG_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Error Response Body:")
        print(response.text)

def main():
    appp = sys.argv[1]
    application_key = "d433b108608385238fee0b675f612364a06e33d76413e02f3110d0c89bac1b09"
    config_dict = fetch_configs(application_key)
    run_aviso(config_dict)

if __name__ == "__main__":
    main()