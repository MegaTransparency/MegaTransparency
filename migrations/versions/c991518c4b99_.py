"""empty message

Revision ID: c991518c4b99
Revises: 71f3f2c07f1d
Create Date: 2017-04-22 02:36:07.751811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c991518c4b99'
down_revision = '71f3f2c07f1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nicknames',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('group', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_index(op.f('ix_nicknames_group'), 'nicknames', ['group'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_nicknames_group'), table_name='nicknames')
    op.drop_table('nicknames')
    # ### end Alembic commands ###