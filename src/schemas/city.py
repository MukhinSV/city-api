from pydantic import BaseModel, ConfigDict


class CityRequestDTO(BaseModel):
    name: str


class CityDTO(BaseModel):
    name: str
    latitude: float
    longitude: float


class City(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)
