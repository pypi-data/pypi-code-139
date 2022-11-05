from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.dialects.mysql import TINYINT

from borsodi_database_model.tables.base import Base


class Report(Base):
    __tablename__ = 'report'

    licence_plate = Column(String(12), nullable=False)
    entry_point_camera_id = Column(TINYINT(4), nullable=False, default=1)
    arrived_to_entry_point = Column(DateTime, nullable=False)
    leaved_entry_point = Column(DateTime, nullable=False)
    entry_time_in_minutes = Column(TINYINT(4), nullable=False)
    start_loading_point_camera_id = Column(TINYINT(4), nullable=False, default=2)
    arrived_to_start_loading_point = Column(DateTime, nullable=False)
    leaved_start_loading_point = Column(DateTime, nullable=False)
    start_loading_time_in_minutes = Column(TINYINT(4), nullable=False)
    finish_loading_point_camera_id = Column(TINYINT(4), nullable=False, default=3)
    arrived_to_finish_loading_point = Column(DateTime, nullable=False)
    leaved_finish_loading_point = Column(DateTime, nullable=False)
    finish_loading_time_in_minutes = Column(TINYINT(4), nullable=False)
    loading_time_in_minutes = Column(SMALLINT(6), nullable=False)
