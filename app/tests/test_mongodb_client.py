from unittest.mock import MagicMock, patch

import pytest

from app.db.mongo_client import MongoDB


@pytest.fixture
def setup_mock_env():
    with patch.dict(
        "os.environ",
        {
            "MONGO_URL": "mongodb://localhost:27017",
            "DB_USER": "user",
            "DB_PASSWORD": "password",
            "MONGO_DB_NAME": "test_db",
        },
    ):
        yield


def test_get_database_not_initialized(setup_mock_env):
    MongoDB._client = None
    with pytest.raises(Exception, match="MongoDB client is not initialized"):
        MongoDB.get_database()


def test_close(setup_mock_env):
    mock_client = MagicMock()
    MongoDB._client = mock_client
    MongoDB.close()
    mock_client.close.assert_called_once()
    assert MongoDB._client is None
