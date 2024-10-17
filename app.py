import base64
from dotenv import load_dotenv
import os
import whisper
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from utils import download_mp3_in_memory, transcribe_audio, generate_summary
import uvicorn
from contextlib import asynccontextmanager
import asyncio

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

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

# Global variable to hold the model
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    await asyncio.sleep(10)  # Delay loading the model by 10 seconds
    # Startup: Load the Whisper model
    print("Loading Whisper model on startup...")
    model = whisper.load_model("base")
    print("Whisper model loaded.")

    yield  # Application will run here

    # Shutdown: Clean up resources if needed
    print("Shutting down application...")
    model = None
    print("Whisper model unloaded.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Webhook received"}


@app.post("/webhook")
async def webhook_endpoint(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()  # Get the JSON payload from the webhook
    print(f"Webhook received: {body}")
    url = body["data"]["recording"]
    call_id = body["data"]["id"]

    if model is None:
        return {"status": "error", "message": "Model not loaded yet."}

    # Make a POST request to Hubspot API
    background_tasks.add_task(attach_hubspot_note, call_id = call_id, url = url)

    # Return succes (HTTP 200) to the webhook
    return {"status": "success", "message": "Webhook received"}



@app.post("/make-post-request")
def attach_hubspot_note(call_id: int, url: str):
    # The URL you want to send the POST request to
    urlEndpoint = f"https://api.aircall.io/v1/calls/{call_id}/comments"

    if model is None:
        return {"status": "error", "message": "Model not loaded yet."}

    audio_data = download_mp3_in_memory(url)
    transcription = transcribe_audio(audio_data, model)
    summary = generate_summary(transcription)
    print(f"Summary: {summary}")


    #Data to send with the POST request
    data = {
        "content": summary
    }

    # Make the POST request
    response = requests.post(urlEndpoint, json=data, headers=headers)
    
    # Return the response from the external server
    return {
        "status_code": response.status_code,
        "response_data": response.json()  # Assuming the response is in JSON format
    }


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)