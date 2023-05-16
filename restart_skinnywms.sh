#!/bin/bash

# fetching s3 data and moving it to data dir
data_loc=$1

python fetch_s3.py $data_loc
echo "moving from $data_loc to $SKINNYWMS_DATA_DIR"
mv $data_loc $HOME/data

# restarting skinnywms service
IMAGE_NAME="ecmwf/skinnywms"
SERVICE_NAME="skinnywms"
SERVICE_STATUS=$(docker-compose ps -q "$SERVICE_NAME")

if [ -n "$SERVICE_STATUS" ]; then
    docker-compose restart "$SERVICE_NAME"
    echo "Container for service '$SERVICE_NAME' restarted successfully."
else
    echo "Service '$SERVICE_NAME' is not running."
fi