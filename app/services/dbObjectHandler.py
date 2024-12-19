from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.utils.company import create_company
from app.api.utils.contact import create_contact
from app.api.utils.callSummary import create_callSummary
from app.db.models import Company, Contact
from app.pydantic_schemas.company import CompanyCreate
from app.pydantic_schemas.contact import ContactCreate
from app.pydantic_schemas.CallSummary import CallSummaryCreate
from app.services.external_services import get_company_from_contactID, get_contact_info
import datetime

def handleDBObjects(db, phone_number: str, call_date: str, call_duration: str, call_summary: str, call_result: str):
    
    formatted_phone_number = phone_number.replace(" ", "")
    print(f"Formatted phone number: {formatted_phone_number}")
    contact = get_contact_info(formatted_phone_number)
    if contact:
        company = get_company_from_contactID(contact["id"])

    data = {
    "company_name": company["name"] if company else None,
    "country": company["country"] if company else None,
    "first_name": contact["firstname"],
    "last_name": contact.get("lastname", None),
    "email": contact.get("email", None),
    "phone": phone_number,
    "call_date": datetime.datetime.fromtimestamp(call_date),
    "call_duration": call_duration,
    "call_result": call_result,
    "summary": call_summary
    }
   
    # Step 1: Check or create the Company
    company_name = data.get("company_name")
    country = data.get("country")
    company = None

    if company_name and country:
        company = db.query(Company).filter_by(name=company_name, country=country).first()
        if not company:
            company_data = CompanyCreate(name=company_name, country=country)
            company = create_company(db, company_data)

    # Step 2: Check or create the Contact
    contact_email = data.get("email")
    contact_phone = data.get("phone")
    contact = None

    if contact_email or contact_phone:
        contact = db.query(Contact).filter(
            (Contact.phone == contact_phone)
        ).first()
        if not contact:
            contact_data = ContactCreate(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=contact_email,
                phone=contact_phone,
                company_id=company.id if company else None  # Link to Company, if available
            )
            try:
                contact = create_contact(db, contact_data)
            except IntegrityError:
                db.rollback()  # Handle cases where the email or phone already exists

    # Step 3: Create the CallSummary
    call_summary_data = CallSummaryCreate(
        call_date=data.get("call_date"),
        call_duration=data.get("call_duration"),
        call_result=data.get("call_result"),
        summary=data.get("summary"),
        contact_id=contact.id if contact else None  # Link to Contact, or NULL
    )
    db_callSummary = create_callSummary(db, call_summary_data)

    return db_callSummary