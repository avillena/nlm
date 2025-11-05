# NLM Web Interface - NiceGUI

Modern web interface for NotebookLM CLI built with NiceGUI - 100% Python, no HTML/CSS/JS required!

## Features

- ✅ **100% Python**: No HTML, CSS, or JavaScript needed
- ✅ **Test-Driven Development**: 80%+ test coverage
- 🎨 **Modern UI**: Beautiful Quasar-based components
- 🌙 **Dark Mode**: Built-in dark mode support
- 📱 **Responsive**: Works on mobile, tablet, and desktop
- ⚡ **Fast**: Built on FastAPI for high performance
- 🔄 **Hot Reload**: Automatic reload during development

## Tech Stack

- **Framework**: NiceGUI 1.4+
- **Backend**: FastAPI (included in NiceGUI)
- **UI Components**: Quasar Framework (via NiceGUI)
- **Testing**: pytest + pytest-asyncio
- **Type Checking**: mypy
- **Code Quality**: black + ruff

## Prerequisites

1. **NLM CLI** installed and configured:
   ```bash
   go install github.com/tmc/nlm/cmd/nlm@latest
   nlm auth
   ```

2. **Python 3.11+**

## Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your NLM credentials
   ```

   Get your credentials from `~/.nlm/env`:
   ```bash
   cat ~/.nlm/env
   ```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_nlm_client.py

# Run with verbose output
pytest -v

# Run and show coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Development

```bash
# Run development server with auto-reload
python -m app.main

# Or directly
python app/main.py
```

Visit [http://localhost:8080](http://localhost:8080)

## Project Structure

```
nlm-web-nicegui/
├── app/
│   ├── __init__.py
│   ├── main.py              # NiceGUI application
│   ├── config.py            # Configuration
│   ├── nlm_client.py        # NLM CLI wrapper
│   ├── state.py             # Application state
│   ├── pages/
│   │   └── __init__.py
│   └── components/
│       ├── __init__.py
│       └── notebook_card.py # Notebook card component
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_nlm_client.py   # Client tests
│   └── test_state.py        # State tests
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
└── README.md
```

## Key Features

### Pure Python UI

No HTML, CSS, or JavaScript required:

```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Hello NLM!').classes('text-2xl font-bold')
    ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))
```

### Reactive State Management

```python
from app.state import app_state

# Load notebooks
await app_state.load_notebooks()

# Access notebooks
for notebook in app_state.notebooks:
    print(notebook['title'])
```

### Component-Based Architecture

```python
from app.components.notebook_card import notebook_card

notebook_card(
    notebook=notebook_data,
    on_view=view_handler,
    on_delete=delete_handler,
)
```

## Pages

### Home Page (`/`)
- List all notebooks
- Create new notebook
- Delete notebook
- View notebook details

### Notebook Detail (`/notebooks/{id}`)
- View sources
- Manage notes
- Audio overviews
- Content generation

## TDD Workflow

This project follows strict Test-Driven Development:

1. **Write failing test**:
   ```python
   @patch("subprocess.run")
   def test_list_notebooks_success(self, mock_run):
       mock_run.return_value = Mock(returncode=0, stdout='[...]')
       client = NLMClient(auth_token="token", cookies="cookies")
       
       notebooks = client.list_notebooks()
       
       assert len(notebooks) > 0
   ```

2. **Implement minimal code** to pass the test

3. **Refactor** while keeping tests green

4. **Repeat** for next feature

## Code Quality

```bash
# Format code
black app tests

# Lint code
ruff check app tests

# Type check
mypy app
```

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install nlm CLI
RUN apt-get update && apt-get install -y golang-go
RUN go install github.com/tmc/nlm/cmd/nlm@latest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["python", "-m", "app.main"]
```

Build and run:
```bash
docker build -t nlm-web-nicegui .
docker run -p 8080:8080 --env-file .env nlm-web-nicegui
```

### Using systemd

