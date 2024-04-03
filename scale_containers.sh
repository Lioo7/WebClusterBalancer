#!/bin/bash

# set execute permission on the script if not already set
if [ ! -x "$0" ]; then
    chmod +x "$0"
fi

# Check if the number of instances is provided
if [ -z "$1" ]; then
    echo "Usage: $0 [number_of_instances]"
    exit 1
fi

# Scale up/down the container apps
docker-compose up -d --scale app="$1"

# Restart the nginx service
docker-compose restart nginx