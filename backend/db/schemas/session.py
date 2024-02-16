from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime
import pytz
from typing import Optional
from .driver import Driver
from .vehicle import Vehicle

from exceptions import Valid_time_period_exception

class Session(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    vehicle_id: int
    session_start_time: datetime = None
    session_end_time: datetime = None

class SessionJoin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    vehicle_id: int
    session_start_time: datetime
    session_end_time: Optional[datetime] = ...
    driver: Driver
    vehicle: Vehicle

class SessionJoinVehicle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    vehicle_id: int
    session_start_time: datetime
    session_end_time: Optional[datetime] = ...
    vehicle: Vehicle

class SessionJoinDriver(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    vehicle_id: int
    session_start_time: datetime
    session_end_time: Optional[datetime] = ...
    driver: Driver

class SessionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int = None
    vehicle_id: int
    session_start_time: datetime

class SessionUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_end_time: datetime = datetime.now(tz=pytz.utc)

class SessionQuery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_time: datetime = None 
    end_time: datetime = None

    @model_validator(mode='after')
    def check_valid_time_period(self) -> 'SessionQuery':
        print("Raiden", self.start_time)
        if self.start_time != None and self.end_time != None:
            if self.start_time > self.end_time:
                raise Valid_time_period_exception
        else:
            if self.start_time == None:
                self.start_time = datetime.min
            if self.end_time == None:
                self.end_time = datetime.max
        return self