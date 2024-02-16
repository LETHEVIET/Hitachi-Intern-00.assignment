from fastapi import HTTPException, status
import pytz
from sqlalchemy import select, insert
from sqlalchemy.orm import lazyload, joinedload, dynamic_loader
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from db import schemas, models
from exceptions import *
from .vehicles import get_a_vehicle

async def get_all_drivers (db_session: AsyncSession):
    drivers = (await db_session.scalars(select(models.Driver).order_by(models.Driver.id))).all()
    return drivers

async def get_a_driver (driver_id: int, db_session: AsyncSession) -> models.Driver:
    driver = (await db_session.scalars(select(models.Driver).where(models.Driver.id == driver_id))).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

async def get_driver_status (driver_id: int, db_session: AsyncSession):
    await print("get_driver_status")
    return

async def get_driver_histories (driver_id: int, data: schemas.SessionQuery, db_session: AsyncSession):
    driver = await get_a_driver(driver_id, db_session)
    sessions = (await db_session.scalars(select(models.Session)
                                         .where(models.Session.driver_id==driver.id)
                                         .where(models.Session.session_start_time>=data.start_time)
                                         .where(models.Session.session_start_time<=data.end_time)
                                         .options(joinedload(models.Session.vehicle)).order_by(models.Session.id))).fetchall()

    return sessions

async def add_a_driver (data: schemas.Driver, db_session: AsyncSession):
    new_driver = models.Driver(**data.model_dump())
    try:
        db_session.add(new_driver)
        await db_session.commit()
        await db_session.refresh(new_driver)
    except IntegrityError as err:
        await db_session.rollback()
        raise DMException(err)
    return new_driver

async def driver_activate (driver_id: int, vehicle_id: int, start_time, db_session: AsyncSession):
    driver = await get_a_driver(driver_id, db_session)
    vehicle = await get_a_vehicle(vehicle_id, db_session)

    if driver.working == True or vehicle.active == True:
        raise StatusException

    if start_time == None:
        start_time = datetime.now(tz=pytz.utc)
    
    new_session = models.Session(driver=driver, vehicle=vehicle, session_start_time=start_time)
    
    driver.working = True
    vehicle.active = True

    try:
        db_session.add(new_session)
        await db_session.commit()
        await db_session.refresh(new_session)

    except IntegrityError as err:
        await db_session.rollback()
        raise DMException(err)
    
    return new_session

async def update_a_driver (driver_id: int, data: schemas.DriverUpdate, db_session: AsyncSession):
    driver = await get_a_driver(driver_id, db_session)

    try:
        for key, value in data.model_dump().items():
            setattr(driver, key, value) if value else None
        await db_session.commit()
        await db_session.refresh(driver)
    except Exception as err:
        await db_session.rollback()
        raise DMException(err)
    
    return driver

async def driver_deactivate (driver_id: int, end_time, db_session: AsyncSession):
    driver = await get_a_driver(driver_id, db_session)
    session = (await db_session.scalars(select(models.Session)
                                        .where(models.Session.driver_id == driver_id)
                                        .options(joinedload(models.Session.driver), 
                                                 joinedload(models.Session.vehicle))
                                        .order_by(models.Session.session_start_time))
              ).first()
    
    if end_time == None:
        end_time = datetime.now(tz=pytz.utc)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.session_end_time != None:
        raise HTTPException(status_code=500, detail="The vehicle has been already deactivated")
    if session.session_start_time > end_time:
        raise HTTPException(status_code=500, detail="Session end time must after session start time")
    
    session.session_end_time = end_time
    
    driver.working = False
    if session.vehicle:
        session.vehicle.active = False
    
    await db_session.commit()
    await db_session.refresh(session)
    
    return session

async def remove_a_driver (driver_id: int, db_session: AsyncSession):
    driver = await get_a_driver(driver_id, db_session)
    await db_session.delete(driver)
    await db_session.commit()
    return JSONResponse(
            status_code = status.HTTP_200_OK, 
            content = {
                "message": "Delete successfully"
                }
        )
