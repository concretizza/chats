from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session, selectinload

from app import database
from app.dtos.common import NotFoundResponse
from app.dtos.user import UserRequest
from app.middlewares.auth import get_current_user
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.user import User

router = APIRouter(
    prefix='/users',
    tags=['User'],
    responses=NotFoundResponse,
)


@router.post('/')
async def store(
        req: UserRequest,
        db: Session = Depends(database.connection),
):
    user = User()
    user.uuid = req.uuid
    user.set_metadata(account_uuid=req.account_uuid)

    db.add(user)
    db.flush()
    db.commit()
    db.refresh(user)

    return user
