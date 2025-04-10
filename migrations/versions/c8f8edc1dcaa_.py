"""empty message

Revision ID: c8f8edc1dcaa
Revises: e8093ae822be
Create Date: 2025-03-21 15:25:13.945864

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c8f8edc1dcaa'
down_revision = 'e8093ae822be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agency', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.drop_constraint('invoice_ibfk_2', type_='foreignkey')
        batch_op.drop_column('fk_voyage_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_voyage_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('invoice_ibfk_2', 'voyage', ['fk_voyage_id'], ['id'])

    with op.batch_alter_table('agency', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
