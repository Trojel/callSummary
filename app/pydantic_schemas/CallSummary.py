from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class CallSummaryBase(BaseModel):
    call_date: datetime
    call_duration: int
    call_result: str
    summary: str
    contact_id: Optional[int] = None

    class Config:
        orm_mode = True


class CallSummaryCreate(CallSummaryBase):
    pass


class CallSummaryResponse(CallSummaryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True