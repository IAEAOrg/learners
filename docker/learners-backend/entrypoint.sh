#!/bin/sh

# Initially wait for hugo builder to start up
echo "Wait until hugo build completed."
sleep 5

# Define the path to the file to wait for
file_to_wait_for="/app/webroot/hugo/exercises.json"

# Define the command to run
learners_start_cmd="gunicorn --certfile=/app/ssl/learners.crt --keyfile=/app/ssl/learners.key  --worker-class gevent --timeout 90 --bind 0.0.0.0:5000 backend:app"

# Function to check if the file is present
wait_until_file_exists() {
  while [ ! -f "$file_to_wait_for" ]; do
    sleep 2
  done
}

# Run the function to wait for the file
wait_until_file_exists

# Run your command after the file is present
eval "$learners_start_cmd"