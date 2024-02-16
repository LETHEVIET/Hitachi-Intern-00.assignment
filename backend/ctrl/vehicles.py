from fastapi import HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import schemas, models
from exceptions import *

async def get_all_vehicles (db_session: AsyncSession):
    vehicles = (await db_session.scalars(select(models.Vehicle).order_by(models.Vehicle.id))).all()
    return vehicles

async def get_a_vehicle (vehicle_id: int, db_session: AsyncSession) -> models.Vehicle:
    vehicle = (await db_session.scalars(select(models.Vehicle).where(models.Vehicle.id == vehicle_id))).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

async def get_vehicle_status (vehicle_id: int, db_session: AsyncSession):
    await print("get_vehicle_status")
    return

async def get_vehicle_histories (vehicle_id: int, data: schemas.SessionQuery, db_session: AsyncSession):
    vehicle = await get_a_vehicle(vehicle_id, db_session)
    print("Snake", data.start_time)
    sessions = (await db_session.scalars(select(models.Session)
                                         .where(models.Session.vehicle_id==vehicle.id)
                                         .where(models.Session.session_start_time>=data.start_time)
                                         .where(models.Session.session_start_time<=data.end_time)
                                         .options(joinedload(models.Session.driver)).order_by(models.Session.id))).fetchall()

    return sessions

async def add_a_vehicle (data: schemas.Vehicle, db_session: AsyncSession):
    new_vehicle = models.Vehicle(**data.model_dump())
    try:
        db_session.add(new_vehicle)
        await db_session.commit()
        await db_session.refresh(new_vehicle)
    except IntegrityError as err:
        await db_session.rollback()
        raise DMException(err)
    return new_vehicle

async def activate_a_vehicle (vehicle_id: int, db_session: AsyncSession):
    await print("activate_a_vehicle")
    return

async def update_a_vehicle (vehicle_id: int, data: schemas.VehicleUpdate, db_session: AsyncSession):
    vehicle = await get_a_vehicle(vehicle_id, db_session)

    try:
        for key, value in data.model_dump().items():
            setattr(vehicle, key, value) if value else None
        await db_session.commit()
        await db_session.refresh(vehicle)
    except Exception as err:
        await db_session.rollback()
        raise DMException(err)
    
    return vehicle

async def deactivate_the_vehicle (vehicle_id: int, db_session: AsyncSession):
    await print("deactivate_the_vehicle")
    return

async def remove_a_vehicle (vehicle_id: int, db_session: AsyncSession):
    vehicle = await get_a_vehicle(vehicle_id, db_session)
    await db_session.delete(vehicle)
    await db_session.commit()
    return JSONResponse(
            status_code = status.HTTP_200_OK, 
            content = {
                "message": "Delete successfully"
                }
        )
