from fastapi import APIRouter, Request, BackgroundTasks
from utils.slackNotification import send_slack_message
from services.summary_service import process_call_summary
from utils.audio_processing import *



router = APIRouter()  # Create a router instance

@router.post("/webhook")
async def webhook_endpoint(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()  # Get the JSON payload from the webhook
    print(f"Webhook received: {body}")
    url = body["data"]["recording"]
    call_id = body["data"]["id"]
    phone_number = body["data"]["raw_digits"]
    
    #model = request.app.state.model
    background_tasks.add_task(process_call_summary, call_id, url)

    #Send notification to UK team slack channel
    background_tasks.add_task(send_slack_message, "C07UCAW5RST", phone_number)

    return {"status": "success", "message": "Webhook received and processing started"}
