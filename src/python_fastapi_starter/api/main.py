"""
Main FastAPI application for the starter project.
Defines the API endpoints and app instance.
"""

from fastapi import Depends

from .app import create_app
from .versioning import get_api_version

app = create_app()


@app.get("/")
def read_root(version: int = Depends(get_api_version)):
    """
    Root endpoint for health check and welcome message.
    Returns a JSON response with a greeting.

    API Versioning:
        - Default (no version header): version 1
        - With header: Accept: application/json; api-version=2
    """
    if version == 1:
        return {"message": "Hello, FastAPI starter!"}
    elif version >= 2:
        return {
            "message": "Hello, FastAPI starter!",
            "version": version,
            "status": "ok",
        }
