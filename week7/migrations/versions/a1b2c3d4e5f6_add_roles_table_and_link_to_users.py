"""Add roles table and link to users

Revision ID: a1b2c3d4e5f6
Revises: 703c99257338
Create Date: 2026-01-19 16:36:09.260544

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'  
down_revision = '703c99257338'
branch_labels = None
depends_on = None

def upgrade() -> None:

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False)
    )

    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=True))

    op.create_foreign_key(
        'fk_users_role',
        source_table='users',
        referent_table='roles',
        local_cols=['role_id'],
        remote_cols=['id']
    )

    op.execute("INSERT INTO roles (name) VALUES ('admin'), ('manager'), ('staff');")

    op.execute("""
        UPDATE users
        SET role_id = (SELECT id FROM roles WHERE name = 'staff')
    """)

    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('role_id', nullable=False)

    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('role')


def downgrade() -> None:

    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(20), nullable=False, server_default='staff'))

    
    op.drop_constraint('fk_users_role', 'users', type_='foreignkey')


    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('role_id')

  
    op.drop_table('roles')
