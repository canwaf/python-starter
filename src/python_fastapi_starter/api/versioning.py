"""
API versioning support via custom API-Version header.
"""

from typing import Optional

from fastapi import Header

# Latest API version - increment when introducing new versions
LATEST_API_VERSION = 2


def get_api_version(api_version: Optional[int] = Header(None, alias="api-version")) -> int:
    """
    Extract API version from API-Version header.

    Expects header: api-version: 1
    If not specified, returns the latest API version.

    Args:
        api_version: API-Version header value from request

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
    if not api_version:
        return LATEST_API_VERSION

    try:
        version = api_version
        return max(1, version)  # Ensure minimum version is 1
    except (ValueError, TypeError):
        return LATEST_API_VERSION
