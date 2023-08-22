import logging.config
import yaml
import os

log_file_path = os.environ.get('DATAVISOR_LOG_PATH')

#Load the logging configuration from the YAML file
with open('logging.yaml', 'r') as file:
    config = yaml.safe_load(file)
# Replace the variable placeholder in the configuration dictionary
config['handlers']['error_file']['filename'] = log_file_path

# Configure logging using the modified configuration
logging.config.dictConfig(config)

# Use the logger
logger = logging.getLogger('morpheusLogger')
