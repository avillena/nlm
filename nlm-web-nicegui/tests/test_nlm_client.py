"""Tests for NLM CLI wrapper client - same as FastAPI version."""
import pytest
from unittest.mock import Mock, patch
from app.nlm_client import NLMClient, NLMError, NotebookNotFoundError


class TestNLMClientInit:
    """Test NLMClient initialization."""

    def test_init_with_credentials(self):
        """Test client initialization with credentials."""
        client = NLMClient(auth_token="token123", cookies="cookie123")
        assert client.auth_token == "token123"
        assert client.cookies == "cookie123"

    def test_init_without_credentials(self):
        """Test client initialization without credentials raises error."""
        with pytest.raises(ValueError, match="auth_token and cookies are required"):
            NLMClient(auth_token="", cookies="")


class TestListNotebooks:
    """Test listing notebooks."""

    @patch("subprocess.run")
    def test_list_notebooks_success(self, mock_run):
        """Test successful notebook listing."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='[{"project_id": "nb1", "title": "Notebook 1"}]',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        notebooks = client.list_notebooks()

        assert len(notebooks) == 1
        assert notebooks[0]["project_id"] == "nb1"

    @patch("subprocess.run")
    def test_list_notebooks_empty(self, mock_run):
        """Test listing notebooks when none exist."""
        mock_run.return_value = Mock(returncode=0, stdout="[]", stderr="")
        client = NLMClient(auth_token="token", cookies="cookies")

        notebooks = client.list_notebooks()

        assert notebooks == []


class TestCreateNotebook:
    """Test creating notebooks."""

    @patch("subprocess.run")
    def test_create_notebook_success(self, mock_run):
        """Test successful notebook creation."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"project_id": "nb123", "title": "New Notebook"}',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        notebook = client.create_notebook(title="New Notebook", emoji="📚")

        assert notebook["project_id"] == "nb123"
        assert notebook["title"] == "New Notebook"


class TestDeleteNotebook:
    """Test deleting notebooks."""

    @patch("subprocess.run")
    def test_delete_notebook_success(self, mock_run):
        """Test successful notebook deletion."""
        mock_run.return_value = Mock(returncode=0, stdout="Deleted", stderr="")
        client = NLMClient(auth_token="token", cookies="cookies")

        result = client.delete_notebook(notebook_id="nb123")

        assert result is True
