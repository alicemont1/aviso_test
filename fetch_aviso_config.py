import os
import sys
from dotenv import load_dotenv
import requests
import json
from pyaviso import NotificationManager
from pyaviso.user_config import UserConfig
from logging_config import logger


# Load env file with credentials for S3 bucket
dotenv_path = os.path.join(os.getenv("HOME"), ".env")
load_dotenv(dotenv_path)
VM_UUID = os.getenv('VM_UUID')
DATAVISOR_SERVER_URL = os.getenv('DATAVISOR_SERVER_URL')
AVISO_CONFIG_DIR = os.getenv('AVISO_CONFIG_DIR')


# CONFIG_URL = f"{DATAVISOR_SERVER_URL}/api/v1/aviso-config-for-vm/{VM_UUID}"
CONFIG_URL = f"{DATAVISOR_SERVER_URL}/api/v1/aviso-alt-config-for-vm/{VM_UUID}"

def create_key_file(key):
    aviso_key_file=f"{AVISO_CONFIG_DIR}/key"
    with open(aviso_key_file, "w") as f:
        f.write(key)

# def run_aviso(aviso_config):
#     user_conf = UserConfig(
#         notification_engine=aviso_config.get('notification_engine'),
#         configuration_engine=aviso_config.get('configuration_engine'),
#         schema_parser=aviso_config.get('schema_parser'),
#         remote_schema=aviso_config.get('remote_schema'),
#         auth_type=aviso_config.get('auth_type'),
#         username=aviso_config.get('username'),
#         key_file=f"{AVISO_CONFIG_DIR}/key"
#     )
#     aviso = NotificationManager()

#     try:
#         conf_listeners = {"listeners": aviso_config.get('listeners')}
#         aviso.listen(
#             listeners=conf_listeners,
#             config=user_conf,
#             from_date=aviso_config.get('from_date'),
#             to_date=aviso_config.get('to_date'),
#             now=aviso_config.get('now'),
#             catchup=False
#             )
#     except Exception as e:
#         logger.error(e)
#         raise e

def run_aviso(aviso_config):

    user_conf = UserConfig(
        notification_engine=aviso_config.get('notification_engine'),
        configuration_engine=aviso_config.get('configuration_engine'),
        schema_parser=aviso_config.get('schema_parser'),
        remote_schema=aviso_config.get('remote_schema'),
        auth_type=aviso_config.get('auth_type'),
        username=aviso_config.get('user_email'),
        key_file=f"{AVISO_CONFIG_DIR}/key"
    )
    aviso = NotificationManager()

    try:
        conf_listeners = {"listeners": aviso_config.get('listeners')}
        aviso.listen(
            listeners=conf_listeners,
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
    # alt_response = requests.get(ALT_CONFIG_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    # elif alt_response.status_code == 200:
    #     return alt_response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Error Response Body:")
        print(response.text)

def main():
    application_key = sys.argv[1]
    config_dict = fetch_configs(application_key)
    create_key_file(config_dict.get("key"))
    run_aviso(config_dict)

if __name__ == "__main__":
    main()