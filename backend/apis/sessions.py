from . import DBSessionDep
from fastapi import APIRouter, Depends
from typing import List

from db import schemas
import ctrl

router = APIRouter(
    prefix="/api/sessions",
    tags=["sessions"],
    responses={404: {"description": "Not found"}},
)

# GET methods

@router.get("/", response_model=List[schemas.SessionJoin])
async def get_all_sessions (db_session: DBSessionDep):
    """
    get list of information of all sessions
    """
    return await ctrl.get_all_sessions(db_session)

@router.get("/{session_id}", response_model=schemas.SessionJoin)
async def get_a_session (session_id: int, db_session: DBSessionDep):
    """
    get information of the session has "session_id"
    """
    return await ctrl.get_a_session(session_id, db_session)

# POST methods

@router.post("/", response_model=schemas.SessionCreate)
async def add_a_session (data: schemas.SessionCreate, db_session: DBSessionDep):
    """
    add new a new session to the table
    """
    new_session = await ctrl.add_a_session(data, db_session)
    return new_session

# PUT methods

@router.put("/{session_id}", response_model=schemas.Session)
async def update_a_session (session_id: int, data:schemas.SessionUpdate, db_session: DBSessionDep):
    """
    update information of session has "session_id"
    """
    return await ctrl.update_a_session(session_id, data, db_session)

# DELETE methods

@router.delete("/{session_id}")
async def remove_a_session (session_id: int, db_session: DBSessionDep):
    """
    delete information of the session has "session_id"
    """
    return  await ctrl.remove_a_session(session_id, db_session)