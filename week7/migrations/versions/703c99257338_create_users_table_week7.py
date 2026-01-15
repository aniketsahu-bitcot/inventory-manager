"""
Revision ID: 703c99257338
Revises: 
Create Date: 2026-01-15
"""

from alembic import op
import sqlalchemy as sa


revision = '703c99257338'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Create users table + indexes (products table untouched)."""
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), default='staff', nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

def downgrade() -> None:
    """Rollback - remove users table only."""
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
