"""Change camera_id enum values

Revision ID: 0c9e968aeb0b
Revises: 5a215d376732
Create Date: 2022-09-09 07:15:44.270143

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '0c9e968aeb0b'
down_revision = '5a215d376732'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('truck_tracking_log', 'camera_id')
    op.add_column('truck_tracking_log', sa.Column('camera_id', sa.Enum('1', '2', '3'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('truck_tracking_log', 'camera_id')
    op.add_column('truck_tracking_log', sa.Column('camera_id', sa.Enum('one', 'two', 'three'), nullable=False))
    # ### end Alembic commands ###
