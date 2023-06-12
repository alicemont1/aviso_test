#!/bin/bash

# Get command line argument
DATA_LOC=$1

# Source the environment file
source .env
export LOG_FILE_PATH="$LOG_DIR/skinnywms_trigger.log"

# Logging start
echo "===========================================================================================================================" >> $LOG_FILE_PATH

# Fetch s3 file
echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - SkinnyWMSTrigger - Fetching '$DATA_LOC' from s3 bucket" >> fetch_s3.log
python s3_file_fetcher.py $DATA_LOC

# Check if file was downloaded and move it to skinnywms data dir
if [ -f "$DATA_LOC" ]; then
  mv "$DATA_LOC" "$HOME/data"
  echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - SkinnyWMSTrigger - '$DATA_LOC' was found and moved into to SkinnyWMS data dir at '$HOME/data'" >> $LOG_FILE_PATH
else
  echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - SkinnyWMSTrigger - '$DATA_LOC' file does not exist. Terminating." >> $LOG_FILE_PATH
  exit 1
fi

# Restart skinnywms service
IMAGE_NAME="ecmwf/skinnywms"
SERVICE_NAME="skinnywms"
SERVICE_STATUS=$(docker-compose ps -q "$SERVICE_NAME")

if [ -n "$SERVICE_STATUS" ]; then
    docker-compose restart "$SERVICE_NAME" 2>> $LOG_FILE_PATH
    echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - SkinnyWMSTrigger - Container for service '$SERVICE_NAME' restarted successfully." >> $LOG_FILE_PATH

else
    echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - SkinnyWMSTrigger - Service '$SERVICE_NAME' is not running." >> $LOG_FILE_PATH
fi

echo "$separator" >> $LOG_FILE_PATH
