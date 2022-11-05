from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from borsodi_database_model.tables.base import Base


class TruckTrackingLog(Base):
    __tablename__ = 'truck_tracking_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_id = Column(String(50), nullable=False)
    ts = Column(DateTime, nullable=False)
    camera_id = Column(Integer, nullable=False)
    licence_plate = Column(String(15), nullable=True, default=None)
    arrived = Column(DateTime, nullable=False)
    waiting = Column(DateTime, nullable=False)
    finished = Column(DateTime, nullable=False)
    status = Column(String(10), nullable=False)
