from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    country = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Contact model
    contacts = relationship("Contact", back_populates="company", cascade="save-update")

    def __repr__(self):
        return f"<Company(name='{self.name}', vertical='{self.vertical}')>"

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True, nullable=False, unique=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="contacts")
    call_summaries = relationship("CallSummary", back_populates="contact", cascade="save-update")

    def __repr__(self):
        return f"<Contact(name='{self.first_name} {self.last_name}', email='{self.email}')>"

class CallSummary(Base):
    __tablename__ = 'call_summaries'

    id = Column(Integer, primary_key=True, index=True)
    call_date = Column(DateTime(timezone=True), nullable=False, index=True)
    call_duration = Column(String, nullable=False, index=True)
    call_result = Column(String, nullable=False, index=True)
    summary = Column(String, nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Contact model
    contact = relationship("Contact", back_populates="call_summaries")

    def __repr__(self):
        return f"<CallSummary(date='{self.call_date}', result='{self.call_result}')>"
