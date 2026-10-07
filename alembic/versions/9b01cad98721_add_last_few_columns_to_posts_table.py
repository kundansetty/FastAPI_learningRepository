"""add last few columns to posts table

Revision ID: 9b01cad98721
Revises: 0eb1168e2d4f
Create Date: 2026-10-07 15:55:26.358766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b01cad98721'
down_revision: Union[str, Sequence[str], None] = '0eb1168e2d4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False, server_default="TRUE"))
    op.add_column("posts",sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
