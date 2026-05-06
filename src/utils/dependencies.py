from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel

from src.database import async_session_maker
from src.utils.db_manager import DBManager


class CoordinateParams(BaseModel):
    latitude: Annotated[
        float,
        Query(
            ge=-90,
            le=90,
            description="Широта точки, относительно которой нужно искать города",
            examples=[55.7558],
        ),
    ]
    longitude: Annotated[
        float,
        Query(
            ge=-180,
            le=180,
            description="Долгота точки, относительно которой нужно искать города",
            examples=[37.6173],
        ),
    ]


CoordinateDep = Annotated[CoordinateParams, Depends()]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
