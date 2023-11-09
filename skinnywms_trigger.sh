#!/bin/bash
source $HOME/.env

# Get the name of the task for logging purposes
task_name="skinnywms_trigger"

# Get command line argument
DATA_LOC=$1
S3_URL="s3://$S3_BUCKET_NAME/$DATA_LOC"
FILENAME=$(basename "$S3_URL")
echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - $task_name - '$FILENAME' is the filename" >> $DATAVISOR_LOG_PATH


# Fetch s3 file
echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - $task_name - Fetching '$DATA_LOC' from s3 bucket" >> $DATAVISOR_LOG_PATH
python $DATAVISOR_TRIGGER_CONF_DIR/s3_file_fetcher.py $DATA_LOC

# Check if file was downloaded and move it to skinnywms data dir
if [ -f "/tmp/$FILENAME" ]; then
  mv "/tmp/$FILENAME" "$DATAVISOR_BASE_DIR/data"
  echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - $task_name - '$DATA_LOC' was found and moved into to SkinnyWMS data dir at '$DATAVISOR_BASE_DIR/data'" >> $DATAVISOR_LOG_PATH
else
  echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - $task_name - '/tmp/$FILENAME' file does not exist. Terminating." >> $DATAVISOR_LOG_PATH
  exit 1
fi

# Restart skinnywms service
IMAGE_NAME="ecmwf/skinnywms"
SERVICE_NAME="skinnywms"
SERVICE_STATUS=$(docker-compose ps -q "$SERVICE_NAME")

cd $DATAVISOR_BASE_DIR
docker-compose restart "$SERVICE_NAME" 2>> $DATAVISOR_LOG_PATH

# if [ -n "$SERVICE_STATUS" ]; then
#     docker-compose restart "$SERVICE_NAME" 2>> $DATAVISOR_LOG_PATH
#     echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - SkinnyWMSTrigger - Container for service '$SERVICE_NAME' restarted successfully." >> $DATAVISOR_LOG_PATH

# else
#     echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - SkinnyWMSTrigger - Service '$SERVICE_NAME' is not running." >> $DATAVISOR_LOG_PATH
# fi

echo "================================================================================" >> $DATAVISOR_LOG_PATH
