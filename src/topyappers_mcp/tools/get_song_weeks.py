"""MCP tool: get_song_weeks."""

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
        "name": "get_song_weeks",
        "description": (
            "Get available weeks for a specific country in the Songs API. "
            "Use this to discover valid week values before querying rankings "
            "or comparisons. Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country_code": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB')",
                },
            },
            "required": ["country_code"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

async def handle(args, api_key):
    params = {"action": "weeks", "country_code": args["country_code"]}
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
