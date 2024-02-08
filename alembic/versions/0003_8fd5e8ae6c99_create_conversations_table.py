"""create conversations table

Revision ID: 8fd5e8ae6c99
Revises: be973aa8fdb8
Create Date: 2024-01-31 19:22:53.288643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8fd5e8ae6c99'
down_revision: Union[str, None] = 'be973aa8fdb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'conversations',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('document_id', sa.BigInteger(), sa.ForeignKey('documents.id'), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_conversations_document_id', 'document_id'),
        sa.ForeignKeyConstraint(
            ['document_id'],
            ['documents.id'],
            name='fk_document_id',
            onupdate='NO ACTION',
            ondelete='CASCADE',
        ),
    )


def downgrade() -> None:
    op.drop_table('conversations')
