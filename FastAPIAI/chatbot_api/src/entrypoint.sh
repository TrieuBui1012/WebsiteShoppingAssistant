#!/bin/bash

if [ "$AWS_EXECUTION_ENV" != "" ]; then
    echo "Running in AWS Lambda environment..."
    # AWS Lambda will automatically invoke the handler
else
    echo "Running locally..."
    # Start Uvicorn for local development
    uvicorn main:app --host 0.0.0.0 --port 8082 --reload
fi