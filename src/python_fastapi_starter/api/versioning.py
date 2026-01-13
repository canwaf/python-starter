"""
API versioning support via Accept header.
Parses the 'api-version' parameter from Accept header to determine API version.
"""

from typing import Optional

from fastapi import Header

# Latest API version - increment when introducing new versions
LATEST_API_VERSION = 2


def get_api_version(accept: Optional[str] = Header(None)) -> int:
    """
    Extract API version from Accept header.

    Expects format: application/json; api-version=1
    If not specified, returns the latest API version.

    Args:
        accept: Accept header value from request

    Returns:
        int: API version (1, 2, 3, etc.). Defaults to LATEST_API_VERSION.

    Example:
        @app.get("/items")
        def list_items(version: int = Depends(get_api_version)):
            if version == 1:
                return {"items": []}
            elif version == 2:
                return {"data": {"items": []}}
    """
    if not accept:
        return LATEST_API_VERSION

    # Parse 'api-version=X' from Accept header
    parts = accept.split(";")
    for part in parts[1:]:
        part = part.strip()
        if part.startswith("api-version="):
            try:
                version = int(part.split("=")[1])
                return max(1, version)  # Ensure minimum version is 1
            except (ValueError, IndexError):
                pass

    return LATEST_API_VERSION
