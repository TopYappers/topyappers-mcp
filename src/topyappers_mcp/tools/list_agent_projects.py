"""MCP tool: list_agent_projects."""

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
        "name": "list_agent_projects",
        "description": (
            "List the user's TopYappers outreach agent projects/campaigns. "
            "Use this to map project IDs from message history to campaign details, "
            "targeting, deal terms, and custom instructions. Free — does not consume credits."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    }

async def handle(args, api_key):
    data, err = await api_get("/api/v1/agent/projects", {}, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
