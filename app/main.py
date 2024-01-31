import datetime

from fastapi import FastAPI

from app.models import Base
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation
from app.models.message import Message

from app.controllers import documents
from app.dtos.healthcheck import HealthcheckResponse

version = '0.0.1'

app = FastAPI()
app.include_router(documents.router)


@app.get('/', response_model=HealthcheckResponse, summary='Get Healthcheck', tags=['Healthcheck'])
async def index():
    return HealthcheckResponse(
        version=version,
        datetime=datetime.datetime.utcnow(),
    )
