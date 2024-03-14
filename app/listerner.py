import json
import os

from redis import Redis

from app.events.events import Events

from app.models import Base
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation
from app.models.message import Message

listeners = {
    'accounts_user.created': User.create,
}


def listener():
    redis_client = Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        db=int(os.getenv('REDIS_DB')),
    )

    pubsub = redis_client.pubsub()
    for event in Events:
        pubsub.subscribe(event.value)

    for message in pubsub.listen():
        if message['type'] == 'message':
            handler = listeners[message['channel'].decode('utf-8')]
            handler(json.loads(message['data'].decode('utf-8')))
