# City API

Небольшое FastAPI-приложение для хранения городов и поиска двух ближайших городов к заданной точке.

## Стек

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- asyncpg
- aiohttp
- Pydantic / pydantic-settings
- Uvicorn
- Docker / Docker Compose

## Что умеет API

- `POST /city` - добавляет город в базу данных.
- `GET /city/{city_name}` - возвращает город по названию.
- `GET /city?latitude=...&longitude=...` - возвращает два ближайших города к переданным координатам.

Координаты при добавлении города API получает из внешнего сервиса Nominatim. В запросе передается только название города, после этого приложение отправляет запрос в Nominatim, берет `lat` и `lon`, сохраняет город в PostgreSQL.

Ближайшие города ищутся среди уже сохраненных городов в базе. Для каждого города считается расстояние от переданной точки по формуле haversine, затем список сортируется по расстоянию и возвращаются первые два города.

## Таблица БД

Используется таблица `city`.

| Поле | Тип | Описание |
| --- | --- | --- |
| `id` | integer | Первичный ключ города |
| `name` | string | Название города, уникальное значение |
| `latitude` | float | Широта города |
| `longitude` | float | Долгота города |

Миграции выполняются через Alembic. При запуске контейнера API команда `alembic upgrade head` применяется автоматически.

## Пример `.env`

```env
DB_NAME=cities
DB_HOST=localhost
DB_PORT=6432
DB_USER=postgres
DB_PASS=postgres

NOMINATIM_URL=https://nominatim.openstreetmap.org/search
```

При запуске через `docker-compose` значение `DB_HOST` для контейнера API переопределяется на `postgres`, поэтому в `.env` можно оставить `localhost` для локального запуска.

## Запуск через Docker

```bash
docker compose up --build
```

API будет доступно на `http://localhost:8000`.

Документация Swagger:

```text
http://localhost:8000/docs
```

## Как протестировать

Добавить город:

```bash
curl -X POST http://localhost:8000/city \
  -H "Content-Type: application/json" \
  -d '{"name": "Москва"}'
```

Получить город по названию:

```bash
curl http://localhost:8000/city/Москва
```

Найти два ближайших города к точке:

```bash
curl "http://localhost:8000/city?latitude=55.7558&longitude=37.6173"
```

Также можно открыть `http://localhost:8000/docs` и выполнить эти запросы через Swagger UI.
