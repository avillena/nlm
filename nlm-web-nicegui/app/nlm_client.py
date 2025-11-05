"""NLM CLI wrapper client for executing nlm commands."""
import json
import subprocess
from typing import Any, Optional
from pathlib import Path


class NLMError(Exception):
    """Base exception for NLM client errors."""

    pass


class NotebookNotFoundError(NLMError):
    """Raised when notebook is not found."""

    pass


class SourceNotFoundError(NLMError):
    """Raised when source is not found."""

    pass


class NLMClient:
    """Client for interacting with NLM CLI."""

    def __init__(self, auth_token: str, cookies: str, nlm_path: str = "nlm"):
        """
        Initialize NLM client.

        Args:
            auth_token: NLM authentication token
            cookies: NLM cookies
            nlm_path: Path to nlm binary (default: "nlm" in PATH)

        Raises:
            ValueError: If auth_token or cookies are empty
        """
        if not auth_token or not cookies:
            raise ValueError("auth_token and cookies are required")

        self.auth_token = auth_token
        self.cookies = cookies
        self.nlm_path = nlm_path

    def _run_command(
        self, args: list[str], input_data: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Run nlm command and return stdout, stderr.

        Args:
            args: Command arguments
            input_data: Optional stdin input

        Returns:
            Tuple of (stdout, stderr)

        Raises:
            NLMError: If command fails
        """
        env = {
            "NLM_AUTH_TOKEN": self.auth_token,
            "NLM_COOKIES": self.cookies,
        }

        try:
            result = subprocess.run(
                [self.nlm_path] + args,
                capture_output=True,
                text=True,
                env=env,
                input=input_data,
                timeout=60,
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip() or result.stdout.strip()
                if "not found" in error_msg.lower():
                    if "notebook" in error_msg.lower():
                        raise NotebookNotFoundError(error_msg)
                    elif "source" in error_msg.lower():
                        raise SourceNotFoundError(error_msg)
                raise NLMError(error_msg)

            return result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            raise NLMError("Command timed out")
        except FileNotFoundError:
            raise NLMError(f"nlm binary not found at: {self.nlm_path}")

    def _parse_json_output(self, output: str) -> Any:
        """
        Parse JSON output from nlm command.

        Args:
            output: Command output

        Returns:
            Parsed JSON data
        """
        # Handle multi-line output where JSON might be on last line
        lines = output.strip().split("\n")
        for line in reversed(lines):
            line = line.strip()
            if line.startswith("{") or line.startswith("["):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue

        # If no JSON found, try parsing entire output
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return output

    # Notebook operations

    def list_notebooks(self) -> list[dict[str, Any]]:
        """
        List all notebooks.

        Returns:
            List of notebook dictionaries
        """
        stdout, _ = self._run_command(["list", "--json"])
        result = self._parse_json_output(stdout)
        return result if isinstance(result, list) else []

    def create_notebook(
        self, title: str, emoji: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Create a new notebook.

        Args:
            title: Notebook title
            emoji: Optional emoji

        Returns:
            Created notebook data
        """
        args = ["create", title]
        if emoji:
            args.extend(["--emoji", emoji])

        stdout, _ = self._run_command(args)
        return self._parse_json_output(stdout)

    def delete_notebook(self, notebook_id: str) -> bool:
        """
        Delete a notebook.

        Args:
            notebook_id: Notebook ID to delete

        Returns:
            True if successful

        Raises:
            NotebookNotFoundError: If notebook not found
        """
        self._run_command(["rm", notebook_id])
        return True

    def get_notebook(self, notebook_id: str) -> dict[str, Any]:
        """
        Get notebook details.

        Args:
            notebook_id: Notebook ID

        Returns:
            Notebook data
        """
        # Note: nlm CLI doesn't have a direct "get" command
        # We'll list all and filter
        notebooks = self.list_notebooks()
        for nb in notebooks:
            if nb.get("project_id") == notebook_id:
                return nb
        raise NotebookNotFoundError(f"Notebook {notebook_id} not found")

    # Source operations

    def list_sources(self, notebook_id: str) -> list[dict[str, Any]]:
        """
        List sources in a notebook.

        Args:
            notebook_id: Notebook ID

        Returns:
            List of source dictionaries
        """
        stdout, _ = self._run_command(["sources", notebook_id, "--json"])
        result = self._parse_json_output(stdout)
        return result if isinstance(result, list) else []

    def add_source(
        self,
        notebook_id: str,
        source_input: str,
        source_type: str = "url",
        mime_type: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Add a source to a notebook.

        Args:
            notebook_id: Notebook ID
            source_input: URL, file path, or text content
            source_type: Type of source ("url", "file", "text")
            mime_type: Optional MIME type

        Returns:
            Created source data
        """
        args = ["add", notebook_id]

        if source_type == "text":
            args.append("-")
            stdout, _ = self._run_command(args, input_data=source_input)
        else:
            args.append(source_input)
            if mime_type:
                args.extend(["--mime", mime_type])
            stdout, _ = self._run_command(args)

        return self._parse_json_output(stdout)

    def delete_source(self, notebook_id: str, source_id: str) -> bool:
        """
        Delete a source.

        Args:
            notebook_id: Notebook ID
            source_id: Source ID

        Returns:
            True if successful
        """
        self._run_command(["rm-source", notebook_id, source_id])
        return True

    def rename_source(self, source_id: str, new_name: str) -> bool:
        """
        Rename a source.

        Args:
            source_id: Source ID
            new_name: New source name

        Returns:
            True if successful
        """
        self._run_command(["rename-source", source_id, new_name])
        return True

    # Content generation

    def generate_guide(self, notebook_id: str) -> str:
        """
        Generate study guide.

        Args:
            notebook_id: Notebook ID

        Returns:
            Generated guide content
        """
        stdout, _ = self._run_command(["generate-guide", notebook_id])
        return stdout

    def generate_outline(self, notebook_id: str) -> str:
        """
        Generate content outline.

        Args:
            notebook_id: Notebook ID

        Returns:
            Generated outline content
        """
        stdout, _ = self._run_command(["generate-outline", notebook_id])
        return stdout

    def generate_faq(self, notebook_id: str) -> str:
        """
        Generate FAQ.

        Args:
            notebook_id: Notebook ID

        Returns:
            Generated FAQ content
        """
        stdout, _ = self._run_command(["faq", notebook_id])
        return stdout

    def generate_glossary(self, notebook_id: str) -> str:
        """
        Generate glossary.

        Args:
            notebook_id: Notebook ID

        Returns:
            Generated glossary content
        """
        stdout, _ = self._run_command(["glossary", notebook_id])
        return stdout

    # Audio operations

    def create_audio(self, notebook_id: str, instructions: str) -> dict[str, Any]:
        """
        Create audio overview.

        Args:
            notebook_id: Notebook ID
            instructions: Generation instructions

        Returns:
            Audio overview data
        """
        stdout, _ = self._run_command(["audio-create", notebook_id, instructions])
        return self._parse_json_output(stdout)

    def get_audio(self, notebook_id: str) -> dict[str, Any]:
        """
        Get audio overview.

        Args:
            notebook_id: Notebook ID

        Returns:
            Audio overview data
        """
        stdout, _ = self._run_command(["audio-get", notebook_id])
        return self._parse_json_output(stdout)

    def list_audio(self, notebook_id: str) -> list[dict[str, Any]]:
        """
        List audio overviews.

        Args:
            notebook_id: Notebook ID

        Returns:
            List of audio overviews
        """
        stdout, _ = self._run_command(["audio-list", notebook_id, "--json"])
        result = self._parse_json_output(stdout)
        return result if isinstance(result, list) else []

    def delete_audio(self, notebook_id: str) -> bool:
        """
        Delete audio overview.

        Args:
            notebook_id: Notebook ID

        Returns:
            True if successful
        """
        self._run_command(["audio-rm", notebook_id])
        return True

    # Note operations

    def list_notes(self, notebook_id: str) -> list[dict[str, Any]]:
        """
        List notes in a notebook.

        Args:
            notebook_id: Notebook ID

        Returns:
            List of note dictionaries
        """
        stdout, _ = self._run_command(["notes", notebook_id, "--json"])
        result = self._parse_json_output(stdout)
        return result if isinstance(result, list) else []

    def create_note(self, notebook_id: str, title: str) -> dict[str, Any]:
        """
        Create a new note.

        Args:
            notebook_id: Notebook ID
            title: Note title

        Returns:
            Created note data
        """
        stdout, _ = self._run_command(["new-note", notebook_id, title])
        return self._parse_json_output(stdout)

    def update_note(
        self, notebook_id: str, note_id: str, content: str, title: str
    ) -> bool:
        """
        Update a note.

        Args:
            notebook_id: Notebook ID
            note_id: Note ID
            content: Note content
            title: Note title

        Returns:
            True if successful
        """
        self._run_command(["update-note", notebook_id, note_id, content, title])
        return True

    def delete_note(self, note_id: str) -> bool:
        """
        Delete a note.

        Args:
            note_id: Note ID

        Returns:
            True if successful
        """
        self._run_command(["rm-note", note_id])
        return True
