"""empty message

Revision ID: fedccfe397b7
Revises: 2d3b4058466b
Create Date: 2024-12-05 20:29:54.118832

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fedccfe397b7'
down_revision = '2d3b4058466b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('voyage_agency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_agency_id', sa.Integer(), nullable=True),
    sa.Column('fk_voyage_id', sa.Integer(), nullable=True),
    sa.Column('total_paid', sa.Integer(), nullable=True),
    sa.Column('rest_to_pay', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_agency_id'], ['agency.id'], ),
    sa.ForeignKeyConstraint(['fk_voyage_id'], ['voyage.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('voyage_include')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('voyage_include',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('fk_agency_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('fk_voyage_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('is_totally_paid', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('total_paid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('rest_to_pay', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['fk_agency_id'], ['agency.id'], name='voyage_include_ibfk_1'),
    sa.ForeignKeyConstraint(['fk_voyage_id'], ['voyage.id'], name='voyage_include_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('voyage_agency')
    # ### end Alembic commands ###
