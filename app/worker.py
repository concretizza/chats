import os

import redis
from dotenv import load_dotenv
from rq import Worker

from app.logger import logger
from app.queuer import q

load_dotenv()

redis_conn = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    db=int(os.getenv('REDIS_DB')),
)

try:
    worker = Worker(queues=[q], connection=redis_conn)
    worker.work()
except Exception as e:
    logger.error('redis worker: %s', e, exc_info=True)
    raise
