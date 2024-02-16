import json
import os
from typing import List

from openai import OpenAI
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.constants.common import MODEL, ROLE_AI, ROLE_USER
from app.models.message import Message


class Chat:
    @staticmethod
    async def store(db: Session, messages: List[Message]):
        await run_in_threadpool(
            Message.store_many, db, messages,
        )

    @staticmethod
    async def conversation(db: Session, conversation_id: int, knowledge: str, question: str):
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
        )

        system_prompt_content = '''
            You're given a context, and have to answer based on it.
            If you don't know the answer, ask another question to be given
            an extra content in order to fully reply the message.
            
            All replies must be in Brazilian Portuguese.
        '''

        system_prompt = {
            'role': 'system',
            'content': system_prompt_content,
        }

        user_prompt_content = f'''
            Here is the context in triple backticks: ```{knowledge}```.
            Answer the question in triple backticks: ```{question}```.
        '''

        user_prompt = {
            'role': ROLE_USER,
            'content': user_prompt_content,
        }

        chunks = client.chat.completions.create(
            messages=[
                system_prompt,
                user_prompt,
            ],
            model=MODEL,
            stream=True,
        )

        message_user = Message()
        message_user.conversation_id = conversation_id
        message_user.role = ROLE_USER
        message_user.content = question

        message_ai = Message()
        message_ai.conversation_id = conversation_id
        message_ai.role = ROLE_AI
        message_ai.content = ''

        for chunk in chunks:
            content = chunk.choices[0].delta.content
            if content is not None:
                message_ai.content += content

            yield json.dumps({
                'state': 'update',
                'data': content,
            })
        yield json.dumps({'state': 'finished', 'data': None})

        await Chat.store(db, [message_user, message_ai])
