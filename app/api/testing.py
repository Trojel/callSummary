from fastapi import APIRouter
from app.utils.slackNotification import send_slack_message
from app.utils.helpers import get_tags



router = APIRouter()  # Create a router instance


@router.get("/")
def read_root():
    return {"status": "success", "message": "Hello, World! \n William from Support was here"}

@router.get("/health")
def health_check():
    return {"status": "success", "message": "Service is running"}

@router.get("/tags")
def get_tags_endpoint():
    return get_tags()

@router.post("/TestSlackMessage")
def test_hubspot_contact():
    send_slack_message("C07U57YU127", "+44 782 436 7444")