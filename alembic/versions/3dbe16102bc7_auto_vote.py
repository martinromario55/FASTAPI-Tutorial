"""auto-vote

Revision ID: 3dbe16102bc7
Revises: c13746524123
Create Date: 2024-04-10 06:51:08.843277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dbe16102bc7'
down_revision: Union[str, None] = 'c13746524123'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.alter_column('posts', 'content',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('posts', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('posts', 'content',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('votes')
    # ### end Alembic commands ###