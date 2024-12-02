from sqlalchemy.orm import Session
from app.api.utils.company import create_company
from app.api.utils.contact import create_contact
from app.api.utils.callSummary import create_callSummary
from app.db.models import Company, Contact
from app.pydantic_schemas.company import CompanyCreate
from app.pydantic_schemas.contact import ContactCreate
from app.pydantic_schemas.CallSummary import CallSummaryCreate
from app.services.external_services import get_company_from_contactID, get_contact_info

def handleDBObjects(phone_number: str, call_date: str, call_duration: str, call_summary: str):
    
    contact = get_contact_info(phone_number)
    company = get_company_from_contactID(contact["company_id"])

    data = {
    "company_name": company.get("name", None),
    "country": company.get("country", None),
    "first_name": contact["firstname"],
    "last_name": contact["lastname"],
    "email": contact["email"],
    "phone": phone_number,
    "call_date": call_date,
    "call_duration": call_duration,
    "call_result": None,
    "summary": call_summary
    }


    return data
    
   