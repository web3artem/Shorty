"""empty message

Revision ID: d7cdf8ee4c3e
Revises: 
Create Date: 2024-03-22 23:23:42.179669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7cdf8ee4c3e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_url', sa.String(), nullable=False),
    sa.Column('short_url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_url'),
    sa.UniqueConstraint('short_url')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    # ### end Alembic commands ###
