from sqlalchemy.orm import Session
from app.db.models import CallSummary
from app.pydantic_schemas.CallSummary import CallSummaryCreate, CallSummaryResponse


def get_callSummaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CallSummary).offset(skip).limit(limit).all()

def get_callSummary_by_id(db: Session, callSummary_id: int):
    return db.query(CallSummary).filter(CallSummary.id == callSummary_id).first()

def create_callSummary(db: Session, callSummary: CallSummaryCreate):
    db_callSummary = CallSummary(call_date=callSummary.call_date, call_duration=callSummary.call_duration, call_result=callSummary.call_result, summary=callSummary.summary, contact_id=callSummary.contact_id)
    db.add(db_callSummary)
    db.commit()
    db.refresh(db_callSummary)
    return db_callSummary

