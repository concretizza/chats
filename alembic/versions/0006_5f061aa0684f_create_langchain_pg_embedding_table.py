"""create langchain_pg_embedding table

Revision ID: 5f061aa0684f
Revises: a69620f5afa5
Create Date: 2024-02-06 06:57:31.699273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5f061aa0684f'
down_revision: Union[str, None] = 'a69620f5afa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

VECTOR_SIZE = 1536


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    op.create_table(
        'langchain_pg_embedding',
        sa.Column('collection_id', postgresql.UUID(), nullable=True),
        sa.Column('embedding', Vector(VECTOR_SIZE), nullable=True),
        sa.Column('document', sa.String(), nullable=True),
        sa.Column('cmetadata', postgresql.JSON(), nullable=True),
        sa.Column('custom_id', sa.String(), nullable=True),
        sa.Column('uuid', postgresql.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name='langchain_pg_embedding_pkey')
    )

    op.create_foreign_key(
        'langchain_pg_embedding_collection_id_fkey',
        'langchain_pg_embedding',
        'langchain_pg_collection',
        ['collection_id'],
        ['uuid'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint(
        'langchain_pg_embedding_collection_id_fkey',
        'langchain_pg_embedding',
        type_='foreignkey',
    )
    op.drop_table('langchain_pg_embedding')
