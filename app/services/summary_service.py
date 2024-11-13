
from app.utils.audio_processing import download_mp3_in_memory, transcribe_audio, generate_summary
from app.utils.slackNotification import send_slack_message
from app.services.external_services import attach_hubspot_note


def process_call_summary(call_id, url):
    """Generates a transcription and summary, then sends them to Slack and HubSpot."""

    
     # Step 1: Download audio and generate transcription and summary
    audio_data = download_mp3_in_memory(url)
    transcription = transcribe_audio(audio_data)
    summary = generate_summary(transcription)

    # Step 2: Send summary to HubSpot
    attach_hubspot_note(call_id, summary)
