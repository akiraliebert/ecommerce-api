"""fix created_at to be timezone aware in orders table

Revision ID: 447a2dce578d
Revises: 5911215d185e
Create Date: 2025-12-18 10:18:13.187034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '447a2dce578d'
down_revision: Union[str, Sequence[str], None] = '5911215d185e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'orders',
        'created_at',
        existing_type=sa.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False
    )

def downgrade():
    op.alter_column(
        'orders',
        'created_at',
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.TIMESTAMP(),
        existing_nullable=False
    )
