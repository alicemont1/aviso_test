#!/bin/bash

data_loc=$1
export LOG_FILE_PATH="skinnywms_trigger.log"

# Fetch s3 file
echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - SkinnyWMSTrigger - Fetching '$data_loc' from s3 bucket" >> fetch_s3.log
python s3_file_fetcher.py $data_loc

# Check if file was downloaded and move it to skinnywms data dir
if [ -f "$data_loc" ]; then
  mv "$data_loc" "$HOME/data"
  echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - SkinnyWMSTrigger - '$data_loc' was found and moved into to SkinnyWMS data dir at '$HOME/data'" >> $LOG_FILE_PATH
else
  echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - SkinnyWMSTrigger - '$data_loc' file does not exist. Terminating." >> $LOG_FILE_PATH
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