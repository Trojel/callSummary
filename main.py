from fastapi import FastAPI
from app.api import testing, webhook  
from sqlalchemy.orm import Session
from app.db.db_setup import get_db, engine
from app.db.models import Base, Company, Contact, CallSummary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create database tables
#Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:9000",
    "https://coral-app-c58z6.ondigitalocean.app",
    "https://coral-app-c58z6.ondigitalocean.app:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(testing.router)
app.include_router(webhook.router)

#if __name__ == "__main__":
#    uvicorn.run("main:app", port=8000, reload=True)