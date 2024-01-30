from sqlalchemy import Column, BigInteger, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(BigInteger, primary_key=True)
    document_id = Column(BigInteger, ForeignKey('documents.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    document = relationship('Document', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation')
