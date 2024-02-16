from . import DBSessionDep
from fastapi import APIRouter, Depends
from typing import List

from db import schemas
import ctrl

router = APIRouter(
    prefix="/api/vehicles",
    tags=["vehicles"],
    responses={404: {"description": "Not found"}},
)

# GET

@router.get("/", response_model=List[schemas.Vehicle])
async def get_all_vehicles (db_session: DBSessionDep):
    """
    get list of information of all vehicles
    """
    return await ctrl.get_all_vehicles(db_session)

@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
async def __ (vehicle_id: int, db_session: DBSessionDep):
    """
    get information of vehicle has "vehicle_id"
    """
    return await ctrl.get_a_vehicle(vehicle_id, db_session)

@router.get("/status/{vehicle_id}")
async def get_vehicle_status (vehicle_id: int, db_session: DBSessionDep):
    """
    get status of vehicle has "vehicle_id" which is activated or not
    """
    return await ctrl.get_vehicle_status(vehicle_id, db_session)

@router.get("/available")
async def get_available_vehicles (db_session: DBSessionDep):
    """
    get all vehicles which are not activated
    """
    return await ctrl.get_available_vehicles(db_session)

@router.get("/{vehicle_id}/histories", response_model=List[schemas.SessionJoinDriver])
async def get_vehicle_histories (vehicle_id: int, data: schemas.SessionQuery, db_session: DBSessionDep):
    """
    get all sessions of the vehicle has ""vehicle_id"" contain associated vehicles information and time
    """
    return await ctrl.get_vehicle_histories(vehicle_id, data, db_session)

# POST

@router.post("/", response_model=schemas.Vehicle)
async def add_a_vehicle (data: schemas.Vehicle, db_session: DBSessionDep):
    """
    add new a new vehicle to the table
    """
    new_vehicle = await ctrl.add_a_vehicle(data, db_session)
    return new_vehicle

# PUT

@router.put("/{vehicle_id}", response_model=schemas.Vehicle)
async def update_a_vehicle (vehicle_id: int, data:schemas.VehicleUpdate, db_session: DBSessionDep):
    """
    update information of vehicle has "vehicle_id"
    """
    return await ctrl.update_a_vehicle(vehicle_id, data, db_session)

# DELETE

@router.delete("/{vehicle_id}")
async def remove_a_vehicle (vehicle_id: int, db_session: DBSessionDep):
    """
    delete information of the vehicle has "vehicle_id"
    """
    return  await ctrl.remove_a_vehicle(vehicle_id, db_session)