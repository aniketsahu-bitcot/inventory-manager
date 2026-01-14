"""ensure product.type nullable

Revision ID: ab9a43bdf4c6
Revises: f9f07f4eb3e7
Create Date: 2026-01-14 12:10:30.426292

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ab9a43bdf4c6'
down_revision: Union[str, Sequence[str], None] = 'f9f07f4eb3e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema: make 'type' column nullable."""
    op.alter_column(
        'products',                # table name
        'type',                    # column name
        existing_type=sa.String(), # current column type
        nullable=True              # make it nullable
    )

def downgrade() -> None:
    """Downgrade schema: revert 'type' column to NOT NULL."""
    op.alter_column(
        'products',
        'type',
        existing_type=sa.String(),
        nullable=False
    )

