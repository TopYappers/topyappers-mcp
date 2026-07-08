"""MCP tool: get_new_song_entries."""

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
        "name": "get_new_song_entries",
        "description": (
            "Get songs that newly entered the chart for a specific country. "
            "Shows fresh trending songs that just appeared on the rankings. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB', 'FR')",
                },
            },
            "required": ["country"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

async def handle(args, api_key):
    params = {"action": "new-entries", "country": args["country"]}
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
