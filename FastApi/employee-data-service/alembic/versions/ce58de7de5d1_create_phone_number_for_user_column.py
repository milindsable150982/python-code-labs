"""create phone number for user column

Revision ID: ce58de7de5d1
Revises: 
Create Date: 2026-11-16 13:23:13.328590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce58de7de5d1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('PhoneNumber', sa.String(length=15), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'PhoneNumber')
