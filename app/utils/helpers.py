import requests
import re
from app.config.headers import AIRCALL_HEADERS

def get_tags():
    response = requests.get("https://api.aircall.io/v1/tags", headers=AIRCALL_HEADERS)

    # Extract the JSON data from the response
    data = response.json()

    # Extract all the 'name' values from the 'tags' array that does not have a 'description'
    tag_names = [tag['name'] for tag in data['tags'] if tag['description'] is None]
    
    return tag_names



def validate_uk_phone_number(phone_number):
    #Validates if the given phone number is a UK number.

    formatted_phone_number = phone_number.replace(" ", "")
    
    uk_pattern = re.compile(r"^\+44\d{10}$|^0\d{10}$")
    if not uk_pattern.match(formatted_phone_number):
        return False
    
    return True
