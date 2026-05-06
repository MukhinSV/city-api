from pydantic import BaseModel, ConfigDict, Field


class CityRequestDTO(BaseModel):
    name: str = Field(
        description="Название города на английском языке",
        examples=["Moscow", "Kazan", "Saint Petersburg"],
    )


class CityDTO(BaseModel):
    name: str = Field(description="Название города", examples=["Moscow"])
    latitude: float = Field(description="Широта города", examples=[55.7558])
    longitude: float = Field(description="Долгота города", examples=[37.6173])


class City(BaseModel):
    id: int = Field(description="Идентификатор города", examples=[1])
    name: str = Field(description="Название города", examples=["Moscow"])
    latitude: float = Field(description="Широта города", examples=[55.7558])
    longitude: float = Field(description="Долгота города", examples=[37.6173])

    model_config = ConfigDict(from_attributes=True)
