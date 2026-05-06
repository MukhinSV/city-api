import aiohttp
import math

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


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.asin(math.sqrt(a))

    return R * c
