"""HTTP response and CORS helpers for the Worker runtime."""

import json

from js import Headers, Response

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": (
        "Content-Type, Authorization, X-API-Key, X-MyApp-API-Key, "
        "X-Topyappers-API-Key, Api-Key, Mcp-Session-Id, "
        "MCP-Protocol-Version, Accept"
    ),
    "Access-Control-Expose-Headers": "WWW-Authenticate, Mcp-Session-Id",
    "Access-Control-Max-Age": "86400",
}


def apply_cors(headers):
    for key, value in CORS_HEADERS.items():
        headers.set(key, value)
    return headers


def make_headers(content_type=None, extra_headers=None):
    headers = Headers.new()
    if content_type:
        headers.set("Content-Type", content_type)
    apply_cors(headers)
    for key, value in (extra_headers or {}).items():
        headers.set(key, value)
    return headers


def json_response(body, status=200, extra_headers=None):
    headers = make_headers("application/json", extra_headers)
    return Response.new(json.dumps(body), status=status, headers=headers)


def html_response(body, status=200, extra_headers=None):
    headers = make_headers("text/html; charset=utf-8", extra_headers)
    return Response.new(body, status=status, headers=headers)


def empty_response(status=202, extra_headers=None):
    return Response.new("", status=status, headers=make_headers(None, extra_headers))


def redirect_response(url, status=302):
    return empty_response(status, {"Location": url})


def method_not_allowed_response(message="Method not allowed. Use POST for MCP messages."):
    return json_response({"error": message}, status=405)

