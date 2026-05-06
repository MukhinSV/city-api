import aiohttp

from src.config import settings


async def get_coordinates(city_name: str) -> tuple | None:
    url = settings.NOMINATIM_URL
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
        "namedetails": 1,
        "featuretype": "city"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
                url,
                params=params,
                headers={"User-Agent": "fastapi-app"}
        ) as resp:
            data = await resp.json()

    if not data:
        return None

    result = data[0]

    real_name = result.get("name", "").lower()

    if real_name != city_name.lower():
        return None

    return float(result["lat"]), float(result["lon"])
