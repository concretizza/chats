from sqlalchemy import Column, BigInteger, DateTime, func, CHAR
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models import Base, SessionLocal


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    uuid = Column(CHAR(36), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
    cmetadata = Column(JSONB, nullable=True)

    documents = relationship('Document', back_populates='user')

    def set_metadata(self, account_uuid: str | None):
        cmetadata = {}

        if self.cmetadata is not None:
            cmetadata['account_uuid'] = self.cmetadata.get('account_uuid', None)

        if account_uuid is not None:
            cmetadata['account_uuid'] = account_uuid

        self.cmetadata = cmetadata

    @staticmethod
    def create(user):
        db = SessionLocal()

        user_new = User()
        user_new.uuid = user['uuid']
        user_new.set_metadata(account_uuid=user['account_uuid'])

        db.add(user_new)
        db.flush()
        db.commit()
        db.refresh(user_new)
