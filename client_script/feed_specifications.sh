#!/bin/bash

# Note: Ensure that the server is running and listening on port 8000 before executing this script.
# This script finds all YAML files in the 'specifications' directory and sends them to the server at http://localhost:8000/upload.
# Make sure to have curl installed on your system to run this script.
# Usage: Save this script as feed_specifications.sh and run it in a terminal.
# Example: ./feed_specifications.sh
# Ensure the script has execute permissions
# by running: chmod +x feed_specifications.sh
# This script is designed to be run in a Unix-like environment.
# It uses the `find` command to locate all YAML files in the 'specifications' directory and its subdirectories.
# The `curl` command is used to send each file to the specified server endpoint.
# Make sure to adjust the server URL if it's different.
# If you want to test this script, ensure that the server is set up to handle file uploads at the specified endpoint.
# The script will print a message for each file it sends, and a final message when all files have been sent.
# Ensure that the 'specifications' directory exists and contains YAML files before running this script.
# This script is intended for use in a development or testing environment.


for file in $(find specifications -type f -name "*.yaml"); do
    echo "Sending $file"
    curl -X POST http://localhost:8000/upload --data-binary @"$file"
done
echo "All files sent."
