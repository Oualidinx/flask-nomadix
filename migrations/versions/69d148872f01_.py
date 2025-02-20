"""empty message

Revision ID: 69d148872f01
Revises: c32b0467fae2
Create Date: 2024-11-26 19:09:11.514343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69d148872f01'
down_revision = 'c32b0467fae2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bus', schema=None) as batch_op:
        batch_op.add_column(sa.Column('state', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bus', schema=None) as batch_op:
        batch_op.drop_column('state')

    # ### end Alembic commands ###
