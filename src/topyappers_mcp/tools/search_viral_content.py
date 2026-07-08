"""MCP tool: search_viral_content."""

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
        "name": "search_viral_content",
        "description": (
            "Discover viral TikTok content. Filter by content category, country, "
            "view count, virality score (views÷followers ratio, 0–1), date range, "
            "music/sound title, and opening hook text. Returns video URLs, engagement "
            "metrics, virality scores, and creator info. Costs 1 credit per result."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "array",
                    "items": {"type": "string", "enum": CATEGORIES},
                    "description": "Content categories to filter by (e.g. ['Music', 'Fashion'])",
                },
                "countries": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Countries to filter by using full names "
                        "(e.g. ['United States', 'France', 'United Kingdom'])"
                    ),
                },
                "viewsMin": {
                    "type": "integer",
                    "description": "Minimum number of views",
                },
                "viewsMax": {
                    "type": "integer",
                    "description": "Maximum number of views",
                },
                "viralityScoreMin": {
                    "type": "number",
                    "description": (
                        "Minimum virality score (0–1). Higher means more viral "
                        "relative to follower count. 0.5+ is highly viral."
                    ),
                },
                "viralityScoreMax": {
                    "type": "number",
                    "description": "Maximum virality score (0–1)",
                },
                "followersMin": {
                    "type": "integer",
                    "description": "Minimum creator followers",
                },
                "followersMax": {
                    "type": "integer",
                    "description": "Maximum creator followers",
                },
                "dateCreatedFrom": {
                    "type": "string",
                    "description": "Posts created on or after this date (YYYY-MM-DD)",
                },
                "dateCreatedTo": {
                    "type": "string",
                    "description": "Posts created on or before this date (YYYY-MM-DD)",
                },
                "musicTitle": {
                    "type": "string",
                    "description": "Filter by music/sound title (case-insensitive partial match)",
                },
                "hook": {
                    "type": "string",
                    "description": "Filter by video opening hook text (case-insensitive partial match)",
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "pageSize": {
                    "type": "integer",
                    "description": "Results per page (default: 12, max: 100)",
                    "default": 12,
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

_VIRAL_CONTENT_KEYS = [
    "categories", "countries", "viewsMin", "viewsMax",
    "viralityScoreMin", "viralityScoreMax", "followersMin", "followersMax",
    "dateCreatedFrom", "dateCreatedTo", "musicTitle", "hook",
    "page", "pageSize",
]

def _pick(args, keys):
    return {k: args[k] for k in keys if k in args}

async def handle(args, api_key):
    body = _pick(args, _VIRAL_CONTENT_KEYS)
    data, err = await api_post("/api/v1/viral-content", body, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
