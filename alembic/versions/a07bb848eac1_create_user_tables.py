"""Create user tables

Revision ID: a07bb848eac1
Revises: 4bb23277bc8f
Create Date: 2024-08-13 19:40:15.195966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a07bb848eac1'
down_revision: Union[str, None] = '4bb23277bc8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('user_authentications',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('provider', sa.String(length=100), nullable=False),
    sa.Column('provider_user_id', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_authentications_id'), 'user_authentications', ['id'], unique=False)
    op.create_index(op.f('ix_user_authentications_provider'), 'user_authentications', ['provider'], unique=False)
    op.create_index(op.f('ix_user_authentications_provider_user_id'), 'user_authentications', ['provider_user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_authentications_provider_user_id'), table_name='user_authentications')
    op.drop_index(op.f('ix_user_authentications_provider'), table_name='user_authentications')
    op.drop_index(op.f('ix_user_authentications_id'), table_name='user_authentications')
    op.drop_table('user_authentications')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
