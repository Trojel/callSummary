from sqlalchemy.orm import Session
from app.db.models import CallSummary
from app.pydantic_schemas.CallSummary import CallSummaryCreate, CallSummaryResponse
from datetime import datetime, timezone


def get_callSummaries(db: Session, skip: int = 0, start_date: str = None, end_date: str = None, filterResolved: bool = True, filterUnresolved: bool = True):
    print("Filter Resolved: ", filterResolved)
    query = db.query(CallSummary)
    if start_date:
        query = query.filter(CallSummary.call_date >= datetime.fromtimestamp(int(start_date), tz=timezone.utc))
    if end_date:
        query = query.filter(CallSummary.call_date <= datetime.fromtimestamp(int(end_date), tz=timezone.utc))

    if filterResolved and filterUnresolved:
        pass  # both True, use query as is
    elif filterResolved:
        query = query.filter(CallSummary.call_result == "resolved")
    elif filterUnresolved:
        query = query.filter(CallSummary.call_result == "unresolved")

    results = query.offset(skip).all()
    result_list = []
    for cs in results:
        result_list.append({
            "id": cs.id,
            "summary": cs.summary,
            "call_result": cs.call_result,
            "call_duration": cs.call_duration,
            "call_date": cs.call_date,
            "contact_id": cs.contact_id,
            "first_name": cs.contact.first_name if cs.contact else None,
            "last_name": cs.contact.last_name if cs.contact else None,
            "phone": cs.contact.phone if cs.contact else None,
            "company_name": cs.contact.company.name if cs.contact and cs.contact.company else None
        })
    return result_list

def get_callSummary_by_id(db: Session, callSummary_id: int):
    return db.query(CallSummary).filter(CallSummary.id == callSummary_id).first()

def create_callSummary(db: Session, callSummary: CallSummaryCreate):
    db_callSummary = CallSummary(call_date=callSummary.call_date, call_duration=callSummary.call_duration, call_result=callSummary.call_result, summary=callSummary.summary, contact_id=callSummary.contact_id)
    db.add(db_callSummary)
    db.commit()
    db.refresh(db_callSummary)
    return db_callSummary

