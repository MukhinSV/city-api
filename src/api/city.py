from fastapi import APIRouter, HTTPException

from src.schemas.city import CityRequestDTO, CityDTO
from src.utils.coordinates import get_coordinates
from src.utils.dependencies import CoordinateParams, DBDep

router = APIRouter(prefix="/city", tags=["Города"])


@router.get("/{city_name}", summary="Получить информацию о городе по названию")
async def get_city_info_by_name(city_name: str, db: DBDep):
    city = await db.city.get(city_name)
    if not city:
        raise HTTPException(status_code=404, detail="Город не найден")

    return {
        "status": "Город успешно получен",
        "data": city
    }


@router.get("", summary="Получить 2 города ближайших к координате")
async def get_cities_by_coordinate(coordinate: CoordinateParams):
    pass


@router.post("", summary="Добавить новый город")
async def add_city(city_data: CityRequestDTO, db: DBDep):
    coordinates = await get_coordinates(city_name=city_data.name)

    if not coordinates:
        raise HTTPException(
            status_code=404,
            detail="Координаты для этого города не найдены"
        )

    latitude, longitude = coordinates

    city = CityDTO(name=city_data.name, latitude=latitude, longitude=longitude)

    resp = await db.city.add(city)
    if not resp:
        raise HTTPException(
            status_code=409,
            detail="Такой город уже существует"
        )

    await db.commit()

    return {
        "status": "Город успешно добавлен",
        "data": resp
    }
