"""Cloudflare Worker entrypoint for the TopYappers MCP server."""

import json

from topyappers_mcp import oauth
from topyappers_mcp.constants import (
    MCP_PATH,
    PROTOCOL_VERSION,
    SERVER_NAME,
    SERVER_VERSION,
)
from topyappers_mcp.http import (
    empty_response,
    json_response,
    method_not_allowed_response,
)
from topyappers_mcp.instructions import INSTRUCTIONS
from topyappers_mcp.prompts import PROMPTS, render_prompt
from topyappers_mcp.rpc import rpc_error, rpc_success, tool_result
from topyappers_mcp.tools import PUBLIC_TOOLS, TOOL_HANDLERS, TOOLS

API_KEY_HEADER_NAMES = (
    "X-API-Key",
    "X-MyApp-API-Key",
    "X-Topyappers-API-Key",
    "Api-Key",
)


class AuthRequired(Exception):
    def __init__(self, req_id):
        super().__init__("Authentication required")
        self.req_id = req_id


def _header(headers, name):
    try:
        return headers.get(name)
    except Exception:
        return None


def extract_api_key(request):
    auth = _header(request.headers, "Authorization") or ""
    if auth.lower().startswith("bearer "):
        return auth[7:].strip() or None

    for header_name in API_KEY_HEADER_NAMES:
        value = _header(request.headers, header_name)
        if value:
            return str(value).strip() or None
    return None


def handle_initialize(req_id):
    return rpc_success(req_id, {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {}, "prompts": {}},
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        "instructions": INSTRUCTIONS,
    })


def handle_tools_list(req_id):
    return rpc_success(req_id, {"tools": TOOLS})


def handle_prompts_list(req_id):
    return rpc_success(req_id, {"prompts": PROMPTS})


def handle_prompts_get(req_id, params):
    name = params.get("name", "")
    prompt = next((p for p in PROMPTS if p["name"] == name), None)
    if not prompt:
        return rpc_error(req_id, -32602, f"Unknown prompt: {name}")
    return rpc_success(req_id, {"messages": render_prompt(name, params.get("arguments", []))})


async def handle_tool_call(req_id, params, api_key):
    tool_name = params.get("name", "")
    handler = TOOL_HANDLERS.get(tool_name)
    if not handler:
        return rpc_error(req_id, -32602, f"Unknown tool: {tool_name}")

    if tool_name not in PUBLIC_TOOLS and not api_key:
        raise AuthRequired(req_id)

    try:
        result = await handler(params.get("arguments", {}), api_key)
        return rpc_success(req_id, result)
    except Exception as exc:
        return rpc_success(
            req_id,
            tool_result(f"Tool execution error: {str(exc)}", is_error=True),
        )


async def handle_rpc(rpc, api_key, env):
    method = rpc.get("method", "")
    req_id = rpc.get("id")
    params = rpc.get("params", {})
    is_notification = req_id is None

    if method == "initialize":
        return handle_initialize(req_id)
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return rpc_success(req_id, {})
    if method == "tools/list":
        return handle_tools_list(req_id)
    if method == "prompts/list":
        return handle_prompts_list(req_id)
    if method == "prompts/get":
        return handle_prompts_get(req_id, params)
    if method == "tools/call":
        return await handle_tool_call(req_id, params, api_key)

    if is_notification:
        return None
    return rpc_error(req_id, -32601, f"Method not found: {method}")


def _is_path(path, expected):
    if expected == "/":
        return path == "/"
    return path == expected or path == f"{expected}/"


def _server_info():
    return json_response({
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "protocol": "MCP",
        "transport": {
            "endpoint": MCP_PATH,
            "url_hint": "Use /mcp for hosted MCP clients.",
        },
        "description": (
            "TopYappers MCP Server - discover viral content, trending songs, "
            "and influencers across TikTok, Instagram, YouTube, and Twitch."
        ),
        "tools": len(TOOLS),
    })


async def _handle_mcp_post(request, env):
    try:
        body_text = await request.text()
        rpc = json.loads(body_text)
    except Exception:
        return json_response(rpc_error(None, -32700, "Parse error: invalid JSON"))

    api_key = extract_api_key(request)

    try:
        if isinstance(rpc, list):
            results = []
            for msg in rpc:
                if not api_key and oauth.calls_protected_tool(msg, TOOL_HANDLERS, PUBLIC_TOOLS):
                    raise AuthRequired(msg.get("id"))
                result = await handle_rpc(msg, api_key, env)
                if result is not None:
                    results.append(result)
            return json_response(results) if results else empty_response()

        if not api_key and oauth.calls_protected_tool(rpc, TOOL_HANDLERS, PUBLIC_TOOLS):
            raise AuthRequired(rpc.get("id"))
        result = await handle_rpc(rpc, api_key, env)
    except AuthRequired as exc:
        return oauth.auth_required_response(request, exc.req_id, env)

    return json_response(result) if result is not None else empty_response()


async def on_fetch(request, env):
    path = oauth.request_path(request)

    if request.method == "OPTIONS":
        return empty_response(204)

    if _is_path(path, "/.well-known/oauth-protected-resource"):
        if request.method != "GET":
            return method_not_allowed_response()
        return json_response(oauth.protected_resource_metadata(request, env, "/"))

    if _is_path(path, "/.well-known/oauth-protected-resource/mcp"):
        if request.method != "GET":
            return method_not_allowed_response()
        return json_response(oauth.protected_resource_metadata(request, env, MCP_PATH))

    if _is_path(path, "/.well-known/oauth-authorization-server") or _is_path(
        path,
        "/.well-known/openid-configuration",
    ):
        if request.method != "GET":
            return method_not_allowed_response()
        return json_response(oauth.authorization_server_metadata(request, env))

    if _is_path(path, "/authorize"):
        if request.method not in ("GET", "POST"):
            return method_not_allowed_response("Method not allowed for /authorize.")
        return await oauth.handle_authorize(request, env)

    if _is_path(path, "/token"):
        if request.method != "POST":
            return method_not_allowed_response("Method not allowed for /token.")
        return await oauth.handle_token(request, env)

    if _is_path(path, MCP_PATH):
        if request.method == "GET":
            return method_not_allowed_response()
        if request.method == "DELETE":
            return empty_response(200)
        if request.method == "POST":
            return await _handle_mcp_post(request, env)
        return method_not_allowed_response()

    if _is_path(path, "/"):
        if request.method == "GET":
            return _server_info()
        if request.method == "DELETE":
            return empty_response(200)
        if request.method == "POST":
            return await _handle_mcp_post(request, env)
        return method_not_allowed_response()

    return json_response({"error": "Not found"}, status=404)
