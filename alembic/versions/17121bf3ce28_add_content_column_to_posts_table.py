"""add content column to posts table

Revision ID: 17121bf3ce28
Revises: f2b0e7a331fa
Create Date: 2024-04-10 06:24:16.339270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17121bf3ce28'
down_revision: Union[str, None] = 'f2b0e7a331fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
