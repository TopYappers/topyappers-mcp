#!/usr/bin/env python3
"""Smoke-check the hosted OAuth shim and MCP transport endpoints.

Usage:
  BASE_URL=https://mcp.topyappers.com API_KEY=... python scripts/check_oauth_shim.py

The script intentionally disables redirect following for /authorize so it can
inspect the OAuth code and state that Claude expects in the callback URL.
"""

import base64
import json
import os
import sys
from urllib import parse, request
from urllib.error import HTTPError


BASE_URL = os.environ.get("BASE_URL", "http://localhost:8787").rstrip("/")
API_KEY = os.environ.get("API_KEY", "test-api-key")
CLIENT_ID = os.environ.get("CLIENT_ID", "myapp-claude")
REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = request.build_opener(NoRedirect)


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def http_json(method, path, body=None, headers=None, expected_status=200):
    data = None
    if body is not None:
        if isinstance(body, dict):
            data = parse.urlencode(body).encode("utf-8")
            headers = {"Content-Type": "application/x-www-form-urlencoded", **(headers or {})}
        else:
            data = body.encode("utf-8")
    req = request.Request(f"{BASE_URL}{path}", data=data, headers=headers or {}, method=method)
    try:
        resp = OPENER.open(req)
        status = resp.status
        raw = resp.read().decode("utf-8")
        response_headers = resp.headers
    except HTTPError as exc:
        status = exc.code
        raw = exc.read().decode("utf-8")
        response_headers = exc.headers

    if status != expected_status:
        fail(f"{method} {path} returned {status}, expected {expected_status}: {raw}")
    return json.loads(raw) if raw else None, response_headers


def http_raw(method, path, body=None, headers=None, expected_status=200):
    data = body.encode("utf-8") if isinstance(body, str) else body
    req = request.Request(f"{BASE_URL}{path}", data=data, headers=headers or {}, method=method)
    try:
        resp = OPENER.open(req)
        status = resp.status
        raw = resp.read().decode("utf-8")
        response_headers = resp.headers
    except HTTPError as exc:
        status = exc.code
        raw = exc.read().decode("utf-8")
        response_headers = exc.headers

    if status != expected_status:
        fail(f"{method} {path} returned {status}, expected {expected_status}: {raw}")
    return raw, response_headers


def authorization_code():
    query = parse.urlencode(
        {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "code_challenge": "test-challenge",
            "code_challenge_method": "S256",
            "state": "state-123",
            "scope": "myapp:read",
            "resource": f"{BASE_URL}/mcp",
        }
    )
    _, headers = http_raw("GET", f"/authorize?{query}", expected_status=302)
    location = headers.get("Location")
    if not location:
        fail("/authorize did not return a Location header")
    parsed = parse.urlparse(location)
    params = parse.parse_qs(parsed.query)
    if params.get("state") != ["state-123"]:
        fail("/authorize did not preserve state")
    code = params.get("code", [None])[0]
    if not code:
        fail("/authorize did not return code")
    return code


def main():
    http_json("GET", "/mcp", expected_status=405)

    init_body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init, _ = http_raw(
        "POST",
        "/mcp",
        body=init_body,
        headers={"Content-Type": "application/json"},
        expected_status=200,
    )
    if '"protocolVersion"' not in init:
        fail("POST /mcp initialize did not return MCP initialization data")

    tool_call = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "list_agent_projects", "arguments": {}},
        }
    )
    _, headers = http_raw(
        "POST",
        "/mcp",
        body=tool_call,
        headers={"Content-Type": "application/json"},
        expected_status=401,
    )
    challenge = headers.get("WWW-Authenticate", "")
    expected_metadata = f'{BASE_URL}/.well-known/oauth-protected-resource/mcp'
    if expected_metadata not in challenge:
        fail("WWW-Authenticate does not point to /mcp protected-resource metadata")

    metadata, _ = http_json("GET", "/.well-known/oauth-protected-resource/mcp")
    if metadata.get("resource") != f"{BASE_URL}/mcp":
        fail("protected-resource metadata resource is not exactly BASE_URL/mcp")

    code = authorization_code()
    token, _ = http_json(
        "POST",
        "/token",
        body={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": API_KEY,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "resource": f"{BASE_URL}/mcp",
        },
    )
    if token.get("access_token") != API_KEY:
        fail("client_secret_post token response did not return client_secret as access_token")

    basic = base64.b64encode(f"{CLIENT_ID}:{API_KEY}".encode("utf-8")).decode("ascii")
    token, _ = http_json(
        "POST",
        "/token",
        body={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {basic}"},
    )
    if token.get("access_token") != API_KEY:
        fail("Basic auth token response did not return Basic password as access_token")

    bad, _ = http_json(
        "POST",
        "/token",
        body={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": API_KEY,
            "code": code,
            "resource": f"{BASE_URL}/mcp/",
        },
        expected_status=400,
    )
    if bad.get("error") != "invalid_target":
        fail("/token did not reject mismatched /mcp/ resource")

    print("OK: OAuth shim and /mcp transport checks passed")


if __name__ == "__main__":
    main()
