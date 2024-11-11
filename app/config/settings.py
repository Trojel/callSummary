import os
from dotenv import load_dotenv
import base64

load_dotenv()

# Slack configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Aircall API credentials
AIRCALL_APP_TOKEN = os.getenv("aircall_app_token")
AIRCALL_API_TOKEN = os.getenv("aircall_api_token")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# HubSpot configuration
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")