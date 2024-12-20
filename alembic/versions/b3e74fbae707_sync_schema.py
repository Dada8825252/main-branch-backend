"""Sync schema

Revision ID: b3e74fbae707
Revises: 845857bdccfa
Create Date: 2024-11-23 20:42:44.788916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3e74fbae707'
down_revision: Union[str, None] = '845857bdccfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_authentications', sa.Column('login_fail_time', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_authentications', 'login_fail_time')
    # ### end Alembic commands ###
