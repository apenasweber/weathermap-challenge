from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from app.services.open_weather_service import (collect_weather_data,
                                               get_progress,
                                               weather_data_store)

router = APIRouter()
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CollectWeatherRequest(BaseModel):
    user_defined_id: str


@router.post("/collect")
async def post_weather(
    request: CollectWeatherRequest, background_tasks: BackgroundTasks
):
    user_defined_id = request.user_defined_id

    if user_defined_id in weather_data_store:
        raise HTTPException(status_code=400, detail="ID already exists")

    background_tasks.add_task(collect_weather_data, user_defined_id)
    weather_data_store[user_defined_id] = {
        "status": "in_progress",
        "data": {
            "user_defined_id": user_defined_id,
            "datetime": datetime.utcnow().isoformat(),
            "cities": [],
        },
    }
    return {"message": "Weather data collection started", "id": user_defined_id}


@router.get("/progress/{user_defined_id}")
async def get_weather_progress(user_defined_id: str):
    if user_defined_id not in weather_data_store:
        raise HTTPException(status_code=404, detail="ID not found")

    progress = get_progress(user_defined_id)
    return {"id": user_defined_id, "progress": progress}
