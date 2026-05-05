from pydantic import BaseModel


class CityRequestDTO(BaseModel):
    name: str


class CityDTO(BaseModel):
    name: str
    latitude: float
    longitude: float
