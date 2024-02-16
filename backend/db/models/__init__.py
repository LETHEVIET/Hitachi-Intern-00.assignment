from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .driver import Driver
from .vehicle import Vehicle
from .session import Session
