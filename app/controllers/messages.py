import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session

from app import database
from app.constants.common import COLLECTION_NAME
from app.dtos.common import NotFoundResponse
from app.dtos.message import Message as MessageRequest
from app.middlewares.auth import get_current_user
from app.models.conversation import Conversation
from app.models.user import User
from app.services.chat import Chat

router = APIRouter(
    prefix='/messages',
    tags=['Message'],
    responses=NotFoundResponse,
)


@router.post('/')
async def store(
        conversation_id: int,
        req: MessageRequest,
        db: Session = Depends(database.connection),
        current_user: User = Depends(get_current_user),
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='conversation not found')

    if conversation.document.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='cannot access this conversation')

    embeddings = OpenAIEmbeddings()
    vector_db = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=os.getenv('DB_URL'),
        embedding_function=embeddings,
    )

    search_kwargs = {'filter': {'doc_id': conversation.document.id}}
    retriever = vector_db.as_retriever(
        search_kwargs=search_kwargs,
    )

    docs_related = retriever.get_relevant_documents(req.content)
    knowledge = '\n'.join([item.page_content for item in docs_related])

    return StreamingResponse(Chat.conversation(knowledge, req.content), media_type='text/event-stream')
