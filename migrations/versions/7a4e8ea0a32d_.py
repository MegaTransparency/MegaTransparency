"""empty message

Revision ID: 7a4e8ea0a32d
Revises: 0dfebe40aa24
Create Date: 2017-04-22 02:58:00.284867

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7a4e8ea0a32d'
down_revision = '0dfebe40aa24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('voters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('voters',
    sa.Column('slug', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('voters_at_same_address', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('statevoterid', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('countyvoterid', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('title', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('fname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('namesuffix', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('birthdate', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('gender', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regstnum', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regstfrac', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regstname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regsttype', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regunittype', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regstpredirection', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regstpostdirection', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regunitnum', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regcity', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regstate', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('regzipcode', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('countycode', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('precinctcode', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('precinctpart', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('legislativedistrict', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('congressionaldistrict', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mail1', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mail2', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mail3', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mail4', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mailcity', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mailzip', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mailstate', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('mailcountry', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('registrationdate', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('absenteetype', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lastvoted', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('statuscode', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('dflag', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('slug', name=u'voters_pkey')
    )
    # ### end Alembic commands ###