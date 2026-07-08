"""MCP tool: get_song_history."""

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
        "name": "get_song_history",
        "description": (
            "Get the full chart performance history of a specific song over time. "
            "Shows rank progression week by week. Requires song_id (obtainable from "
            "get_song_rankings or search_songs results) and a country_code. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "song_id": {
                    "type": "string",
                    "description": "Song ID from rankings or search results",
                },
                "country_code": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB')",
                },
            },
            "required": ["song_id", "country_code"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

async def handle(args, api_key):
    params = {
        "action": "song-history",
        "song_id": args["song_id"],
        "country_code": args["country_code"],
    }
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
