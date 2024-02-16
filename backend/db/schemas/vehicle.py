from pydantic import BaseModel, ConfigDict
from datetime import date

class Vehicle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = None
    license_plate: str
    manufacture_year: int
    active: bool = False

class VehicleUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    license_plate: str = None
    manufacture_year: int = None
    active: bool = False