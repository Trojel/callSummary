from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Contact
from app.pydantic_schemas.contact import ContactResponse, ContactCreate

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(first_name=contact.first_name, last_name=contact.last_name, email=contact.email, phone=contact.phone, company_id=contact.company_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
