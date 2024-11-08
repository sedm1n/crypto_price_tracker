"""Initial tables

Revision ID: f897efcca0f7
Revises: 
Create Date: 2024-11-02 12:50:41.061654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f897efcca0f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tickers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickers_id'), 'tickers', ['id'], unique=False)
    op.create_index(op.f('ix_tickers_name'), 'tickers', ['name'], unique=True)
    op.create_table('price_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=18, scale=8), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_history_id'), 'price_history', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_price_history_id'), table_name='price_history')
    op.drop_table('price_history')
    op.drop_index(op.f('ix_tickers_name'), table_name='tickers')
    op.drop_index(op.f('ix_tickers_id'), table_name='tickers')
    op.drop_table('tickers')
    # ### end Alembic commands ###
