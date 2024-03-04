from sqlalchemy import Column, BigInteger, DateTime, func, ForeignKey, Index, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models import Base


class Conversation(Base):
    __tablename__ = 'conversations'

    __table_args__ = (
        ForeignKeyConstraint(
            ['document_id'],
            ['documents.id'],
            name='fk_document_id',
            onupdate='NO ACTION',
            ondelete='CASCADE',
        ),
        Index('ix_conversations_document_id', 'document_id'),
    )

    id = Column(BigInteger, primary_key=True)
    document_id = Column(BigInteger, ForeignKey('documents.id'), nullable=False)
    cmetadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    document = relationship('Document', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation', order_by='Message.id.desc()')

    def set_metadata(self, account_uuid: str | None):
        cmetadata = {}

        if self.cmetadata is not None:
            cmetadata['account_uuid'] = self.cmetadata.get('account_uuid', None)

        if account_uuid is not None:
            cmetadata['account_uuid'] = account_uuid

        self.cmetadata = cmetadata
