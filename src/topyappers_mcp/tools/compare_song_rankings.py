"""MCP tool: compare_song_rankings."""

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
        "name": "compare_song_rankings",
        "description": (
            "Compare song chart rankings between two different weeks for a country. "
            "Shows position changes, new entries, and drops between the two weeks. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB')",
                },
                "week1": {
                    "type": "string",
                    "description": "First week in ISO format (e.g. '2026-W03')",
                },
                "week2": {
                    "type": "string",
                    "description": "Second week in ISO format (e.g. '2026-W04')",
                },
            },
            "required": ["country", "week1", "week2"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

async def handle(args, api_key):
    params = {
        "action": "compare",
        "country": args["country"],
        "week1": args["week1"],
        "week2": args["week2"],
    }
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
