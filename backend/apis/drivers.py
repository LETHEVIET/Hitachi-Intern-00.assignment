from . import DBSessionDep
from fastapi import APIRouter, Depends
from typing import List

from datetime import datetime

from db import schemas
import ctrl

router = APIRouter(
    prefix="/api/drivers",
    tags=["drivers"],
    responses={404: {"description": "Not found"}},
)

# GET methods

@router.get("/", response_model=List[schemas.Driver])
async def get_all_drivers (db_session: DBSessionDep):
    """
    get list of information of all drivers
    """
    return await ctrl.get_all_drivers(db_session)

@router.get("/{driver_id}", response_model=schemas.Driver)
async def get_a_driver (driver_id: int, db_session: DBSessionDep):
    """
    get information of the driver has "driver_id"
    """
    return await ctrl.get_a_driver(driver_id, db_session)

@router.get("/status/{driver_id}")
async def get_driver_status (driver_id: int, db_session: DBSessionDep):
    """
    get status of the driver has "driver_id" which is working or not
    """
    return await ctrl.get_driver_status(driver_id, db_session)

@router.get("/{driver_id}/histories", response_model=List[schemas.SessionJoinVehicle])
async def get_driver_histories (driver_id: int, data: schemas.SessionQuery, db_session: DBSessionDep):
    """
    get all sessions of the driver has "driver_id" contain associated vehicles information and time
    """
    return await ctrl.get_driver_histories(driver_id, data, db_session)

# POST methods

@router.post("/", response_model=schemas.Driver)
async def add_a_driver (data: schemas.Driver, db_session: DBSessionDep):
    """
    add new a new driver to the table
    """
    new_driver = await ctrl.add_a_driver(data, db_session)
    return new_driver

@router.post("/{driver_id}/activate/{vehicle_id}", response_model=schemas.SessionCreate)
async def driver_activate (driver_id: int, vehicle_id: int, db_session: DBSessionDep, start_time: datetime|None=None):
    """
    activate the vehicle which has "vehicle_id" associate with the driver has "driver_id" 
    """
    return  await ctrl.driver_activate(driver_id, vehicle_id, start_time, db_session)

# PUT methods

@router.put("/{driver_id}", response_model=schemas.Driver)
async def update_a_driver (driver_id: int, data:schemas.DriverUpdate, db_session: DBSessionDep):
    """
    update information of driver has "driver_id"
    """
    return await ctrl.update_a_driver(driver_id, data, db_session)

@router.put("/{driver_id}/deactivate", response_model=schemas.Session)
async def driver_deactivate (driver_id: int, db_session: DBSessionDep, end_time: datetime|None=None):
    """
    deactivate the current vehicle associate with the driver has "driver_id" 
    """
    return await ctrl.driver_deactivate(driver_id, end_time, db_session)

# DELETE methods

@router.delete("/{driver_id}")
async def remove_a_driver (driver_id: int, db_session: DBSessionDep):
    """
    delete information of the driver has "driver_id"
    """
    return  await ctrl.remove_a_driver(driver_id, db_session)