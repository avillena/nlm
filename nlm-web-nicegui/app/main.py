"""Main NiceGUI application."""
from nicegui import ui, app
from app.config import settings
from app.state import app_state
from app.components.notebook_card import notebook_card


# Configure dark mode
ui.dark_mode().enable() if settings.dark_mode else ui.dark_mode().disable()


@ui.page("/")
async def index():
    """Home page - Notebooks list."""

    # Header
    with ui.header().classes("items-center justify-between"):
        with ui.row().classes("items-center gap-4"):
            ui.label("📚 NLM").classes("text-2xl font-bold")
            ui.label("NotebookLM Web Interface").classes("text-lg")

        with ui.row().classes("items-center gap-2"):
            # Dark mode toggle
            ui.switch("Dark Mode", value=settings.dark_mode, on_change=lambda e: ui.dark_mode().toggle())

            # Connection status
            with ui.row().classes("items-center gap-2"):
                ui.icon("circle", size="xs").classes("text-green-500")
                ui.label("Connected").classes("text-sm")

    # Main content
    with ui.column().classes("w-full max-w-7xl mx-auto p-6 gap-6"):
        # Page header
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column():
                ui.label("Notebooks").classes("text-3xl font-bold")
                ui.label("Manage your NotebookLM notebooks").classes("text-gray-600")

            ui.button(
                "New Notebook",
                on_click=lambda: create_notebook_dialog(),
                icon="add",
            ).props("color=primary")

        # Error display
        error_label = ui.label().classes("text-red-500")
        error_label.visible = False

        # Loading indicator
        spinner = ui.spinner(size="lg")
        spinner.visible = False

        # Notebooks grid
        notebooks_container = ui.grid(columns=3).classes("w-full gap-4")

        async def load_notebooks():
            """Load and display notebooks."""
            spinner.visible = True
            error_label.visible = False
            notebooks_container.clear()

            success = await app_state.load_notebooks()

            spinner.visible = False

            if not success:
                error_label.text = app_state.error or "Failed to load notebooks"
                error_label.visible = True
                return

            if not app_state.notebooks:
                with notebooks_container:
                    with ui.column().classes("col-span-3 text-center py-12"):
                        ui.icon("description", size="xl").classes("text-gray-400")
                        ui.label("No notebooks").classes("text-lg font-medium mt-2")
                        ui.label("Get started by creating a new notebook").classes(
                            "text-gray-500"
                        )
                return

            with notebooks_container:
                for notebook in app_state.notebooks:
                    notebook_card(
                        notebook=notebook,
                        on_view=lambda nb_id: view_notebook(nb_id),
                        on_delete=lambda nb_id: delete_notebook_confirm(nb_id),
                    )

        async def view_notebook(notebook_id: str):
            """Navigate to notebook detail page."""
            ui.navigate.to(f"/notebooks/{notebook_id}")

        async def delete_notebook_confirm(notebook_id: str):
            """Show delete confirmation dialog."""
            with ui.dialog() as dialog, ui.card():
                ui.label("Delete Notebook?").classes("text-lg font-semibold")
                ui.label("This action cannot be undone.").classes("text-gray-600 mt-2")

                with ui.row().classes("gap-2 mt-4 justify-end"):
                    ui.button("Cancel", on_click=dialog.close).props("flat")
                    ui.button(
                        "Delete",
                        on_click=lambda: delete_notebook(notebook_id, dialog),
                    ).props("flat color=negative")

            dialog.open()

        async def delete_notebook(notebook_id: str, dialog):
            """Delete notebook."""
            dialog.close()
            spinner.visible = True

            success = await app_state.delete_notebook(notebook_id)

            spinner.visible = False

            if success:
                ui.notify("Notebook deleted successfully", type="positive")
                await load_notebooks()
            else:
                ui.notify(
                    app_state.error or "Failed to delete notebook", type="negative"
                )

        def create_notebook_dialog():
            """Show create notebook dialog."""
            with ui.dialog() as dialog, ui.card():
                ui.label("Create New Notebook").classes("text-lg font-semibold")

                title_input = ui.input("Title", placeholder="My Research Notebook").classes(
                    "w-full"
                ).props("outlined")

                emoji_input = ui.input("Emoji (optional)", placeholder="📚").classes(
                    "w-full"
                ).props("outlined")

                with ui.row().classes("gap-2 mt-4 justify-end"):
                    ui.button("Cancel", on_click=dialog.close).props("flat")
                    ui.button(
                        "Create",
                        on_click=lambda: create_notebook(
                            title_input.value, emoji_input.value, dialog
                        ),
                    ).props("color=primary")

            dialog.open()

        async def create_notebook(title: str, emoji: str, dialog):
            """Create new notebook."""
            if not title:
                ui.notify("Title is required", type="warning")
                return

            dialog.close()
            spinner.visible = True

            success = await app_state.create_notebook(
                title=title, emoji=emoji if emoji else None
            )

            spinner.visible = False

            if success:
                ui.notify("Notebook created successfully", type="positive")
                await load_notebooks()
            else:
                ui.notify(
                    app_state.error or "Failed to create notebook", type="negative"
                )

        # Initial load
        await load_notebooks()


