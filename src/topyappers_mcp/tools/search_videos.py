"""MCP tool: search_videos."""

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
        "name": "search_videos",
        "description": (
            "Search for video content from TikTok, Instagram, YouTube, and Twitch. "
            "Filter by creator handle, follower count, views, likes, comments, "
            "shares, hashtags, and text search in descriptions/captions. "
            "Sort by views, likes, shares, or follower count. "
            "Returns video metadata, engagement metrics, and subtitles. "
            "Costs 1 credit per video returned."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "userHandle": {
                    "type": "string",
                    "description": "Filter by specific creator handle/username",
                },
                "userFollowersMin": {
                    "type": "integer",
                    "description": "Minimum creator followers",
                },
                "userFollowersMax": {
                    "type": "integer",
                    "description": "Maximum creator followers",
                },
                "viewsMin": {
                    "type": "integer",
                    "description": "Minimum video views",
                },
                "viewsMax": {
                    "type": "integer",
                    "description": "Maximum video views",
                },
                "likesMin": {
                    "type": "integer",
                    "description": "Minimum likes",
                },
                "likesMax": {
                    "type": "integer",
                    "description": "Maximum likes",
                },
                "commentsMin": {
                    "type": "integer",
                    "description": "Minimum comments",
                },
                "commentsMax": {
                    "type": "integer",
                    "description": "Maximum comments",
                },
                "sharesMin": {
                    "type": "integer",
                    "description": "Minimum shares",
                },
                "sharesMax": {
                    "type": "integer",
                    "description": "Maximum shares",
                },
                "hashtags": {
                    "type": "string",
                    "description": "Filter by hashtags, comma-separated (e.g. 'fashion,streetwear,ootd')",
                },
                "textSearch": {
                    "type": "string",
                    "description": "Search keywords in video description/caption (e.g. 'workout routine')",
                },
                "sortBy": {
                    "type": "string",
                    "enum": ["user_followers", "views", "shares", "likes"],
                    "description": "Field to sort results by",
                },
                "sortOrder": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Sort direction (default: desc)",
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "perPage": {
                    "type": "integer",
                    "description": "Results per page (default: 20, max: 100)",
                    "default": 20,
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

_VIDEO_SEARCH_KEYS = [
    "userHandle", "userFollowersMin", "userFollowersMax",
    "viewsMin", "viewsMax", "likesMin", "likesMax",
    "commentsMin", "commentsMax", "sharesMin", "sharesMax",
    "hashtags", "textSearch", "sortBy", "sortOrder",
    "page", "perPage",
]

def _pick(args, keys):
    return {k: args[k] for k in keys if k in args}

async def handle(args, api_key):
    params = _pick(args, _VIDEO_SEARCH_KEYS)
    data, err = await api_get("/api/v1/videos", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
