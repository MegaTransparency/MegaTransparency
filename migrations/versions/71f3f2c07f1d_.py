"""empty message

Revision ID: 71f3f2c07f1d
Revises: 88ecbc02d652
Create Date: 2017-04-06 18:24:55.348414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71f3f2c07f1d'
down_revision = '88ecbc02d652'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('slug'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apps')
    # ### end Alembic commands ###