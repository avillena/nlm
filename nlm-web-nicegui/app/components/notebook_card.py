"""Notebook card component."""
from nicegui import ui
from typing import Dict, Any, Callable


def notebook_card(
    notebook: Dict[str, Any],
    on_view: Callable[[str], None],
    on_delete: Callable[[str], None],
) -> None:
    """
    Render a notebook card.

    Args:
        notebook: Notebook data
        on_view: Callback when view is clicked
        on_delete: Callback when delete is clicked
    """
    with ui.card().classes("w-full hover:shadow-lg transition-shadow"):
        # Header
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(f"{notebook.get('emoji', '📚')} {notebook['title']}").classes(
                "text-lg font-semibold"
            )

        # Metadata
        ui.label(f"ID: {notebook['project_id']}").classes("text-sm text-gray-500")

        # Stats
        source_count = len(notebook.get("sources", []))
        with ui.row().classes("gap-4 mt-2"):
            ui.label(f"📄 {source_count} sources").classes("text-sm text-gray-600")

        # Actions
        with ui.row().classes("gap-2 mt-4"):
            ui.button(
                "View",
                on_click=lambda: on_view(notebook["project_id"]),
            ).props("flat color=primary")

            ui.button(
                "Delete",
                on_click=lambda: on_delete(notebook["project_id"]),
            ).props("flat color=negative")
