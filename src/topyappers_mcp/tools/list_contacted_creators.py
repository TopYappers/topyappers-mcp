"""MCP tool: list_contacted_creators."""

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
        "name": "list_contacted_creators",
        "description": (
            "List creators who have been contacted by the user's outreach agent via email. "
            "Filter by exact creator email from an inbox, creator ID, or project ID. "
            "Returns creator identity, project IDs, Gmail thread IDs, sent count, reply count, "
            "reply status, and latest outreach preview. Free — does not consume credits."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "projectId": {
                    "type": "string",
                    "description": "Filter to one agent project ID",
                },
                "creatorEmail": {
                    "type": "string",
                    "description": "Case-insensitive exact creator email match",
                },
                "creatorEmailContains": {
                    "type": "string",
                    "description": "Case-insensitive partial creator email match",
                },
                "creatorId": {
                    "type": "string",
                    "description": "Filter by creator ID",
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "perPage": {
                    "type": "integer",
                    "description": "Results per page (default: 50, max: 100)",
                    "default": 50,
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    }

_AGENT_CONTACTED_CREATOR_KEYS = [
    "projectId", "creatorEmail", "creatorEmailContains", "creatorId",
    "page", "perPage",
]

def _pick(args, keys):
    return {k: args[k] for k in keys if k in args}

async def handle(args, api_key):
    params = _pick(args, _AGENT_CONTACTED_CREATOR_KEYS)
    data, err = await api_get("/api/v1/agent/contacted-creators", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
