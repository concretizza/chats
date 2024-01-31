from sqlalchemy import Column, BigInteger, DateTime, func, String, ForeignKey, ForeignKeyConstraint, Index
from sqlalchemy.orm import relationship

from app.models import Base


class Document(Base):
    __tablename__ = 'documents'

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name='fk_user_id',
            onupdate='NO ACTION',
            ondelete='CASCADE',
        ),
        Index('ix_documents_user_id', 'user_id'),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    user = relationship('User', back_populates='documents')
    conversations = relationship('Conversation', back_populates='document')
