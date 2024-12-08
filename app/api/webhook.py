from fastapi import APIRouter, Request, BackgroundTasks, Depends
from app.utils.slackNotification import send_slack_message
from app.services.summary_service import process_call_summary
from app.utils.audio_processing import *
from app.db.db_setup import get_db, Session



router = APIRouter()  # Create a router instance

@router.post("/webhook")
async def webhook_endpoint(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    body = await request.json()  # Get the JSON payload from the webhook
    print(f"Webhook received: {body}")
    url = body["data"]["recording"]
    call_id = body["data"]["id"]
    phone_number = body["data"]["raw_digits"]
    call_duration = body["data"]["duration"]
    call_date = body["data"]["started_at"]
    
    background_tasks.add_task(process_call_summary, db=db, call_id=call_id, url=url, phone_number=phone_number, call_date=call_date, call_duration=call_duration)

    return {"status": "success", "message": "Webhook received and processing started"}
