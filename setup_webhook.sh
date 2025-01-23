#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Check if BOT_TOKEN and NGROK_URL are set
if [[ -z "$BOT_TOKEN" || -z "$NGROK_URL" ]]; then
  echo "Error: BOT_TOKEN or NGROK_URL is not set in the .env file."
  exit 1
fi

# Set the webhook URL
WEBHOOK_URL="https://api.telegram.org/bot$BOT_TOKEN/setWebhook"
WEBHOOK_DATA="url=$NGROK_URL/webhook"

# Send the POST request to set the webhook
curl -X POST "$WEBHOOK_URL" -d "$WEBHOOK_DATA"