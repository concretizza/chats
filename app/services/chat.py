import json
import os

from openai import OpenAI

MODEL = 'gpt-3.5-turbo'


class Chat:
    @staticmethod
    async def conversation(knowledge: str, question: str):
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
        )

        system_prompt_content = f'''
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
            'role': 'user',
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

        for chunk in chunks:
            yield json.dumps({
                'state': 'update',
                'data': chunk.choices[0].delta.content,
            })
        yield json.dumps({'state': 'finished', 'data': None})
