"""create langchain_pg_collection table

Revision ID: a69620f5afa5
Revises: 4334f8b5a366
Create Date: 2024-02-06 06:53:34.447391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a69620f5afa5'
down_revision: Union[str, None] = '4334f8b5a366'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'langchain_pg_collection',
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('cmetadata', postgresql.JSON(), nullable=True),
        sa.Column('uuid', postgresql.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name='langchain_pg_collection_pkey'),
    )


def downgrade() -> None:
    op.drop_table('langchain_pg_collection')
