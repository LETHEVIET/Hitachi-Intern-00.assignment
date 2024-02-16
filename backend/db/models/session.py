from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from datetime import date, datetime

from . import Base

class Session (Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id"), index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), index=True)
    session_start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    session_end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=True)

    driver: Mapped["Driver"] = relationship(back_populates="sessions")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="sessions")

    # driver: Mapped["Driver"] = relationship(foreign_keys=[driver_id])
    # vehicle: Mapped["Vehicle"] = relationship(foreign_keys=[vehicle_id])