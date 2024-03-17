#!/bin/bash

# set execute permission on the script if not already set
if [ ! -x "$0" ]; then
    chmod +x "$0"
fi

# Scale up/down the container apps to 5
docker-compose up -d --scale app=5
