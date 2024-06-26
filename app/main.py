import datetime

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.listerner import listener
from app.models import Base
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation
from app.models.message import Message

from app.controllers import documents, conversations, messages
from app.dtos.healthcheck import HealthcheckResponse

load_dotenv()

version = '0.0.1'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(documents.router)
app.include_router(conversations.router)
app.include_router(messages.router)


@app.on_event('startup')
async def startup_event():
    import threading
    thread = threading.Thread(target=listener, daemon=True)
    thread.start()


@app.get('/', response_model=HealthcheckResponse, summary='Get Healthcheck', tags=['Healthcheck'])
async def index():
    return HealthcheckResponse(
        version=version,
        datetime=datetime.datetime.utcnow(),
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
