from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .contact import ContactResponse



class CompanyBase(BaseModel):
    name: str
    country: str

    class Config:
        orm_mode = True


class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    contacts: List[ContactResponse] = []

    class Config:
        orm_mode = True


