from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class CoordinateParams(BaseModel):
    latitude: Annotated[float, Query()]
    longitude: Annotated[float, Query()]


CoordinateDep = Annotated[CoordinateParams, Depends()]
