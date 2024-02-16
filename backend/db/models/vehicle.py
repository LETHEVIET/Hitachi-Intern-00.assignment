from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer
from typing import List
from datetime import date

from . import Base

class Vehicle (Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    license_plate: Mapped[str] = mapped_column(index=True, unique=True)
    manufacture_year: Mapped[int] = mapped_column(index=True)
    active: Mapped[bool] = mapped_column(index=True)    

    sessions: Mapped[List["Session"]] = relationship(back_populates="vehicle")