from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.utils.slackNotification import send_slack_message
from app.utils.audio_processing import generate_report
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
    get_contact_info("+447824367444")
    return {"status": "success", "message": "got contact info"}


@router.get("/callsummaries")
async def get_callsummaries(db: Session = Depends(get_db), start_date: str = None, end_date: str = None, filterResolved: bool = True, filterUnresolved: bool = True):
    return get_callSummaries(db=db, start_date=start_date, end_date=end_date, filterResolved=filterResolved, filterUnresolved=filterUnresolved)

class ReportRequest(BaseModel):
    summarries: str

@router.post("/report")
async def handle_generate_report(request: ReportRequest):
    try:
        print("Summaries: ", request.summarries)
        return await generate_report(summarries=request.summarries)
    except Exception as e:
        print("Something went wrong with report generation")
        return {"status": "error", "message": str(e)}

