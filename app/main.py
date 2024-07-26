from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import weather
from app.db.mongo_client import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoDB.initialize()
    yield
    MongoDB.close()


app = FastAPI(title="Weather Forecast API")
app.include_router(weather.router, prefix="/weather", tags=["weather"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
