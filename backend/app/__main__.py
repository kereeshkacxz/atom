import os
import sys
from logging import getLogger

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn import run


sys.path.append(os.path.join(os.getcwd(), os.pardir, os.pardir))

from app.config import DefaultSettings
from app.config.utils import getSettings
from app.endpoints import listOfRoutes
from app.models import AuthSchema
from app.schedulers import listOfSchedulers


logger = getLogger(__name__)


def bindRoutes(application: FastAPI, setting: DefaultSettings) -> None:
    for route in listOfRoutes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def bindSchedulers(scheduler) -> None:
    for task in listOfSchedulers:
        scheduler.add_job(task, "interval", hours=0.5)


def getApp() -> FastAPI:
    description = "Сервис обработки требований компании Atom"

    tags_metadata = [
        {
            "name": "Health check",
        },
        {
            "name": "User",
            "description": "Регистрация и авторизация для дальнейших действий.",
        },
    ]

    application = FastAPI(
        title="Atom",
        docs_url="/swagger",
        openapi_url="/openapi",
        description=description,
        version="1.0.0",
        openapi_tags=tags_metadata,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    settings = getSettings()
    bindRoutes(application, settings)
    application.state.settings = settings

    return application


app = getApp()

app.mount("/static", StaticFiles(directory="static"), name="static")

scheduler = BackgroundScheduler()
bindSchedulers(scheduler)
scheduler.start()


@app.on_event("startup")
async def startup_event():
    for task in listOfSchedulers:
        await task()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


if __name__ == "__main__":  # pragma: no cover
    settings_for_application = getSettings()
    run(
        "__main__:app",
        port=settings_for_application.BACKEND_PORT,
        reload=True,
        reload_dirs=["app", "tests"],
        log_level="debug",
        host=settings_for_application.BACKEND_HOST,
    )
