"""empty message

Revision ID: a01774ed3407
Revises: 13847857c112
Create Date: 2024-10-13 17:44:21.915424

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a01774ed3407'
down_revision = '13847857c112'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hasChanged', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('username', sa.String(length=100), nullable=False))
    op.drop_column('user', 'birthday')
    op.drop_column('user', 'is_verified')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', mysql.VARCHAR(length=100), nullable=False))
    op.add_column('user', sa.Column('is_verified', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('birthday', sa.DATE(), nullable=True))
    op.drop_column('user', 'username')
    op.drop_column('user', 'password_hasChanged')
    # ### end Alembic commands ###
