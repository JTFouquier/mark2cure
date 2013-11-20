"""NCBO User relationship fix datetime2

Revision ID: 424a6731cb31
Revises: 1749147f5093
Create Date: 2013-11-08 10:47:19.418685

"""

# revision identifiers, used by Alembic.
revision = '424a6731cb31'
down_revision = '1749147f5093'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ncbo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('min_term_size', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ncbo')
    ### end Alembic commands ###