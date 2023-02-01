"""empty message

Revision ID: f2193090df5c
Revises: 
Create Date: 2023-02-01 19:30:01.776587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2193090df5c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'h_exchanges',
        sa.Column('h_exchange_id', sa.Integer(), nullable=False),
        sa.Column('h_exchange_name', sa.Text(), nullable=False, unique=True),
        sa.Column('h_exchange_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('h_exchange_id')
    )
    op.create_table(
        'h_labels',
        sa.Column('h_label_id', sa.Integer(), nullable=False),
        sa.Column('h_label_name', sa.Text(), nullable=False, unique=True),
        sa.Column('h_label_api_key', sa.Text(), nullable=False),
        sa.Column('h_label_secret_key', sa.Text(), nullable=False),
        sa.Column('h_label_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('h_label_id')
    )
    op.create_table(
        'h_symbols',
        sa.Column('h_symbol_id', sa.Integer(), nullable=False),
        sa.Column('h_symbol_name', sa.Text(), nullable=False, unique=True),
        sa.Column('h_symbol_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('h_symbol_id')
    )
    op.create_table(
        'h_tickers',
        sa.Column('h_ticker_id', sa.Integer(), nullable=False),
        sa.Column('h_ticker_name', sa.Text(), nullable=False, unique=True),
        sa.Column('h_ticker_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('h_ticker_id')
    )
    op.create_table(
        'l_exchanges_symbols',
        sa.Column('l_exchange_symbol_id', sa.Integer(), nullable=False),
        sa.Column('h_exchange_id', sa.Integer(), nullable=False),
        sa.Column('h_symbol_id', sa.Integer(), nullable=False),
        sa.Column('l_exchange_symbol_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['h_exchange_id'], ['h_exchanges.h_exchange_id'], ),
        sa.ForeignKeyConstraint(['h_symbol_id'], ['h_symbols.h_symbol_id'], ),
        sa.PrimaryKeyConstraint('l_exchange_symbol_id')
    )
    op.create_table(
        'l_exchanges_tickers',
        sa.Column('l_exchange_ticker_id', sa.Integer(), nullable=False),
        sa.Column('h_exchange_id', sa.Integer(), nullable=False),
        sa.Column('h_ticker_id', sa.Integer(), nullable=False),
        sa.Column('l_exchange_ticker_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['h_exchange_id'], ['h_exchanges.h_exchange_id'], ),
        sa.ForeignKeyConstraint(['h_ticker_id'], ['h_tickers.h_ticker_id'], ),
        sa.PrimaryKeyConstraint('l_exchange_ticker_id')
    )
    op.create_table(
        'l_exchanges_symbols_labels',
        sa.Column('l_exchange_symbol_label_id', sa.Integer(), nullable=False),
        sa.Column('h_label_id', sa.Integer(), nullable=False),
        sa.Column('l_exchange_symbol_id', sa.Integer(), nullable=False),
        sa.Column('l_exchange_symbol_label_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['h_label_id'], ['h_labels.h_label_id'], ),
        sa.ForeignKeyConstraint(['l_exchange_symbol_id'], ['l_exchanges_symbols.l_exchange_symbol_id'], ),
        sa.PrimaryKeyConstraint('l_exchange_symbol_label_id')
    )
    op.create_table(
        'l_exchanges_tickers_labels',
        sa.Column('l_exchange_ticker_label_id', sa.Integer(), nullable=False),
        sa.Column('h_label_id', sa.Integer(), nullable=False),
        sa.Column('l_exchange_ticker_id', sa.Integer(), nullable=False),
        sa.Column('l_exchange_ticker_label_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['h_label_id'], ['h_labels.h_label_id'], ),
        sa.ForeignKeyConstraint(['l_exchange_ticker_id'], ['l_exchanges_tickers.l_exchange_ticker_id'], ),
        sa.PrimaryKeyConstraint('l_exchange_ticker_label_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('l_exchanges_tickers_labels')
    op.drop_table('l_exchanges_symbols_labels')
    op.drop_table('l_exchanges_tickers')
    op.drop_table('l_exchanges_symbols')
    op.drop_table('h_tickers')
    op.drop_table('h_symbols')
    op.drop_table('h_labels')
    op.drop_table('h_exchanges')
    # ### end Alembic commands ###
