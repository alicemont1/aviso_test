#!/bin/bash
source $HOME/.env

# Get the name of the task for logging purposes
task_name="send_logs"

# Set the API endpoint URL
API_URL="$DATAVISOR_SERVER_URL/api/v1/vms/$VM_UUID/push-logs"

# Read the file contents into a variable
log_contents=$(<"$$DATAVISOR_LOG_PATH")
payload = "{'vm_uuid': $VM_UUID, 'log_contents'}"

# Make the API GET call and save the response to the output file
# curl -s -H "Authorization: Bearer $AUTH_TOKEN" "$API_URL" -o "$OUTPUT_FILE"
response_code=$(curl -X PATCH "$API_URL" \
    -H "X-Application-Key: $APPLICATION_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    -w "%{http_code}")

# Check if the response code is 200
if [ "$response_code" -eq 200 ]; then
    echo "$(date +'%d-%m-%Y %H:%M:%S') - INFO - "$task_name" task - VM logs were sent successfully" >> $DATAVISOR_LOG_PATH
else
    echo "$(date +'%d-%m-%Y %H:%M:%S') - ERROR - "$task_name" task - VM log sending failled $response_code" >> $DATAVISOR_LOG_PATH
fi