# SkinnyWMS Trigger


## Background
This repo is part of the End-to-end use case demonstration for the DestinE MVP.

The entire repo will be cloned inside the EWC hosted VM during "setup phase". The VM setup phase is automated by the repo found in https://github.com/ecmwf-projects/de-use-cases/tree/main/ewc_skinnywms.


## Description
The project contains an aviso listerner configuration file and trigger scripts, which will be called when a notification is received.

The listener will be triggered when a specific file is uploaded to the S3 bucket (representing DestinE data bridge). The notification event will provide the location of the file in its parameters, and the listener will receive this location and pass it as input argument to the trigger script.

This script then downloads the file from the S3 bucket into the VM, and restarts the skinnywms docker container so that the newly downloaded data is served. This process is repeated every time the listener is triggered, meaning that it enables the Skinnywms server to serve multiple data files.


## Execution
Althought this repo is intended to be part of an automated pipeline as described in the backgroud, it can also be used as standalone script.

1. Install the project dependencies with:

```
pip install -r frozen_requirements.txt
```

2. Rename the .env_example file to .env and fill it with your S3 bucket credentials.

3. Run the s3_file_fetcher.py file, which is meant for standalone use, with:

```
python fetch_s3.py <path of file on s3 bucket>
```

 

