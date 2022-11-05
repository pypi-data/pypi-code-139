"""add 'timezone' to 'User' table

Revision ID: e82e5e9447de
Revises: 9f8c9c37da44
Create Date: 2018-06-08 16:01:52.684935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e82e5e9447de'
down_revision = '9f8c9c37da44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('timezone', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'timezone')
    # ### end Alembic commands ###
