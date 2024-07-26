import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.open_weather_service import (CITY_IDS, collect_weather_data,
                                               fetch_weather_data,
                                               get_progress, save_weather_data,
                                               weather_data_store)

client = TestClient(app)

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
VALID_CITY_ID = 3439525
INVALID_CITY_ID = -1

SAMPLE_WEATHER_DATA = {
    "id": 123,
    "main": {"temp": 303.15, "humidity": 70},  # 30°C em Kelvin
    "name": "Canoas",
}


@pytest.fixture
def setup_mock_env():
    with patch.dict("os.environ", {"OPEN_WEATHER_API_KEY": API_KEY}):
        yield


@pytest.mark.asyncio
async def test_fetch_weather_data(setup_mock_env):
    with patch("app.services.open_weather_service.httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"list": [SAMPLE_WEATHER_DATA]}
        mock_get.return_value = mock_response

        data = await fetch_weather_data([VALID_CITY_ID])
        assert data["list"][0]["id"] == SAMPLE_WEATHER_DATA["id"]
        assert data["list"][0]["main"]["temp"] == SAMPLE_WEATHER_DATA["main"]["temp"]


@pytest.mark.asyncio
async def test_collect_weather_data(setup_mock_env):
    with patch(
        "app.services.open_weather_service.fetch_weather_data",
        return_value={"list": [SAMPLE_WEATHER_DATA]},
    ):
        user_defined_id = "test_id"
        data = await collect_weather_data(user_defined_id)
        assert data["user_defined_id"] == user_defined_id
        assert len(data["cities"]) > 0
        assert data["cities"][0]["city_id"] == SAMPLE_WEATHER_DATA["id"]


def test_get_progress():
    user_defined_id = "test_id"
    weather_data_store[user_defined_id] = {
        "status": "in_progress",
        "data": {
            "user_defined_id": user_defined_id,
            "datetime": "2021-01-01T00:00:00Z",
            "cities": [{"city_id": 123, "temperature": 30, "humidity": 70}],
        },
    }
    progress = get_progress(user_defined_id)
    assert progress == (1 / len(CITY_IDS)) * 100


def test_get_progress_completed():
    user_defined_id = "test_id_completed"
    weather_data_store[user_defined_id] = {
        "status": "completed",
        "data": {
            "user_defined_id": user_defined_id,
            "datetime": "2021-01-01T00:00:00Z",
            "cities": [{"city_id": 123, "temperature": 30, "humidity": 70}],
        },
    }
    progress = get_progress(user_defined_id)
    assert progress == 100


def test_collect_endpoint():
    with patch(
        "app.services.open_weather_service.collect_weather_data",
        new_callable=MagicMock,
    ) as mock_collect:
        mock_collect.return_value = {
            "user_defined_id": "unique_id_123",
            "datetime": "2021-01-01T00:00:00Z",
            "cities": [{"city_id": 123, "temperature": 30, "humidity": 70}],
        }
        response = client.post(
            "/weather/collect", json={"user_defined_id": "unique_id_123"}
        )
        assert response.status_code == 200
        assert response.json()["id"] == "unique_id_123"


def test_collect_endpoint_existing_id():
    weather_data_store["existing_id"] = {
        "status": "in_progress",
        "data": {
            "user_defined_id": "existing_id",
            "datetime": "2021-01-01T00:00:00Z",
            "cities": [],
        },
    }
    response = client.post("/weather/collect", json={"user_defined_id": "existing_id"})
    assert response.status_code == 400
    assert response.json()["detail"] == "ID already exists"


def test_progress_endpoint_not_found():
    response = client.get("/weather/progress/non_existing_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "ID not found"


def test_save_weather_data():
    with patch("app.db.mongo_client.MongoDB.get_database") as mock_get_database:
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.weather_data = mock_collection
        mock_get_database.return_value = mock_db

        weather_data = {
            "user_defined_id": "unique_id_123",
            "datetime": "2021-01-01T00:00:00Z",
            "cities": [{"city_id": 123, "temperature": 30, "humidity": 70}],
        }
        save_weather_data("unique_id_123", weather_data)
        mock_collection.insert_one.assert_called_once_with(weather_data)
