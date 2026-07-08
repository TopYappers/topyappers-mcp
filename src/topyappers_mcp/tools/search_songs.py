"""MCP tool: search_songs."""

import json

from ..api import api_get, api_post
from ..constants import (
    ACCOUNT_TYPES,
    BODY_COMPLEXIONS,
    CATEGORIES,
    GENDERS,
    LANGUAGES,
    PROMOTED_BUSINESS_TYPES,
    SOURCES,
)
from ..rpc import tool_result


TOOL = {
        "name": "search_songs",
        "description": (
            "Search for songs by title or artist name. Returns matching songs "
            "with chart performance data. Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "Search query — song title or artist name",
                },
            },
            "required": ["q"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

async def handle(args, api_key):
    params = {"action": "search", "q": args["q"]}
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
