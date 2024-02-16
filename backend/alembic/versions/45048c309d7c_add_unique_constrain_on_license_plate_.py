"""add unique constrain on license_plate of vehicle and driver_licence_number of driver

Revision ID: 45048c309d7c
Revises: 85f2cc115450
Create Date: 2024-02-07 13:32:23.256687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45048c309d7c'
down_revision = '85f2cc115450'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_driver_driver_licence_number', table_name='driver')
    op.create_index(op.f('ix_driver_driver_licence_number'), 'driver', ['driver_licence_number'], unique=True)
    op.drop_index('ix_vehicle_license_plate', table_name='vehicle')
    op.create_index(op.f('ix_vehicle_license_plate'), 'vehicle', ['license_plate'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vehicle_license_plate'), table_name='vehicle')
    op.create_index('ix_vehicle_license_plate', 'vehicle', ['license_plate'], unique=False)
    op.drop_index(op.f('ix_driver_driver_licence_number'), table_name='driver')
    op.create_index('ix_driver_driver_licence_number', 'driver', ['driver_licence_number'], unique=False)
    # ### end Alembic commands ###