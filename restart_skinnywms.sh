#!/bin/bash

# fetching s3 data and moving it to data dir
data_loc=$1

echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - Fetching '$data_loc' from s3 bucket" >> fetch_s3.log
python fetch_s3.py $data_loc

if [ -f "$data_loc" ]; then
  mv "$data_loc" "$HOME/data"
  echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - '$data_loc' was found and moved into to SkinnyWMS data dir at '$HOME/data'" >> fetch_s3.log
else
  echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - '$data_loc' file does not exist. Terminating." >> fetch_s3.log
  exit 1
fi

# restarting skinnywms service
IMAGE_NAME="ecmwf/skinnywms"
SERVICE_NAME="skinnywms"
SERVICE_STATUS=$(docker-compose ps -q "$SERVICE_NAME")

if [ -n "$SERVICE_STATUS" ]; then
    docker-compose restart "$SERVICE_NAME" 2>> fetch_s3.log
    echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - Container for service '$SERVICE_NAME' restarted successfully." >> fetch_s3.log

else
    echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - Service '$SERVICE_NAME' is not running." >> fetch_s3.log
fi