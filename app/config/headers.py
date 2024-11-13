from base64 import b64encode
import base64
from app.config.settings import AIRCALL_APP_TOKEN, AIRCALL_API_TOKEN, SLACK_BOT_TOKEN


credentials = f"{AIRCALL_APP_TOKEN}:{AIRCALL_API_TOKEN}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

AIRCALL_HEADERS = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json"
}


SLACK_HEADERS = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json",
}