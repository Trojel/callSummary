import requests
from config.headers import AIRCALL_HEADERS

def get_tags():
    response = requests.get("https://api.aircall.io/v1/tags", headers=AIRCALL_HEADERS)

    # Extract the JSON data from the response
    data = response.json()

    # Extract all the 'name' values from the 'tags' array that does not have a 'description'
    tag_names = [tag['name'] for tag in data['tags'] if tag['description'] is None]
    
    return tag_names
