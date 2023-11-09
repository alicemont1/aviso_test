import logging.config
import yaml
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getenv("HOME"), ".env")
load_dotenv(dotenv_path)

log_file_path = os.getenv('DATAVISOR_LOG_PATH')
trigger_conf_dir = os.getenv('DATAVISOR_TRIGGER_CONF_DIR')

#Load the logging configuration from the YAML file
with open(f'{trigger_conf_dir}/logging.yaml', 'r') as file:
    config = yaml.safe_load(file)
# Replace the variable placeholder in the configuration dictionary
config['handlers']['error_file']['filename'] = log_file_path

# Configure logging using the modified configuration
logging.config.dictConfig(config)

# Use the logger
logger = logging.getLogger('morpheusLogger')
