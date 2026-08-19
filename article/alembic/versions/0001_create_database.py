"""create database

Revision ID: 0001
Revises:
Create Date: 2026-08-19

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE DATABASE IF NOT EXISTS article")


def downgrade() -> None:
    op.execute("DROP DATABASE IF EXISTS article")
