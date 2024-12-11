from fastapi import APIRouter, Depends
from app.utils.slackNotification import send_slack_message
from app.utils.helpers import get_tags
from app.api.utils.callSummary import get_callSummaries, get_callSummary_by_id, create_callSummary
from app.db.db_setup import get_db, Session
from app.pydantic_schemas.CallSummary import CallSummaryCreate
from app.services.external_services import get_company_from_contactID, get_contact_info, get_company_from_contactID
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
    send_slack_message("C07U57YU127", "+44 208 759 9036")

@router.post("/callsummary")
async def add_callsummary(callSummary: CallSummaryCreate, db: Session = Depends(get_db)):
    
    create_callSummary(db=db, callSummary=callSummary)
    return {"status": "success", "message": "Company added"}

@router.get("/get-company")
def get_company():
    get_company_from_contactID(10468386801)
    return {"status": "success", "message": "Company added"}

@router.get("/get-contact")
def get_contact():
    get_contact_info("+460107470088")
    return {"status": "success", "message": "got contact info"}