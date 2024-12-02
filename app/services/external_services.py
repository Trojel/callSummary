from hubspot import HubSpot
from hubspot.crm.contacts import ApiException, Filter, FilterGroup, PublicObjectSearchRequest
import requests
import json
from app.config.headers import AIRCALL_HEADERS
from app.config.settings import HUBSPOT_API_KEY

# Initialize the HubSpot client with your access token
api_client = HubSpot(access_token=HUBSPOT_API_KEY)


def attach_hubspot_note(call_id, summary):
    urlEndpoint = f"https://api.aircall.io/v1/calls/{call_id}/comments"

    print("Summary data received: ", summary)

    # Construct a text paragraph from the JSON object
    formatted_text = f"""
    **Summary:** 
    {summary["summary"]}

    **Customer Sentiment:** 
    {summary["customer_sentiment"]}

    **Resolution Status:** 
    {summary["resolution_status"]}

    **Tags:** 
     {summary["tags"]}
    """

    print(f"Sending summary to Aircall: {formatted_text}")

    #Data to send with the POST request
    data = {
        "content": formatted_text
    }
    # Make the POST request
    response = requests.post(urlEndpoint, json=data, headers=AIRCALL_HEADERS)
    
    #Return the response from the external server
    return {
        "status_code": response.status_code,
        "response_data": response.json()  # Assuming the response is in JSON format
    }

    

def get_contact_info(phone_number):
    try:
        # Create filter and filter group for the phone number
        filter = Filter(property_name="phone", operator="EQ", value=phone_number)
        filter_group = FilterGroup(filters=[filter])
        search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group],
            properties=["phone", "firstname", "email"]
        )

        # Execute the search
        response = api_client.crm.contacts.search_api.do_search(public_object_search_request=search_request)
        if response.results:
            contact = response.results[0]
            contact_info = {
                "id": contact.id,
                "firstname": contact.properties.get("firstname"),
                "email": contact.properties.get("email"),
                "phone": contact.properties.get("phone"),
            }
            print(f"Contact info retrieved: {contact_info}")
            return contact_info
        else:
            print("No contact found with that phone number.")
            return None
    except ApiException as e:
        print(f"Exception when calling HubSpot API: {e}")
        return None



def get_company_from_contactID(contact_id):
    """
    Retrieve the associated company information for a HubSpot contact.
    Args:
        contact_id (str): HubSpot contact ID
    Returns:
        dict: Dictionary containing company properties, or None if no company is associated.
    """
    # API endpoint for getting contact's company associations
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/companies"
    
    # Set up headers with authentication
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get company associations
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        associations = response.json()

        # Check if there are any associated companies
        if associations['results']:
            # Get the first associated company ID
            company_id = associations['results'][0]['id']
            
            # Make a second API call to get company details
            company_url = f"https://api.hubapi.com/crm/v3/objects/companies/{company_id}?properties=name,country"
            company_response = requests.get(company_url, headers=headers)
            company_response.raise_for_status()
            
            # Extract company properties
            company_properties = company_response.json().get('properties', {})
            print(f"Company information retrieved: {company_properties}")
            return company_properties  # Return as a dictionary
        
        # No associated companies found
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving company information: {str(e)}")
        return None
    except KeyError as e:
        print(f"Unexpected response format: {str(e)}")
        return None



def create_contact_url(contact_id):
    return f"https://app.hubspot.com/contacts/25045833/{contact_id}/"
