"""create users table

Revision ID: cb10853ff9da
Revises: 
Create Date: 2024-01-31 14:18:28.271716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cb10853ff9da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('uuid', sa.CHAR(36), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid'),
        sa.Index('ix_users_uuid', 'uuid', unique=True)
    )


def downgrade() -> None:
    op.drop_table('users')
