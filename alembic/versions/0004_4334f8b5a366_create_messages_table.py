"""create messages table

Revision ID: 4334f8b5a366
Revises: 8fd5e8ae6c99
Create Date: 2024-01-31 19:27:42.702287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4334f8b5a366'
down_revision: Union[str, None] = '8fd5e8ae6c99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'messages',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('conversation_id', sa.BigInteger(), sa.ForeignKey('conversations.id'), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_messages_conversation_id', 'conversation_id'),
        sa.ForeignKeyConstraint(
            ['conversation_id'],
            ['conversations.id'],
            name='fk_conversation_id',
            onupdate='NO ACTION',
            ondelete='CASCADE',
        ),
    )


def downgrade() -> None:
    op.drop_table('messages')
