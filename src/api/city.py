from fastapi import APIRouter

from src.schemas.city import CityRequestDTO
from src.utils.dependencies import CoordinateParams

router = APIRouter(prefix="/city", tags=["Города"])


@router.get("/{city_name}", summary="Получить информацию о городе по названию")
async def get_city_info_by_name(city_name: str):
    pass


@router.get("", summary="Получить 2 города ближайших к координате")
async def get_cities_by_coordinate(coordinate: CoordinateParams):
    pass


@router.post("", summary="Добавить новый город")
async def add_city(city_data: CityRequestDTO):
    pass
