from fastapi import HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from db import schemas, models
from exceptions import *
from .drivers import get_a_driver
from .vehicles import get_a_vehicle

async def get_all_sessions (db_session: AsyncSession):
    sessions = (await db_session.scalars(select(models.Session).options(joinedload(models.Session.driver), joinedload(models.Session.vehicle)).order_by(models.Session.id))).fetchall()

    return sessions

async def get_a_session (session_id: int, db_session: AsyncSession) -> models.Session:
    session = (await db_session.scalars(select(models.Session)
                                        .where(models.Session.id == session_id)
                                        .options(joinedload(models.Session.driver), joinedload(models.Session.vehicle)))
              ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

async def add_a_session (data: schemas.SessionCreate, db_session: AsyncSession):
    driver = await get_a_driver(data.driver_id, db_session)
    vehicle = await get_a_vehicle(data.vehicle_id, db_session)

    if driver.working == True or vehicle.active == True:
        raise StatusException

    new_session = models.Session(driver=driver, vehicle=vehicle, **data.model_dump())
    
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

async def update_a_session (session_id: int, data: schemas.SessionUpdate, db_session: AsyncSession):
    session = await get_a_session(session_id, db_session)

    try:
        for key, value in data.model_dump().items():
            setattr(session, key, value) if value else None
        await db_session.commit()
        await db_session.refresh(session)

    except Exception as err:
        await db_session.rollback()
        raise DMException(err)
    
    return session

async def remove_a_session (session_id: int, db_session: AsyncSession):
    session = await get_a_session(session_id, db_session)

    await db_session.delete(session)
    await db_session.commit()

    return JSONResponse(
            status_code = status.HTTP_200_OK, 
            content = {
                "message": "Delete successfully"
                }
        )