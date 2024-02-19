from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session, selectinload

from app import database
from app.dtos.common import NotFoundResponse
from app.middlewares.auth import get_current_user
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.user import User

router = APIRouter(
    prefix='/conversations',
    tags=['Conversation'],
    responses=NotFoundResponse,
)


@router.get('/{conversation_id}')
async def show(
        conversation_id: int,
        db: Session = Depends(database.connection),
        current_user: User = Depends(get_current_user),
):
    conversation = db.query(Conversation).options(
        selectinload(Conversation.messages),
    ).filter(Conversation.id == conversation_id).first()

    if current_user.id != conversation.document.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='cannot access this conversation')

    return conversation


@router.post('/')
async def store(
        doc_id: str,
        db: Session = Depends(database.connection),
        current_user: User = Depends(get_current_user),
):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='document not found')

    if doc.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='cannot access this document')

    conversation = Conversation()
    conversation.document_id = doc.id

    db.add(conversation)
    db.flush()
    db.commit()
    db.refresh(conversation)

    return conversation
