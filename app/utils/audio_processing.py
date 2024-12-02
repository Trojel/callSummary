import requests
from io import BytesIO
from openai import OpenAI
import json
from app.config.settings import OPENAI_API_KEY
from app.config.headers import AIRCALL_HEADERS

client = OpenAI(api_key=OPENAI_API_KEY)

# Function to download MP3 file and store it in memory
def download_mp3_in_memory(url):
    response = requests.get(url)
    audio_data = BytesIO(response.content)
    audio_data.name = "audio.mp3"  # Give a name for the file-like object
    return audio_data

# Whisper transcription from in-memory file
def transcribe_audio(audio_data):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_data
    )
    return transcription.text

def generate_summary(transcription):

    response = requests.get("https://api.aircall.io/v1/tags", headers=AIRCALL_HEADERS)

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
                Your job is to generate a JSON object with the following keys: 
                - "summary": a short point summary of the phone call transcript.
                - "customer_sentiment": a brief analysis of the customer's sentiment.
                - "resolution_status": whether the problem/query was resolved or unresolved. Can be "resolved" or "unresolved". 
                - "tags": a tag from the provided list that best describes the call and resolution.

                Always return valid JSON without any code block formatting like ```json.'''
            },
            {
                "role": "user",
                "content": f"{transcription}\n Tags: {', '.join(tag_names)}"
            }
        ]
    )
     # Parse the JSON response from GPT
    response_text = completion.choices[0].message.content
    try:
        summary_data = json.loads(response_text)  # Convert JSON string to a Python dictionary
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from GPT response: {e}\nResponse: {response_text}")

    return summary_data