from typing import Annotated

from db.database import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

from .drivers import router as drivers_router
from .vehicles import router as vehicles_router
from .sessions import router as sessions_router