import requests
from services.external_services import get_contactID, create_contact_url
from config.headers import SLACK_HEADERS
import re


def send_slack_message(channel, phone_number):

    formatted_phone_number = phone_number.replace(" ", "")
    
    uk_pattern = re.compile(r"^\+44\d{10}$|^0\d{10}$")
    if not uk_pattern.match(formatted_phone_number):
        print(f"Phone number {phone_number} is not a UK number")
        return

    contact_id = get_contactID(formatted_phone_number)
    contact_url = create_contact_url(contact_id)

    data = {
        "channel": channel,
        "text": "A new call has been received from a customer. Click here to view the summary: " + contact_url,
    }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json=data)
    response.raise_for_status()
    if response.status_code == 200:
        print("Slack message sent successfully")
    else:
        print("Slack message failed to send" + response.text)




