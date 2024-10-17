import requests
from io import BytesIO
from openai import OpenAI
import whisper
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant at the video commerce software company Sprii. Your job is to generate a short point summary of the provided phone call transcript between a Sprii customer support agent and a customer."},
                    {
                            "role": "user",
                            "content": transcription
                    }
            ]
    )
    return completion.choices[0].message.content
