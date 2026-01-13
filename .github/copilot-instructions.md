# Copilot Instructions for Python FastAPI Starter

## Project Overview

This is a **FastAPI-based REST API starter template** with Docker, PostgreSQL (PostGIS), Poetry dependency management, and semantic versioning. The project uses the `dsp_toolkit` package for CLI tooling, testing, and formatting.

## Architecture & Key Components

### Application Structure
- **Entry Point**: [src/python_fastapi_starter/cli.py](src/python_fastapi_starter/cli.py) - CLI utilities (server startup, testing, linting, releases)
- **App Factory**: [src/python_fastapi_starter/api/app.py](src/python_fastapi_starter/api/app.py) - FastAPI instance creation with CORS and root_path support
- **Main API**: [src/python_fastapi_starter/api/main.py](src/python_fastapi_starter/api/main.py) - Route definitions and endpoint handlers
- **Tests**: [tests/](tests/) - Pytest test files using FastAPI's `TestClient`
- **Database**: PostGIS-enabled PostgreSQL (port 5434 in compose, 5432 in container)

### Critical Patterns
1. **App Factory Pattern**: Use `create_app()` in [app.py](src/python_fastapi_starter/api/app.py) to configure FastAPI with CORS, title, root_path, and logging.
2. **Environment Loading**: Call `load_environment()` (from `dsp_toolkit`) to load `.env` and `.env.local` files. This runs at module import time in `app.py`.
3. **Dynamic Port Finding**: Server uses `find_free_port()` to avoid port conflicts in dev mode.
4. **Dependency on dsp_toolkit**: CLI commands (`test`, `lint`, `release`) delegate to `dsp_toolkit.cli` - these are NOT implemented locally.

## Developer Workflows

### Getting Started
```bash
# Clone and set up the project
git clone <repo-url>
cd python-fastapi-starter

# Install pyenv (recommended for Python version management)
# macOS: brew install pyenv
# Ubuntu/Debian: https://github.com/pyenv/pyenv#installation

# Install and use Python 3.12+
pyenv install 3.12
pyenv local 3.12

# Install Poetry (if not already installed)
# https://python-poetry.org/docs/#installation

# Create virtual environment and install dependencies
poetry install

# Activate the virtual environment
source .venv/bin/activate
```

### Starting Development
```bash
# Terminal 1: Start PostgreSQL + API with hot-reload
poetry run start --reload

# Terminal 2: Run tests
poetry run test

# Run linting + formatting
poetry run lint

# Run all tests
poetry run test

# Run tests matching a pattern
poetry run test -k "test_name"
```

### With Docker Compose
```bash
# Start both API and PostgreSQL
docker compose up --build -d

# Stop services
docker compose down

# Reset database and API
docker compose down db && docker compose up --build -d db
```

### Testing
- Use `pytest` via `poetry run test`
- Tests import from `python_fastapi_starter.api.main` (the actual app, not a factory)
- Use `TestClient` from FastAPI for endpoint testing
- Example test pattern: See [tests/test_main.py](tests/test_main.py)

### Code Quality
- **Linting & Formatting**: `poetry run lint` (Ruff with E, F, I, W, B, A, C4, SIM, RUF rules; line-length=100)
- **Pre-commit hooks**: Runs `poetry run lint` (ruff check and format) via Lefthook
- **Pre-push hooks**: Runs [scripts/pre_push.sh](scripts/pre_push.sh)
- **Known first-party module**: `python_fastapi_starter` (for import sorting in Ruff)

## Dependencies & Configuration

### Environment Variables
- **`.env`**: Static/build-time variables (safe to commit) — loaded by `python-dotenv` at app startup
- **`.env.local`**: Local secrets and overrides (git-ignored) — auto-loaded for development
- Both files are automatically loaded via `load_environment()` from `dsp_toolkit` in [app.py](src/python_fastapi_starter/api/app.py)

### Virtual Environment
- Poetry automatically creates and manages `.venv` in the project root
- Activate with: `source .venv/bin/activate`
- All `poetry run` commands execute within the virtual environment

### Key Dependencies
- **FastAPI** ^0.116.1 with standard extras (includes Starlette, Pydantic)
- **Uvicorn** ^0.35.0 (ASGI server)
- **Pydantic** ^2.11.7 (data validation)
- **python-dotenv** ^1.1.1 (environment loading)
- **pytest** ^8.4.1 (testing)
- **Ruff** ^0.12.7 (linting/formatting)
- **dsp_toolkit** ^1.0.1 (CLI, testing, logging utilities)

### Configuration Files
- [pyproject.toml](pyproject.toml) - Poetry scripts, dependencies, semantic-release config
- [ruff.toml](ruff.toml) - Line-length=100, rules E/F/I, isort first-party config
- [docker-compose.yml](docker-compose.yml) - API + PostgreSQL services, port 5434 externally
- [.env](/.env) & [.env.local](.env.local) - Environment variables (`.env.local` not tracked)

### Poetry Scripts
All scripts defined in `[tool.poetry.scripts]` delegate to [cli.py](src/python_fastapi_starter/cli.py):
- `start` → `main()` - Starts dev server with hot-reload
- `test` → `test()` - Runs pytest via dsp_toolkit
- `lint` → `lint_and_format()` - Runs Ruff via dsp_toolkit
- `release` → `release()` - Publishes new release via semantic-release

## Adding Features

### API Versioning
The API supports versioning via the `api-version` header. Clients specify the version number directly.

**Default behavior**: Latest version (currently version 2)

**Usage in requests**:
```
api-version: 1
api-version: 2
```

**Implementation pattern** in endpoints:
```python
from fastapi import Depends
from .versioning import get_api_version

@app.get("/items")
def list_items(version: int = Depends(get_api_version)):
    if version == 1:
        return {"items": []}
    elif version >= 2:
        return {"data": {"items": []}, "count": 0}
```

**Testing versioned endpoints**:
```python
def test_list_items_v1():
    response = client.get("/items", 
        headers={"api-version": "1"})
    assert response.json() == {"items": []}

def test_list_items_v2():
    response = client.get("/items", 
        headers={"api-version": "2"})
    assert "count" in response.json()
```

See [src/python_fastapi_starter/api/versioning.py](src/python_fastapi_starter/api/versioning.py) for implementation details.

### New Endpoints
1. Define route handlers in [src/python_fastapi_starter/api/main.py](src/python_fastapi_starter/api/main.py) or separate router files
2. Use Pydantic models for request/response validation
3. Reference [app.py](src/python_fastapi_starter/api/app.py) for accessing the FastAPI instance

### New Tests
1. Create test files in [tests/](tests/) following pytest conventions
2. Use `TestClient(app)` from `python_fastapi_starter.api.main`
3. Run with `poetry run test` or `poetry run test -k "pattern"`

### Database Changes
1. Update schema in [db/schema.sql](db/schema.sql)
2. Add seed data to [db/seed.sql](db/seed.sql)
3. Rebuild with `docker compose down db && docker compose up --build -d db`

## External Integration Points

- **dsp_toolkit**: Provides `load_environment()`, CLI utilities (`test`, `lint`, `release`), logging config
- **Uvicorn**: ASGI server; configured in [cli.py](src/python_fastapi_starter/cli.py) with reload mode
- **PostGIS/PostgreSQL**: External database service; credentials in env vars (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
- **Semantic Release**: Automatic versioning and changelog generation via [pyproject.toml](pyproject.toml) config