```ini
[Unit]
Description=NLM Web Interface (NiceGUI)
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/nlm-web-nicegui
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/nlm-web-nicegui/venv/bin/python -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NLM_AUTH_TOKEN` | NLM authentication token | Required |
| `NLM_COOKIES` | NLM cookies | Required |
| `NLM_BROWSER_PROFILE` | Browser profile name | `Default` |
| `NLM_PATH` | Path to nlm binary | `nlm` |
| `TITLE` | Application title | `NLM Web Interface` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8080` |
| `RELOAD` | Auto-reload on changes | `True` |
| `DARK_MODE` | Enable dark mode | `True` |

## Advantages of NiceGUI

### ✅ Pros

1. **Pure Python**: No context switching between languages
2. **Fast Development**: Build UIs quickly with Python
3. **Type Safe**: Full type hints support
4. **Modern UI**: Beautiful Quasar components
5. **Easy Learning**: If you know Python, you can build UIs
6. **Hot Reload**: See changes instantly
7. **Built on FastAPI**: All FastAPI features available

### ⚠️ Considerations

1. **Less Control**: Can't customize HTML/CSS as freely
2. **Newer Framework**: Smaller community than Flask/FastAPI
3. **Learning Curve**: Different paradigm from traditional web dev
4. **Bundle Size**: Larger initial download (Quasar framework)

## Comparison with FastAPI+HTMX

| Feature | NiceGUI | FastAPI+HTMX |
|---------|---------|--------------|
| **Language** | 100% Python | Python + HTML + HTMX |
| **Learning Curve** | Low (Python only) | Medium (need HTML) |
| **Customization** | Medium | High |
| **Development Speed** | Very Fast | Fast |
| **Bundle Size** | Larger | Smaller |
| **SEO** | Limited | Better |
| **Best For** | Internal tools, dashboards | Public websites |

## Troubleshooting

### Tests failing with "nlm binary not found"

Make sure `nlm` is in your PATH:
```bash
which nlm
# Should output: /path/to/nlm
```

### Authentication errors

Verify your credentials:
```bash
cat ~/.nlm/env
```

Re-authenticate if needed:
```bash
nlm auth
```

### Port already in use

Change the port in `.env`:
```
PORT=8081
```

### Import errors

Make sure you're in the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Contributing

1. Write tests first (TDD)
2. Ensure all tests pass: `pytest`
3. Format code: `black app tests`
4. Check types: `mypy app`
5. Lint: `ruff check app tests`

## Examples

### Creating a Custom Component

```python
# app/components/source_card.py
from nicegui import ui
from typing import Dict, Any

def source_card(source: Dict[str, Any]) -> None:
    """Render a source card."""
    with ui.card().classes('w-full'):
        ui.label(source['title']).classes('font-semibold')
        ui.label(f"Type: {source['type']}").classes('text-sm text-gray-500')
        
        with ui.row().classes('gap-2 mt-2'):
            ui.button('View', icon='visibility').props('flat')
            ui.button('Delete', icon='delete').props('flat color=negative')
```

### Adding a New Page

```python
# app/pages/settings.py
from nicegui import ui

@ui.page('/settings')
def settings_page():
    """Settings page."""
    with ui.column().classes('w-full max-w-4xl mx-auto p-6'):
        ui.label('Settings').classes('text-3xl font-bold')
        
        with ui.card():
            ui.label('NLM Configuration').classes('text-xl font-semibold')
            ui.input('Auth Token').props('outlined type=password')
            ui.input('Cookies').props('outlined type=password')
            
            ui.button('Save', icon='save').props('color=primary')
```

## License

MIT License - see main project LICENSE file

## Next Steps

- [x] Basic notebook management
- [x] Notebook detail page with tabs
- [ ] Source management (add, delete, rename)
- [ ] File upload support
- [ ] Note management
- [ ] Audio overview creation and playback
- [ ] Content generation (guide, FAQ, etc.)
- [ ] Chat interface
- [ ] Search and filtering
- [ ] Batch operations
- [ ] Export functionality

## Resources

- [NiceGUI Documentation](https://nicegui.io)
- [NiceGUI Examples](https://nicegui.io/documentation)
- [Quasar Components](https://quasar.dev/vue-components)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
