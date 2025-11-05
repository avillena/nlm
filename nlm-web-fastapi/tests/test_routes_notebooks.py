"""Tests for notebook routes."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


@pytest.fixture
def client():
    """Create test client."""
    from app.main import app

    return TestClient(app)


class TestListNotebooks:
    """Test GET /api/notebooks endpoint."""

    @patch("app.routes.notebooks.get_nlm_client")
    def test_list_notebooks_success(self, mock_get_client, client):
        """Test successful notebook listing."""
        # Arrange
        mock_nlm = Mock()
        mock_nlm.list_notebooks.return_value = [
            {"project_id": "nb1", "title": "Notebook 1", "emoji": "📚"},
            {"project_id": "nb2", "title": "Notebook 2", "emoji": "📖"},
        ]
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.get("/api/notebooks")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["project_id"] == "nb1"
        assert data[1]["project_id"] == "nb2"

    @patch("app.routes.notebooks.get_nlm_client")
    def test_list_notebooks_empty(self, mock_get_client, client):
        """Test listing when no notebooks exist."""
        # Arrange
        mock_nlm = Mock()
        mock_nlm.list_notebooks.return_value = []
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.get("/api/notebooks")

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    @patch("app.routes.notebooks.get_nlm_client")
    def test_list_notebooks_error(self, mock_get_client, client):
        """Test error handling."""
        # Arrange
        mock_nlm = Mock()
        mock_nlm.list_notebooks.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.get("/api/notebooks")

        # Assert
        assert response.status_code == 500
        assert "error" in response.json()


class TestCreateNotebook:
    """Test POST /api/notebooks endpoint."""

    @patch("app.routes.notebooks.get_nlm_client")
    def test_create_notebook_success(self, mock_get_client, client):
        """Test successful notebook creation."""
        # Arrange
        mock_nlm = Mock()
        mock_nlm.create_notebook.return_value = {
            "project_id": "nb123",
            "title": "New Notebook",
            "emoji": "📚",
        }
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.post(
            "/api/notebooks", json={"title": "New Notebook", "emoji": "📚"}
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["project_id"] == "nb123"
        assert data["title"] == "New Notebook"
        mock_nlm.create_notebook.assert_called_once_with(
            title="New Notebook", emoji="📚"
        )

    @patch("app.routes.notebooks.get_nlm_client")
    def test_create_notebook_without_emoji(self, mock_get_client, client):
        """Test creating notebook without emoji."""
        # Arrange
        mock_nlm = Mock()
        mock_nlm.create_notebook.return_value = {
            "project_id": "nb123",
            "title": "New Notebook",
        }
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.post("/api/notebooks", json={"title": "New Notebook"})

        # Assert
        assert response.status_code == 201
        mock_nlm.create_notebook.assert_called_once_with(title="New Notebook", emoji=None)

    def test_create_notebook_invalid_data(self, client):
        """Test validation error."""
        # Act
        response = client.post("/api/notebooks", json={"title": ""})

        # Assert
        assert response.status_code == 422


class TestDeleteNotebook:
    """Test DELETE /api/notebooks/{id} endpoint."""

    @patch("app.routes.notebooks.get_nlm_client")
    def test_delete_notebook_success(self, mock_get_client, client):
        """Test successful notebook deletion."""
        # Arrange
        mock_nlm = Mock()
        mock_nlm.delete_notebook.return_value = True
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.delete("/api/notebooks/nb123")

        # Assert
        assert response.status_code == 204
        mock_nlm.delete_notebook.assert_called_once_with(notebook_id="nb123")

    @patch("app.routes.notebooks.get_nlm_client")
    def test_delete_notebook_not_found(self, mock_get_client, client):
        """Test deleting non-existent notebook."""
        # Arrange
        from app.nlm_client import NotebookNotFoundError

        mock_nlm = Mock()
        mock_nlm.delete_notebook.side_effect = NotebookNotFoundError("Not found")
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.delete("/api/notebooks/invalid")

        # Assert
        assert response.status_code == 404
        assert "error" in response.json()


class TestGetNotebook:
    """Test GET /api/notebooks/{id} endpoint."""

    @patch("app.routes.notebooks.get_nlm_client")
    def test_get_notebook_success(self, mock_get_client, client):
        """Test successful notebook retrieval."""
        # Arrange
        mock_nlm = Mock()
        mock_nlm.get_notebook.return_value = {
            "project_id": "nb123",
            "title": "Test Notebook",
            "emoji": "📚",
        }
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.get("/api/notebooks/nb123")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["project_id"] == "nb123"
        assert data["title"] == "Test Notebook"

    @patch("app.routes.notebooks.get_nlm_client")
    def test_get_notebook_not_found(self, mock_get_client, client):
        """Test getting non-existent notebook."""
        # Arrange
        from app.nlm_client import NotebookNotFoundError

        mock_nlm = Mock()
        mock_nlm.get_notebook.side_effect = NotebookNotFoundError("Not found")
        mock_get_client.return_value = mock_nlm

        # Act
        response = client.get("/api/notebooks/invalid")

        # Assert
        assert response.status_code == 404