@ui.page("/notebooks/{notebook_id}")
async def notebook_detail(notebook_id: str):
    """Notebook detail page."""

    # Header
    with ui.header().classes("items-center justify-between"):
        with ui.row().classes("items-center gap-4"):
            ui.button(icon="arrow_back", on_click=lambda: ui.navigate.to("/")).props(
                "flat"
            )
            ui.label("📚 NLM").classes("text-2xl font-bold")

    # Main content
    with ui.column().classes("w-full max-w-7xl mx-auto p-6 gap-6"):
        ui.label(f"Notebook: {notebook_id}").classes("text-3xl font-bold")

        # Tabs for different sections
        with ui.tabs().classes("w-full") as tabs:
            sources_tab = ui.tab("Sources")
            notes_tab = ui.tab("Notes")
            audio_tab = ui.tab("Audio")
            generation_tab = ui.tab("Generation")

        with ui.tab_panels(tabs, value=sources_tab).classes("w-full"):
            # Sources panel
            with ui.tab_panel(sources_tab):
                with ui.column().classes("gap-4"):
                    ui.label("Sources").classes("text-2xl font-semibold")

                    # Add source button
                    with ui.row().classes("gap-2"):
                        ui.button("Add URL", icon="link").props("color=primary")
                        ui.button("Upload File", icon="upload_file").props(
                            "color=primary"
                        )
                        ui.button("Add Text", icon="text_fields").props(
                            "color=primary"
                        )

                    # Sources list
                    sources_container = ui.column().classes("w-full gap-2")

                    async def load_sources():
                        """Load sources for this notebook."""
                        sources_container.clear()

                        success = await app_state.load_sources(notebook_id)

                        if not success:
                            with sources_container:
                                ui.label(
                                    app_state.error or "Failed to load sources"
                                ).classes("text-red-500")
                            return

                        if not app_state.sources:
                            with sources_container:
                                ui.label("No sources yet").classes("text-gray-500")
                            return

                        with sources_container:
                            for source in app_state.sources:
                                with ui.card().classes("w-full"):
                                    ui.label(source["title"]).classes("font-semibold")
                                    ui.label(
                                        f"Type: {source['metadata'].get('source_type', 'Unknown')}"
                                    ).classes("text-sm text-gray-500")

                    await load_sources()

            # Notes panel
            with ui.tab_panel(notes_tab):
                ui.label("Notes").classes("text-2xl font-semibold")
                ui.label("Notes management coming soon...").classes("text-gray-500")

            # Audio panel
            with ui.tab_panel(audio_tab):
                ui.label("Audio Overviews").classes("text-2xl font-semibold")
                ui.label("Audio management coming soon...").classes("text-gray-500")

            # Generation panel
            with ui.tab_panel(generation_tab):
                ui.label("Content Generation").classes("text-2xl font-semibold")
                ui.label("Content generation coming soon...").classes("text-gray-500")


def main():
    """Run the application."""
    ui.run(
        title=settings.title,
        host=settings.host,
        port=settings.port,
        reload=False,  # Disable reload for production
        show=False,  # Don't auto-open browser
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
