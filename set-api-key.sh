#!/bin/bash

# Generate the API key
API_KEY=$(openssl rand -hex 24)

# Check if API_KEY already exists in the .env file and replace it or append it
if grep -q "API_KEY=" .env; then
    # If API_KEY exists, replace it
    sed -i "s/API_KEY=.*/API_KEY=$API_KEY/" .env
else
    # If API_KEY does not exist, append it
    echo "API_KEY=$API_KEY" >> .env
fi