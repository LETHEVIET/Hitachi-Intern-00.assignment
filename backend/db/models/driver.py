from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import date

from . import Base

class Driver (Base):
    __tablename__ = "driver"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    birth_date: Mapped[date] = mapped_column(index=True)
    driver_licence_number: Mapped[str] = mapped_column(index=True, unique=True)
    expiry_date: Mapped[date] = mapped_column(index=True)
    working: Mapped[bool] = mapped_column(index=True)

    sessions: Mapped[List["Session"]] = relationship(back_populates="driver")