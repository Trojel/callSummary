from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.settings import DATABASE_URL

engine = create_engine(
    DATABASE_URL, 
    connect_args={}, 
    future=True
    )

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    future=True
    )

def get_db():
    print("DB url: ", DATABASE_URL)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()