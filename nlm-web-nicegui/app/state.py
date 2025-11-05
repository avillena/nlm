"""Application state management."""
from typing import Optional, List, Dict, Any
from app.nlm_client import NLMClient
from app.config import settings


class AppState:
    """Global application state."""

    def __init__(self):
        """Initialize application state."""
        self.client: Optional[NLMClient] = None
        self.notebooks: List[Dict[str, Any]] = []
        self.current_notebook_id: Optional[str] = None
        self.sources: List[Dict[str, Any]] = []
        self.loading: bool = False
        self.error: Optional[str] = None

    def initialize_client(self) -> bool:
        """
        Initialize NLM client with credentials.

        Returns:
            True if successful, False otherwise
        """
        try:
            if not settings.nlm_auth_token or not settings.nlm_cookies:
                # Demo mode: use mock client
                from unittest.mock import Mock
                self.client = Mock(spec=NLMClient)
                self.client.list_notebooks.return_value = [
                    {
                        "project_id": "demo-nb-1",
                        "title": "Demo Research Notebook",
                        "emoji": "📚",
                        "sources": [],
                    },
                    {
                        "project_id": "demo-nb-2",
                        "title": "Demo Study Notes",
                        "emoji": "📖",
                        "sources": [],
                    },
                ]
                self.client.create_notebook.return_value = {
                    "project_id": "demo-nb-new",
                    "title": "New Demo Notebook",
                    "emoji": "📝",
                }
                self.client.delete_notebook.return_value = True
                self.client.list_sources.return_value = []
                return True

            self.client = NLMClient(
                auth_token=settings.nlm_auth_token,
                cookies=settings.nlm_cookies,
                nlm_path=settings.nlm_path,
            )
            return True
        except Exception as e:
            self.error = f"Failed to initialize client: {str(e)}"
            return False

    async def load_notebooks(self) -> bool:
        """
        Load all notebooks.

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            if not self.initialize_client():
                return False

        try:
            self.loading = True
            self.error = None
            self.notebooks = self.client.list_notebooks()
            return True
        except Exception as e:
            self.error = f"Failed to load notebooks: {str(e)}"
            return False
        finally:
            self.loading = False

    async def create_notebook(self, title: str, emoji: Optional[str] = None) -> bool:
        """
        Create a new notebook.

        Args:
            title: Notebook title
            emoji: Optional emoji

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            if not self.initialize_client():
                return False

        try:
            self.loading = True
            self.error = None
            notebook = self.client.create_notebook(title=title, emoji=emoji)
            self.notebooks.insert(0, notebook)
            return True
        except Exception as e:
            self.error = f"Failed to create notebook: {str(e)}"
            return False
        finally:
            self.loading = False

    async def delete_notebook(self, notebook_id: str) -> bool:
        """
        Delete a notebook.

        Args:
            notebook_id: Notebook ID to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            self.loading = True
            self.error = None
            self.client.delete_notebook(notebook_id)
            self.notebooks = [nb for nb in self.notebooks if nb["project_id"] != notebook_id]
            return True
        except Exception as e:
            self.error = f"Failed to delete notebook: {str(e)}"
            return False
        finally:
            self.loading = False

    async def load_sources(self, notebook_id: str) -> bool:
        """
        Load sources for a notebook.

        Args:
            notebook_id: Notebook ID

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            self.loading = True
            self.error = None
            self.current_notebook_id = notebook_id
            self.sources = self.client.list_sources(notebook_id)
            return True
        except Exception as e:
            self.error = f"Failed to load sources: {str(e)}"
            return False
        finally:
            self.loading = False


# Global state instance
app_state = AppState()
