"""add role column to users

Revision ID: d544ac915810
Revises: a1b2c3d4e5f6
Create Date: 2026-01-19 18:43:35.630820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd544ac915810'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Add the new role column with default value
    op.add_column('users', sa.Column('role', sa.String(length=50), 
                                     nullable=False, server_default='staff'))
    
    # Update existing rows with default value (ensures data integrity)
    op.execute("UPDATE users SET role = 'staff' WHERE role IS NULL")

def downgrade():
    # Remove the role column
    op.drop_column('users', 'role')
