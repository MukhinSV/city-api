from src.models.city import CityORM
from src.repositories.base import BaseRepository
from src.schemas.city import CityDTO


class CityRepository(BaseRepository):
    model = CityORM
    schema = CityDTO
