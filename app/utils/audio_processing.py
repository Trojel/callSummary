import requests
from io import BytesIO
from openai import OpenAI
import json
from typing import List
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



async def generate_report(summarries: str):


    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": '''You are an AI assistant analyzing a collection of support call summaries. 
                Your task is to generate a report summarizing the key themes, common issues, and recurring questions raised by customers. 
                Identify major problem areas, any patterns, and areas for improvement. 
                Your job is to generate a JSON object with the following keys: 
                - "key_themes": a short point summary of repeating features and themes of user's questions.
                - "common_issues": the common issues reported by users.
                - "Areas_for_improvement": the areas that need improvement.
                Always return valid JSON without any code block formatting like ```json.'''
            },
            {
                "role": "user",
                "content": f"{summarries}",
            }
        ]
    )
     # Parse the JSON response from GPT
    response_text = completion.choices[0].message.content
    try:
        report_data = json.loads(response_text)  # Convert JSON string to a Python dictionary
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from GPT response: {e}\nResponse: {response_text}")

    return report_data