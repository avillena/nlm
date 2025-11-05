# NLM Web Interface - FastAPI + HTMX

Modern web interface for NotebookLM CLI built with FastAPI, HTMX, and Tailwind CSS.

## Features

- ✅ **Test-Driven Development**: 80%+ test coverage
- 🎨 **Modern UI**: Tailwind CSS with dark mode support
- ⚡ **HTMX**: Dynamic interactions without complex JavaScript
- 🔒 **Type-Safe**: Pydantic models for validation
- 📱 **Responsive**: Works on mobile, tablet, and desktop
- 🚀 **Fast**: Async FastAPI for high performance

## Tech Stack

- **Backend**: FastAPI 0.109+
- **Frontend**: HTMX 1.9+ + Alpine.js 3.x
- **Styling**: Tailwind CSS 3.x
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

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit [http://localhost:8000](http://localhost:8000)

## API Documentation

FastAPI provides automatic API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
nlm-web-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   ├── nlm_client.py        # NLM CLI wrapper
│   ├── routes/
│   │   ├── __init__.py
│   │   └── notebooks.py     # Notebook endpoints
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   └── index.html       # Home page
│   └── static/
│       ├── css/
│       └── js/
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_nlm_client.py   # Client tests
│   └── test_routes_notebooks.py  # Route tests
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .env.example
└── README.md
```

## API Endpoints

### Notebooks

- `GET /api/notebooks` - List all notebooks
- `POST /api/notebooks` - Create notebook
- `GET /api/notebooks/{id}` - Get notebook details
- `DELETE /api/notebooks/{id}` - Delete notebook

### Sources (Coming Soon)

- `GET /api/notebooks/{id}/sources` - List sources
- `POST /api/notebooks/{id}/sources` - Add source
- `DELETE /api/sources/{id}` - Delete source

### Audio (Coming Soon)

- `GET /api/notebooks/{id}/audio` - List audio overviews
- `POST /api/notebooks/{id}/audio` - Create audio
- `GET /api/audio/{id}` - Get audio details

## TDD Workflow

This project follows strict Test-Driven Development:

1. **Write failing test**:
   ```python
   def test_create_notebook_success(self, mock_get_client, client):
       # Arrange
       mock_nlm = Mock()
       mock_nlm.create_notebook.return_value = {"project_id": "nb123"}
       mock_get_client.return_value = mock_nlm
       
       # Act
       response = client.post("/api/notebooks", json={"title": "Test"})
       
       # Assert
       assert response.status_code == 201
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

### Using Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install nlm CLI
RUN apt-get update && apt-get install -y golang-go
RUN go install github.com/tmc/nlm/cmd/nlm@latest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using systemd

```ini
[Unit]
Description=NLM Web Interface
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/nlm-web
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/nlm-web/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
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
| `SECRET_KEY` | App secret key | Change in production |
| `DEBUG` | Debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

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

## License

MIT License - see main project LICENSE file

## Next Steps

- [ ] Add source management routes
- [ ] Add audio/video routes
- [ ] Add content generation routes
- [ ] Add chat interface
- [ ] Add file upload support
- [ ] Add WebSocket for real-time updates
- [ ] Add user authentication
- [ ] Add rate limiting
- [ ] Add caching layer
