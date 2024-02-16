from pydantic import BaseModel, ConfigDict, model_validator
from datetime import date
from exceptions import Request_validation_exception

class Driver(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = None
    first_name: str
    last_name: str
    birth_date: date
    driver_licence_number: str
    expiry_date: date
    working: bool = False

    @model_validator(mode='after')
    def check_driver_licence_number(self):
        if len(self.driver_licence_number) != 10:
            raise Request_validation_exception(
                "driver_licence_number",
                "driver_licence_number length must be equal to 10")
        return self

class DriverUpdate(Driver):
    first_name: str = None
    last_name: str = None
    birth_date: date = None
    driver_licence_number: str = None
    expiry_date: date = None
    working: bool = None