"""add foregin key to posts table

Revision ID: 0eb1168e2d4f
Revises: 7ff3bf43d060
Create Date: 2026-10-06 22:06:47.205180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eb1168e2d4f'
down_revision: Union[str, Sequence[str], None] = '7ff3bf43d060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users",
                          local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fk",table_name = "posts")
    op.drop_column("posts","user_id")
    pass
