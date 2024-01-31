import datetime

from fastapi import FastAPI

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
