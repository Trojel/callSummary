from sqlalchemy.orm import Session
from app.db.models import Company
from app.pydantic_schemas.company import CompanyCreate, CompanyResponse

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def get_company_by_id(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def create_company(db: Session, company: CompanyCreate):

    db_company = Company(name=company.name, country=company.country)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company
