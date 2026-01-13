"""
Test suite for the FastAPI starter project.

Includes tests for the root endpoint with API versioning support.
"""

from fastapi.testclient import TestClient

from python_fastapi_starter.api.main import app


def test_read_root():
    """
    Test the root endpoint ('/') of the FastAPI app.

    Verifies status code and response payload for default version (latest).
    """
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    # Default is latest version (v2)
    data = response.json()
    assert data["message"] == "Hello, FastAPI starter!"
    assert data["version"] == 2
    assert data["status"] == "ok"


def test_read_root_version_1():
    """
    Test the root endpoint with explicit API version 1.
    """
    client = TestClient(app)
    response = client.get("/", headers={"Accept": "application/json; api-version=1"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI starter!"}


def test_read_root_version_2():
    """
    Test the root endpoint with API version 2.
    Version 2 includes additional fields in the response.
    """
    client = TestClient(app)
    response = client.get("/", headers={"Accept": "application/json; api-version=2"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, FastAPI starter!"
    assert data["version"] == 2
    assert data["status"] == "ok"
