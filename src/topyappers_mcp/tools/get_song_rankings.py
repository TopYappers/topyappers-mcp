"""MCP tool: get_song_rankings."""

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
        "name": "get_song_rankings",
        "description": (
            "Get trending song chart rankings for a specific country or globally. "
            "Pass a country code (e.g. 'US', 'GB', 'FR') for country-specific charts, "
            "or set global=true for worldwide rankings. Optionally specify a week in "
            "ISO format (YYYY-Www, e.g. '2026-W04'). Omit week for the latest data. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB', 'FR'). Omit for global rankings.",
                },
                "global_rankings": {
                    "type": "boolean",
                    "description": "Set to true for global rankings instead of country-specific",
                    "default": False,
                },
                "week": {
                    "type": "string",
                    "description": "Week in ISO format (YYYY-Www, e.g. '2026-W04'). Omit for latest.",
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

async def handle(args, api_key):
    params = {"action": "global" if args.get("global_rankings") else "rankings"}
    if "country" in args:
        params["country"] = args["country"]
    if "week" in args:
        params["week"] = args["week"]
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
