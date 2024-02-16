import logging
import sys
import os
from contextlib import asynccontextmanager
from typing import Any, Callable, Dict

from gunicorn.app.base import BaseApplication
import uvicorn
import multiprocessing

from fastapi import FastAPI

from apis import * 
from configs import settings
from db.database import sessionmanager
from exceptions import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.debug_logs else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Exceptions
app.add_exception_handler(DMException, DM_exception_handler)
app.add_exception_handler(StatusException, Status_exception_handler)
app.add_exception_handler(Valid_time_period_exception, Valid_time_period_exception_handler)

# Routers
app.include_router(drivers_router)
app.include_router(vehicles_router)
app.include_router(sessions_router)

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

class StandaloneApplication(BaseApplication):
    def __init__(self, application: Callable, options: Dict[str, Any] = None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    if os.getenv("ENV") == "prod":
        options = {
            "bind": "%s:%s" % ("0.0.0.0", "8000"),
            "workers": number_of_workers(),
            "worker_class": "uvicorn.workers.UvicornWorker",
        }
        StandaloneApplication(app, options).run()
    else:
        uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)