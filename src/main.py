import sys
import uvicorn

from fastapi import FastAPI
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from src.api.city import router as city_router

app = FastAPI()
app.include_router(city_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
