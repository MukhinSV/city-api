from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from src.models.city import CityORM
from src.schemas.city import City, CityDTO


class CityRepository:
    model = CityORM
    schema = City

    def __init__(self, session):
        self.session = session

    async def get(self, city_name: str) -> City | None:
        query = select(self.model).filter_by(name=city_name)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model)

    async def get_all(self) -> list[City]:
        query = select(self.model)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.schema.model_validate(model) for model in models]

    async def add(self, city: CityDTO) -> City | None:
        add_city_stmt = (insert(self.model)
                         .values(**city.model_dump())
                         .on_conflict_do_nothing(index_elements=["name"])
                         .returning(self.model))
        result = await self.session.execute(add_city_stmt)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model)
