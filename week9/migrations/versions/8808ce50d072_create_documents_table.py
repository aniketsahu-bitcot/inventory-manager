"""create documents table

Revision ID: 8808ce50d072
Revises: d544ac915810
Create Date: 2026-02-02 11:03:59.273905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8808ce50d072'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("content_type", sa.String(100)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table("documents")

