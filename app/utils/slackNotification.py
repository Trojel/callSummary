import requests
from app.services.external_services import get_contact_info, create_contact_url
from app.config.headers import SLACK_HEADERS
from app.utils.helpers import validate_uk_phone_number


def send_slack_message(channel, phone_number, summary):

    if validate_uk_phone_number(phone_number):
        print(f"{phone_number} is a valid UK number.")
    else:
        print(f"{phone_number} is not a valid UK number.")
        return
        
    # Get the contact ID and create a URL to the contact in HubSpot using formatted phone number
    contact = get_contact_info(phone_number.replace(" ", ""))
    contact_id = contact["id"]
    contact_url = create_contact_url(contact_id)

    formatted_text = f"""
    *Summary:* 
    {summary["summary"]}

    *Customer Sentiment:* 
    {summary["customer_sentiment"]}

    *Resolution Status:* 
    {summary["resolution_status"]}

    *Tags:* 
    {summary["tags"]}
    """

    data = {
        "channel": channel,
        "text": formatted_text + f" \n Click here to view the summary: <{contact_url}|View Summary>",
        "mrkdwn": True,
    }

    response = requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json=data)
    response.raise_for_status()
    if response.status_code == 200:
        print("Slack message sent successfully" + response.text)
    else:
        print("Slack message failed to send" + response.text)




