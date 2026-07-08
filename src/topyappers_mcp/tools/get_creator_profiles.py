"""MCP tool: get_creator_profiles."""

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
        "name": "get_creator_profiles",
        "description": (
            "Fetch full creator/influencer profiles by their IDs (obtained from "
            "search_creators). Returns detailed profiles including follower count, "
            "average views, engagement rate, categories, bio, promoted products, "
            "niches, country, email, hashtags, and more. "
            "Costs 1 credit per creator returned."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "userIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Creator IDs from search_creators results "
                        "(e.g. ['instagram_57971538386', 'tiktok_12345'])"
                    ),
                },
            },
            "required": ["userIds"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

async def handle(args, api_key):
    user_ids = args.get("userIds")
    if not user_ids or not isinstance(user_ids, list):
        return tool_result(
            "Error: 'userIds' is required and must be a non-empty array of strings.",
            is_error=True,
        )
    data, err = await api_post("/api/v2/creators/get", {"userIds": user_ids}, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
