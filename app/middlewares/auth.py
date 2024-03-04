from urllib.parse import unquote

from fastapi import HTTPException, status, Request, Security, Depends
from typing import Optional, Type

from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app import database
from app.models.user import User
from app.services.access_token import AccessToken

api_key_header = APIKeyHeader(
    name='Authorization',
    scheme_name='Bearer Token',
    description='Enter: Bearer <token>',
    auto_error=False,
)


def get_api_key(api_key: str = Security(api_key_header)):
    """
    Annotation for authentication
    """
    return api_key


async def get_current_user(
        request: Request,
        db: Session = Depends(database.connection),
        api_key: str = Depends(get_api_key),
) -> Type[User]:
    token: Optional[str] = request.headers.get('Authorization')
    if token is None:
        token = request.cookies.get('Authorization')
        token = unquote(token)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='no authentication token provided',
        )

    plain_token = token.replace('Bearer ', '') if token.startswith('Bearer ') else token
    access_token = AccessToken().decode(plain_token)

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='authentication token is invalid',
        )

    user = db.query(User).filter(User.uuid == str(access_token['sub'])).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid authentication credentials',
        )

    request.state.user = user
    return user
