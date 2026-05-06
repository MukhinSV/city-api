from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path

from src.schemas.city import CityRequestDTO, CityDTO
from src.utils.coordinates import get_coordinates, haversine
from src.utils.dependencies import DBDep, CoordinateDep

router = APIRouter(prefix="/city", tags=["Города"])


@router.get(
    "/{city_name}",
    summary="Получить информацию о городе по названию",
    description=(
        "Возвращает город из базы данных по точному названию. "
        "В параметре пути нужно передать название города, например `Москва`."
    ),
    responses={
        200: {
            "description": "Город найден",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Город успешно получен",
                        "data": {
                            "id": 1,
                            "name": "Moscow",
                            "latitude": 55.7558,
                            "longitude": 37.6173,
                        },
                    }
                }
            },
        },
        404: {"description": "Город не найден"},
    },
)
async def get_city_info_by_name(
    city_name: Annotated[
        str,
        Path(
            description="Название города, который нужно найти в базе данных",
            examples=["Москва", "Сочи", "Казань"],
        ),
    ],
    db: DBDep,
):
    city = await db.city.get(city_name)
    if not city:
        raise HTTPException(status_code=404, detail="Город не найден")

    return {"status": "Город успешно получен", "data": city}


@router.get(
    "",
    summary="Получить 2 города ближайших к координате",
    description=(
        "Находит два ближайших города из базы данных к переданным координатам. "
        "Нужно указать `latitude` от -90 до 90 и `longitude` от -180 до 180."
    ),
    responses={
        200: {
            "description": "Ближайшие города найдены",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Успешно найдено 2 ближайших города",
                        "cities": [
                            {
                                "id": 1,
                                "name": "Moscow",
                                "latitude": 55.7558,
                                "longitude": 37.6173,
                            },
                            {
                                "id": 2,
                                "name": "Tula",
                                "latitude": 54.193,
                                "longitude": 37.6173,
                            },
                        ],
                    }
                }
            },
        },
        404: {"description": "В базе данных нет городов"},
    },
)
async def get_cities_by_coordinate(coordinate: CoordinateDep, db: DBDep):
    cities = await db.city.get_all()

    if not cities:
        raise HTTPException(status_code=404, detail="В базе данных нет городов")

    if len(cities) <= 2:
        return {"status": f"В базе данных {len(cities)} город(а)", "cities": cities}

    sorted_cities = sorted(
        cities,
        key=lambda city: haversine(
            coordinate.latitude, coordinate.longitude, city.latitude, city.longitude
        ),
    )

    return {"status": "Успешно найдено 2 ближайших города", "cities": sorted_cities[:2]}


@router.post(
    "",
    summary="Добавить новый город",
    description=(
        "Добавляет город в базу данных. Нужно передать название города в поле "
        "`name`; координаты будут найдены автоматически через внешний сервис."
    ),
    responses={
        200: {
            "description": "Город добавлен",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Город успешно добавлен",
                        "data": {
                            "id": 1,
                            "name": "Moscow",
                            "latitude": 55.7558,
                            "longitude": 37.6173,
                        },
                    }
                }
            },
        },
        404: {"description": "Координаты для этого города не найдены"},
        409: {"description": "Такой город уже существует"},
    },
)
async def add_city(
    city_data: Annotated[
        CityRequestDTO,
        Body(
            description="Название города, который нужно добавить",
            openapi_examples={
                "Москва": {"summary": "Москва", "value": {"name": "Москва"}},
                "Казань": {"summary": "Казань", "value": {"name": "Казань"}},
            },
        ),
    ],
    db: DBDep,
):
    coordinates = await get_coordinates(city_name=city_data.name)

    if not coordinates:
        raise HTTPException(
            status_code=404, detail="Координаты для этого города не найдены"
        )

    latitude, longitude = coordinates

    city = CityDTO(name=city_data.name, latitude=latitude, longitude=longitude)

    resp = await db.city.add(city)
    if not resp:
        raise HTTPException(status_code=409, detail="Такой город уже существует")

    await db.commit()

    return {"status": "Город успешно добавлен", "data": resp}
