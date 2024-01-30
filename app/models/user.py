from sqlalchemy import Column, BigInteger, DateTime, func, String, CHAR
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    uuid = Column(CHAR(36), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    documents = relationship('Document', back_populates='user')
