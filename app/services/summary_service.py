
from app.utils.audio_processing import download_mp3_in_memory, transcribe_audio, generate_summary
from app.utils.slackNotification import send_slack_message
from app.services.external_services import attach_hubspot_note
from app.services.dbObjectHandler import handleDBObjects
from app.db.db_setup import Session

def process_call_summary(db: Session, call_id, url, phone_number, call_date, call_duration):
    """Generates a transcription and summary, then sends them to Slack and HubSpot."""

    
     # Step 1: Download audio and generate transcription and summary
    audio_data = download_mp3_in_memory(url)
    transcription = transcribe_audio(audio_data)
    summary = generate_summary(transcription)

    # Step 2: Send summary to HubSpot
    attach_hubspot_note(call_id, summary)

    # Step 3: Send summary to Slack
    send_slack_message("C07U57YU127", phone_number, summary)

    # Step 4: Save data to the database
    #DBdata = handleDBObjects(db, phone_number, call_date, call_duration, summary["summary"], summary["resolution_status"])




