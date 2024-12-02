from fastapi import FastAPI
from app.api import testing, webhook  
from sqlalchemy.orm import Session
from app.db.db_setup import get_db, engine
from app.db.models import Base, Company, Contact, CallSummary

app = FastAPI()

# Create database tables
#Base.metadata.create_all(bind=engine)

app.include_router(testing.router)
app.include_router(webhook.router)

#if __name__ == "__main__":
#    uvicorn.run("main:app", port=8000, reload=True)