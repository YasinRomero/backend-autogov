import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def mock_session():
    with patch("app.modules.auth.service.SessionLocal") as mock_class:
        session_instance = MagicMock()
        mock_class.return_value = session_instance
        yield session_instance
