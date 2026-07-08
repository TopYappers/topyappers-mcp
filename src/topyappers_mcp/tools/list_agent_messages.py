"""MCP tool: list_agent_messages."""

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
        "name": "list_agent_messages",
        "description": (
            "List saved outreach agent email messages. Use creatorEmail/email from an inbox "
            "to retrieve the full conversation history before drafting a customized reply. "
            "Can return outbound sent emails and inbound creator replies. "
            "Free — does not consume credits."
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
                "threadId": {
                    "type": "string",
                    "description": "Filter by Gmail thread ID",
                },
                "gmailAccountId": {
                    "type": "string",
                    "description": "Filter by connected Gmail account ID",
                },
                "direction": {
                    "type": "string",
                    "enum": ["all", "outbound", "inbound"],
                    "description": (
                        "Message direction. Use outbound for sent emails, "
                        "inbound for replies. Default: all."
                    ),
                    "default": "all",
                },
                "status": {
                    "type": "string",
                    "description": "Filter by stored message status, e.g. sent, received, replied, failed",
                },
                "isFollowUp": {
                    "type": "boolean",
                    "description": "Filter follow-up emails",
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

_AGENT_MESSAGE_KEYS = [
    "projectId", "creatorEmail", "creatorEmailContains", "creatorId",
    "threadId", "gmailAccountId", "direction", "status", "isFollowUp",
    "page", "perPage",
]

def _pick(args, keys):
    return {k: args[k] for k in keys if k in args}

async def handle(args, api_key):
    params = _pick(args, _AGENT_MESSAGE_KEYS)
    data, err = await api_get("/api/v1/agent/messages", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
