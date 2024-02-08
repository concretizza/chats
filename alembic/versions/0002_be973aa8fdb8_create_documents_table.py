"""create documents table

Revision ID: be973aa8fdb8
Revises: cb10853ff9da
Create Date: 2024-01-31 19:18:56.721637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'be973aa8fdb8'
down_revision: Union[str, None] = 'cb10853ff9da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'documents',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text("timezone('utc', CURRENT_TIMESTAMP)"), nullable=True,
        ),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_documents_user_id', 'user_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_id', onupdate='NO ACTION', ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('documents')
