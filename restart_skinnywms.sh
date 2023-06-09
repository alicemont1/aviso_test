#!/bin/bash

# fetching s3 data and moving it to data dir
data_loc=$1
python fetch_s3.py $data_loc
echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - Moving from '$data_loc' to SkinnyWMS data dir at '$SKINNYWMS_DATA_DIR'" >> fetch_s3.log
mv $data_loc $HOME/data

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