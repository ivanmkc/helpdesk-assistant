#!/bin/bash

# Wait until Rasa started and listens on port 4444.
while [ -z "$(netstat -an | grep 4444 | grep -i listen)" ]; do
  echo 'Waiting for Rasa to start ...'
  sleep 1
done
echo 'Rasa started.'

# Start server.
echo 'Starting gunicorn...'
gunicorn --bind :8080 --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 data_generation.chatbots.input_response.input_response_server:app
