import whisper
from fastapi import FastAPI
from utils import *
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from api import testing, webhook

app = FastAPI()


app.include_router(testing.router)
app.include_router(webhook.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)