from sqlalchemy.orm import Session
from app.db.models import CallSummary
from app.pydantic_schemas.CallSummary import CallSummaryCreate, CallSummaryResponse
from datetime import datetime, timezone


def get_callSummaries(db: Session, skip: int = 0, limit: int = 100, start_date: str = None, end_date: str = None, filterResolved: bool = True, filterUnresolved: bool = True):
    print("Filter Resolved: ", filterResolved)
    query = db.query(CallSummary)
    if start_date:
        query = query.filter(CallSummary.call_date >= datetime.fromtimestamp(int(start_date), tz=timezone.utc))
    if end_date:
        query = query.filter(CallSummary.call_date <= datetime.fromtimestamp(int(end_date), tz=timezone.utc))
    
    if filterResolved and filterUnresolved:
        return query.offset(skip).limit(limit).all()
    
    if filterResolved:
        return query.filter(CallSummary.call_result == "resolved").offset(skip).limit(limit).all()
    
    if filterUnresolved:
        return query.filter(CallSummary.call_result == "unresolved").offset(skip).limit(limit).all()
    
    return query.offset(skip).limit(limit).all()

def get_callSummary_by_id(db: Session, callSummary_id: int):
    return db.query(CallSummary).filter(CallSummary.id == callSummary_id).first()

def create_callSummary(db: Session, callSummary: CallSummaryCreate):
    db_callSummary = CallSummary(call_date=callSummary.call_date, call_duration=callSummary.call_duration, call_result=callSummary.call_result, summary=callSummary.summary, contact_id=callSummary.contact_id)
    db.add(db_callSummary)
    db.commit()
    db.refresh(db_callSummary)
    return db_callSummary

