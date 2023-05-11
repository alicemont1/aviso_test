#!/bin/bash
data_loc=$1

python fetch_s3.py $data_loc



IMAGE_NAME="ecmwf/skinnywms"

CONTAINER_ID=$(docker ps -qf "ancestor=$IMAGE_NAME")

if [ -n "$CONTAINER_ID" ]; then
    docker restart $CONTAINER_ID
    echo "Container restarted successfully."
else
    echo "No container found with the specified image name."
fi