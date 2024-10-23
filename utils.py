import requests
from io import BytesIO
from openai import OpenAI
import whisper
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your API credentials
api_id = os.getenv("aircall_app_token")
api_token = os.getenv("aircall_api_token")

# Concatenate the API ID and token with a colon
credentials = f"{api_id}:{api_token}"

# Encode the credentials using Base64
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Construct the headers with the Authorization header
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json"
}

# Function to download MP3 file and store it in memory
def download_mp3_in_memory(url):
    response = requests.get(url)
    audio_data = BytesIO(response.content)
    audio_data.name = "audio.mp3"  # Give a name for the file-like object
    return audio_data

# Whisper transcription from in-memory file
def transcribe_audio(audio_data, model):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_data
    )
    return transcription.text


def generate_summary(transcription):

    response = requests.get("https://api.aircall.io/v1/tags", headers=headers)

    # Extract the JSON data from the response
    data = response.json()

    # Extract all the 'name' values from the 'tags' array that does not have a 'description'
    tag_names = [tag['name'] for tag in data['tags'] if tag['description'] is None]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": '''You are a helpful assistant at the video commerce software company Sprii. 
                Your job is to generate a short point summary of the provided phone call transcript 
                between a Sprii customer support agent and a customer. You must also provide a brief 
                analysis of the customer's sentiment and 'tag' if the problem/query was resolved or unresolved.
                You must also add a 'tag' from the provided list of tags that best describes the call and resolution.'''
            },
            {
                "role": "user",
                "content": f"{transcription}\n Tags: {', '.join(tag_names)}"
            }
        ]
    )
    return completion.choices[0].message.content
