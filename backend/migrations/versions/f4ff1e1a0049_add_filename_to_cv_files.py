"""add filename to cv_files

Revision ID: f4ff1e1a0049
Revises: f15bc69cb753
Create Date: 2026-06-19 18:48:20.369093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4ff1e1a0049'
down_revision: Union[str, Sequence[str], None] = 'f15bc69cb753'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
