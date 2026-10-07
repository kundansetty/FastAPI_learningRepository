"""add content column to posts table

Revision ID: 205ba7944179
Revises: f1e47f86b0e8
Create Date: 2026-10-06 21:50:33.135793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '205ba7944179'
down_revision: Union[str, Sequence[str], None] = 'f1e47f86b0e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("content",sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
    pass
