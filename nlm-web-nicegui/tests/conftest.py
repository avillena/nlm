"""Test configuration and fixtures."""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_nlm_client():
    """Mock NLM client for testing."""
    client = Mock()
    return client


@pytest.fixture
def sample_notebooks():
    """Sample notebook data."""
    return [
        {
            "project_id": "nb1",
            "title": "Research Notebook",
            "emoji": "📚",
            "sources": [],
        },
        {
            "project_id": "nb2",
            "title": "Study Notes",
            "emoji": "📖",
            "sources": [],
        },
    ]


@pytest.fixture
def sample_sources():
    """Sample source data."""
    return [
        {
            "source_id": {"source_id": "src1"},
            "title": "Article 1",
            "metadata": {"source_type": "SOURCE_TYPE_URL"},
        },
        {
            "source_id": {"source_id": "src2"},
            "title": "Document.pdf",
            "metadata": {"source_type": "SOURCE_TYPE_LOCAL_FILE"},
        },
    ]
