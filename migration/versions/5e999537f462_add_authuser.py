"""add authuser

Revision ID: 5e999537f462
Revises: 31cc780be7bb
Create Date: 2024-09-09 13:09:16.422285

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e999537f462"
down_revision: Union[str, None] = "31cc780be7bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "authusers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("password", sa.String()),
        sa.Column("is_verified", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.drop_index("ix_addresses_new_user_id", table_name="addresses_new")
    op.drop_table("addresses_new")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "addresses_new",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("postcode", sa.VARCHAR(length=80), nullable=True),
        sa.Column("city", sa.VARCHAR(length=80), nullable=True),
        sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("created_at", sa.DATETIME(), nullable=True),
        sa.Column("updated_at", sa.DATETIME(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_addresses_new_user_id", "addresses_new", ["user_id"], unique=False
    )
    op.drop_table("authusers")
    # ### end Alembic commands ###
