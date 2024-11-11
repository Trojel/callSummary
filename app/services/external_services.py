from hubspot import HubSpot
from hubspot.crm.contacts import ApiException, Filter, FilterGroup, PublicObjectSearchRequest
import requests
from config.headers import AIRCALL_HEADERS
from config.settings import HUBSPOT_API_KEY

# Initialize the HubSpot client with your access token
api_client = HubSpot(access_token=HUBSPOT_API_KEY)


def attach_hubspot_note(call_id, summary):
    urlEndpoint = f"https://api.aircall.io/v1/calls/{call_id}/comments"

    #Data to send with the POST request
    data = {
        "content": summary
    }
    # Make the POST request
    response = requests.post(urlEndpoint, json=data, headers=AIRCALL_HEADERS)
    
    #Return the response from the external server
    return {
        "status_code": response.status_code,
        "response_data": response.json()  # Assuming the response is in JSON format
    }


def get_contactID(phone_number):
    try:
        # Create filter and filter group for the phone number
        filter = Filter(property_name="phone", operator="EQ", value=phone_number)
        filter_group = FilterGroup(filters=[filter])
        search_request = PublicObjectSearchRequest(filter_groups=[filter_group], properties=["phone"])

        # Execute the search
        response = api_client.crm.contacts.search_api.do_search(public_object_search_request=search_request)
        if response.results:
            # Extract contact ID of the first match (if any)
            contact_id = response.results[0].id
            return contact_id
        else:
            print("No contact found with that phone number.")
            return None
    except ApiException as e:
        print(f"Exception when calling HubSpot API: {e}")
        return None
    
def create_contact_url(contact_id):
    return f"https://app.hubspot.com/contacts/25045833/{contact_id}/"
