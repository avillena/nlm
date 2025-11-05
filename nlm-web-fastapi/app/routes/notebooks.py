"""Notebook routes."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import NotebookCreate, NotebookResponse, ErrorResponse
from app.nlm_client import NLMClient, NotebookNotFoundError, NLMError
from app.config import settings

router = APIRouter(prefix="/api/notebooks", tags=["notebooks"])


def get_nlm_client() -> NLMClient:
    """Get NLM client instance."""
    # Demo mode: return mock data if no credentials
    if not settings.nlm_auth_token or not settings.nlm_cookies:
        # Return a mock client for demo purposes
        from unittest.mock import Mock
        mock_client = Mock(spec=NLMClient)
        mock_client.list_notebooks.return_value = [
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
        mock_client.create_notebook.return_value = {
            "project_id": "demo-nb-new",
            "title": "New Demo Notebook",
            "emoji": "📝",
        }
        mock_client.delete_notebook.return_value = True
        mock_client.get_notebook.return_value = {
            "project_id": "demo-nb-1",
            "title": "Demo Research Notebook",
            "emoji": "📚",
            "sources": [],
        }
        return mock_client
    
    return NLMClient(
        auth_token=settings.nlm_auth_token,
        cookies=settings.nlm_cookies,
        nlm_path=settings.nlm_path,
    )


@router.get("", response_model=List[dict])
async def list_notebooks(client: NLMClient = Depends(get_nlm_client)):
    """
    List all notebooks.

    Returns:
        List of notebooks
    """
    try:
        notebooks = client.list_notebooks()
        return notebooks
    except NLMError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to list notebooks", "detail": str(e)},
        )


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_notebook(
    notebook: NotebookCreate,
    client: NLMClient = Depends(get_nlm_client),
):
    """
    Create a new notebook.

    Args:
        notebook: Notebook creation data

    Returns:
        Created notebook data
    """
    try:
        result = client.create_notebook(
            title=notebook.title,
            emoji=notebook.emoji,
        )
        return result
    except NLMError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{notebook_id}", response_model=dict)
async def get_notebook(
    notebook_id: str,
    client: NLMClient = Depends(get_nlm_client),
):
    """
    Get notebook details.

    Args:
        notebook_id: Notebook ID

    Returns:
        Notebook data
    """
    try:
        notebook = client.get_notebook(notebook_id)
        return notebook
    except NotebookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notebook {notebook_id} not found",
        )
    except NLMError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{notebook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notebook(
    notebook_id: str,
    client: NLMClient = Depends(get_nlm_client),
):
    """
    Delete a notebook.

    Args:
        notebook_id: Notebook ID to delete
    """
    try:
        client.delete_notebook(notebook_id)
    except NotebookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Notebook {notebook_id} not found"},
        )
    except NLMError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
