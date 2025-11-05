"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


@pytest.fixture
def mock_nlm_client():
    """Mock NLM client for testing."""
    with patch("app.nlm_client.NLMClient") as mock:
        client = Mock()
        mock.return_value = client
        yield client


@pytest.fixture
def test_client():
    """Create test client."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def sample_notebook():
    """Sample notebook data."""
    return {
        "project_id": "notebook123",
        "title": "Test Notebook",
        "emoji": "📚",
        "metadata": {
            "create_time": "2025-01-15T10:00:00Z",
            "modified_time": "2025-01-15T10:00:00Z",
        },
        "sources": [],
    }


@pytest.fixture
def sample_source():
    """Sample source data."""
    return {
        "source_id": {"source_id": "source123"},
        "title": "Test Source",
        "metadata": {
            "source_type": "SOURCE_TYPE_URL",
            "last_modified_time": "2025-01-15T10:00:00Z",
        },
    }


@pytest.fixture
def sample_audio():
    """Sample audio overview data."""
    return {
        "audio_id": "audio123",
        "status": "ready",
        "duration": 930,  # 15:30 in seconds
        "url": "https://example.com/audio.mp3",
        "size_bytes": 13107200,  # 12.5 MB
    }
