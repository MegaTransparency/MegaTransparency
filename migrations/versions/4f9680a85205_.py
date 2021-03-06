"""empty message

Revision ID: 4f9680a85205
Revises: 33085172486f
Create Date: 2017-03-23 13:38:53.925866

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4f9680a85205'
down_revision = '33085172486f'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('socrata_datasets',
    sa.Column('domain_and_id', sa.String(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('domain_and_id')
    )
    op.add_column(u'sessions', sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text(u'uuid_generate_v4()'), nullable=False))
    op.drop_column(u'sessions', 'uid')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'sessions', sa.Column('uid', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column(u'sessions', 'uuid')
    op.drop_table('socrata_datasets')
    ### end Alembic commands ###
