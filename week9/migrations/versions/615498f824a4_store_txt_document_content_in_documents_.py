"""store txt document content in documents table

Revision ID: 615498f824a4
Revises: 8808ce50d072
Create Date: 2026-02-04 21:34:35.703690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '615498f824a4'
down_revision: Union[str, Sequence[str], None] = '8808ce50d072'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.add_column(
        "documents",
        sa.Column("content", sa.Text(), nullable=False)
    )
    op.drop_column("documents", "file_path")


def downgrade():
    op.add_column(
        "documents",
        sa.Column("file_path", sa.String(length=500), nullable=False)
    )
    op.drop_column("documents", "content")