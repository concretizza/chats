from sqlalchemy import Column, BigInteger, DateTime, func, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.models import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(BigInteger, primary_key=True)
    conversation_id = Column(BigInteger, ForeignKey('conversations.id'), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    conversation = relationship('Conversation', back_populates='messages')
