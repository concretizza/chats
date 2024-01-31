import datetime

from fastapi import FastAPI

from app.dtos.healthcheck_response import HealthcheckResponse

version = '0.0.1'
app = FastAPI()


@app.get('/', response_model=HealthcheckResponse, summary='Get Healthcheck', tags=['Healthcheck'])
async def index():
    return HealthcheckResponse(
        version=version,
        datetime=datetime.datetime.utcnow(),
    )
