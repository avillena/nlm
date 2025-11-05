"""Tests for NLM CLI wrapper client."""
import pytest
from unittest.mock import Mock, patch, MagicMock
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
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='[{"project_id": "nb1", "title": "Notebook 1"}]',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        notebooks = client.list_notebooks()

        # Assert
        assert len(notebooks) == 1
        assert notebooks[0]["project_id"] == "nb1"
        assert notebooks[0]["title"] == "Notebook 1"
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_list_notebooks_empty(self, mock_run):
        """Test listing notebooks when none exist."""
        # Arrange
        mock_run.return_value = Mock(returncode=0, stdout="[]", stderr="")
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        notebooks = client.list_notebooks()

        # Assert
        assert notebooks == []

    @patch("subprocess.run")
    def test_list_notebooks_cli_error(self, mock_run):
        """Test handling CLI errors."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=1, stdout="", stderr="Authentication failed"
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act & Assert
        with pytest.raises(NLMError, match="Authentication failed"):
            client.list_notebooks()


class TestCreateNotebook:
    """Test creating notebooks."""

    @patch("subprocess.run")
    def test_create_notebook_success(self, mock_run):
        """Test successful notebook creation."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='Created notebook: notebook/nb123\n{"project_id": "nb123", "title": "New Notebook"}',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        notebook = client.create_notebook(title="New Notebook", emoji="📚")

        # Assert
        assert notebook["project_id"] == "nb123"
        assert notebook["title"] == "New Notebook"

    @patch("subprocess.run")
    def test_create_notebook_without_emoji(self, mock_run):
        """Test creating notebook without emoji."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"project_id": "nb123", "title": "New Notebook"}',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        notebook = client.create_notebook(title="New Notebook")

        # Assert
        assert notebook["project_id"] == "nb123"


class TestDeleteNotebook:
    """Test deleting notebooks."""

    @patch("subprocess.run")
    def test_delete_notebook_success(self, mock_run):
        """Test successful notebook deletion."""
        # Arrange
        mock_run.return_value = Mock(returncode=0, stdout="Deleted notebook", stderr="")
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        result = client.delete_notebook(notebook_id="nb123")

        # Assert
        assert result is True

    @patch("subprocess.run")
    def test_delete_notebook_not_found(self, mock_run):
        """Test deleting non-existent notebook."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=1, stdout="", stderr="Notebook not found"
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act & Assert
        with pytest.raises(NotebookNotFoundError):
            client.delete_notebook(notebook_id="invalid")


class TestListSources:
    """Test listing sources."""

    @patch("subprocess.run")
    def test_list_sources_success(self, mock_run):
        """Test successful source listing."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='[{"source_id": {"source_id": "src1"}, "title": "Source 1"}]',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        sources = client.list_sources(notebook_id="nb123")

        # Assert
        assert len(sources) == 1
        assert sources[0]["source_id"]["source_id"] == "src1"


class TestAddSource:
    """Test adding sources."""

    @patch("subprocess.run")
    def test_add_source_from_url(self, mock_run):
        """Test adding source from URL."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"source_id": {"source_id": "src123"}, "title": "New Source"}',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        source = client.add_source(
            notebook_id="nb123", source_input="https://example.com"
        )

        # Assert
        assert source["source_id"]["source_id"] == "src123"

    @patch("subprocess.run")
    def test_add_source_from_text(self, mock_run):
        """Test adding source from text."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"source_id": {"source_id": "src123"}, "title": "Text Source"}',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        source = client.add_source(
            notebook_id="nb123", source_input="Some text content", source_type="text"
        )

        # Assert
        assert source["source_id"]["source_id"] == "src123"


class TestGenerateContent:
    """Test content generation."""

    @patch("subprocess.run")
    def test_generate_guide(self, mock_run):
        """Test generating study guide."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0, stdout="# Study Guide\n\nContent here", stderr=""
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        guide = client.generate_guide(notebook_id="nb123")

        # Assert
        assert "# Study Guide" in guide
        assert "Content here" in guide

    @patch("subprocess.run")
    def test_generate_outline(self, mock_run):
        """Test generating outline."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0, stdout="# Outline\n\n1. Topic 1", stderr=""
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        outline = client.generate_outline(notebook_id="nb123")

        # Assert
        assert "# Outline" in outline


class TestAudioOperations:
    """Test audio overview operations."""

    @patch("subprocess.run")
    def test_create_audio(self, mock_run):
        """Test creating audio overview."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"audio_id": "aud123", "status": "processing"}',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        audio = client.create_audio(
            notebook_id="nb123", instructions="Summarize professionally"
        )

        # Assert
        assert audio["audio_id"] == "aud123"
        assert audio["status"] == "processing"

    @patch("subprocess.run")
    def test_get_audio(self, mock_run):
        """Test getting audio overview."""
        # Arrange
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"audio_id": "aud123", "status": "ready", "url": "https://example.com/audio.mp3"}',
            stderr="",
        )
        client = NLMClient(auth_token="token", cookies="cookies")

        # Act
        audio = client.get_audio(notebook_id="nb123")

        # Assert
        assert audio["status"] == "ready"
        assert "url" in audio
