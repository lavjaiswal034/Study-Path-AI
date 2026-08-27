"""add user name

Revision ID: adc27e9b34bd
Revises: c6ec71fb5fd3
Create Date: 2026-08-15 00:03:10.041825

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "adc27e9b34bd"
down_revision: Union[str, Sequence[str], None] = "c6ec71fb5fd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Add the column temporarily as nullable
    op.add_column(
        "users",
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=True,
        ),
    )

    # 2. Give existing users a temporary name
    op.execute(
        "UPDATE users SET name = 'Existing User' WHERE name IS NULL"
    )

    # 3. Make the column required
    op.alter_column(
        "users",
        "name",
        existing_type=sa.String(length=100),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "name")