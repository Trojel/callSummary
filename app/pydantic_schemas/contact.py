from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: str
    company_id: Optional[int] = None

    class Config:
        orm_mode = True


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True