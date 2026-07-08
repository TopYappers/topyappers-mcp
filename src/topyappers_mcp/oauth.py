"""Claude-compatible OAuth shim for API-key based MCP authentication."""

import base64
import hashlib
import hmac
import json
import time
from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse, urlunparse

from .constants import (
    AUTH_CODE_TTL_SECONDS,
    DEFAULT_OAUTH_CLIENT_ID,
    DEFAULT_SCOPE,
    MCP_PATH,
    TOKEN_EXPIRES_IN,
)

NO_STORE_HEADERS = {
    "Cache-Control": "no-store",
    "Pragma": "no-cache",
}


class OAuthError(Exception):
    def __init__(self, error, description, status=400):
        super().__init__(description)
        self.error = error
        self.description = description
        self.status = status


def env_value(env, *names):
    for name in names:
        try:
            value = getattr(env, name, None)
        except Exception:
            value = None
        if value:
            return str(value)
    return None


def request_origin(request):
    parsed = urlparse(str(request.url))
    return f"{parsed.scheme}://{parsed.netloc}"


def request_path(request):
    return urlparse(str(request.url)).path or "/"


def base_url_for_request(request, env=None):
    configured = env_value(env, "PUBLIC_BASE_URL", "OAUTH_ISSUER", "MCP_BASE_URL") if env else None
    if configured:
        return configured.rstrip("/")
    return request_origin(request).rstrip("/")


def root_resource(base_url):
    return f"{base_url.rstrip('/')}/"


def mcp_resource(base_url):
    return f"{base_url.rstrip('/')}{MCP_PATH}"


def metadata_url_for_resource(request, env=None, resource_path=MCP_PATH):
    base = base_url_for_request(request, env)
    suffix = "/mcp" if resource_path == MCP_PATH else ""
    return f"{base}/.well-known/oauth-protected-resource{suffix}"


def metadata_resource_from_request(request, env=None):
    base = base_url_for_request(request, env)
    return mcp_resource(base) if request_path(request).endswith("/mcp") else root_resource(base)


def protected_resource_metadata(request, env=None, resource_path=None):
    base = base_url_for_request(request, env)
    resource = mcp_resource(base) if resource_path == MCP_PATH else metadata_resource_from_request(request, env)
    return {
        "resource": resource,
        "authorization_servers": [base.rstrip("/")],
        "bearer_methods_supported": ["header"],
        "scopes_supported": [DEFAULT_SCOPE],
    }


def authorization_server_metadata(request, env=None):
    base = base_url_for_request(request, env)
    return {
        "issuer": base,
        "authorization_endpoint": f"{base}/authorize",
        "token_endpoint": f"{base}/token",
        "response_types_supported": ["code"],
        "grant_types_supported": [
            "authorization_code",
            "refresh_token",
            "client_credentials",
        ],
        "scopes_supported": [DEFAULT_SCOPE],
        "token_endpoint_auth_methods_supported": [
            "client_secret_post",
            "client_secret_basic",
        ],
        "code_challenge_methods_supported": ["S256"],
    }


def bearer_challenge(request, env=None):
    return (
        'Bearer error="invalid_token", '
        'error_description="Authentication required", '
        f'resource_metadata="{metadata_url_for_resource(request, env, MCP_PATH)}", '
        f'scope="{DEFAULT_SCOPE}"'
    )


def _b64url_encode(raw):
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64url_decode(value):
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def _json_dumps(data):
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def _allowlist(env):
    raw = env_value(env, "OAUTH_CLIENT_IDS", "CLAUDE_OAUTH_CLIENT_IDS")
    if not raw:
        return None
    return {item.strip() for item in raw.split(",") if item.strip()}


def client_id_allowed(client_id, env):
    if not client_id:
        return False
    allowed = _allowlist(env)
    if allowed is None:
        return True
    return client_id in allowed


def code_secret(env):
    return env_value(
        env,
        "OAUTH_CODE_SECRET",
        "CLAUDE_OAUTH_CODE_SECRET",
        "TOPYAPPERS_OAUTH_CODE_SECRET",
        "TOPYAPPERS_API_KEY",
    ) or DEFAULT_OAUTH_CLIENT_ID


def encode_oauth_code(payload, secret):
    body = _json_dumps(payload).encode("utf-8")
    signature = hmac.new(str(secret).encode("utf-8"), body, hashlib.sha256).digest()
    return f"{_b64url_encode(body)}.{_b64url_encode(signature)}"


def decode_oauth_code(code, secret):
    try:
        body_part, signature_part = str(code).split(".", 1)
        body = _b64url_decode(body_part)
        signature = _b64url_decode(signature_part)
    except Exception as exc:
        raise OAuthError("invalid_grant", "Invalid authorization code") from exc

    expected = hmac.new(str(secret).encode("utf-8"), body, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected):
        raise OAuthError("invalid_grant", "Invalid authorization code")

    try:
        return json.loads(body.decode("utf-8"))
    except Exception as exc:
        raise OAuthError("invalid_grant", "Invalid authorization code") from exc


def validate_oauth_code(code, env, now=None):
    payload = decode_oauth_code(code, code_secret(env))
    current_time = int(now if now is not None else time.time())
    if int(payload.get("exp", 0)) < current_time:
        raise OAuthError("invalid_grant", "Authorization code has expired")
    return payload


def append_query_params(uri, params):
    parsed = urlparse(uri)
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    pairs.extend((key, value) for key, value in params.items() if value is not None)
    return urlunparse(parsed._replace(query=urlencode(pairs)))


def oauth_redirect_error(redirect_uri, error, description, state=None):
    return append_query_params(
        redirect_uri,
        {
            "error": error,
            "error_description": description,
            "state": state,
        },
    )


def query_params(request):
    parsed = urlparse(str(request.url))
    return {key: values[-1] for key, values in parse_qs(parsed.query).items()}


async def read_form(request):
    body_text = await request.text()
    if not body_text:
        return {}

    content_type = request.headers.get("Content-Type") or ""
    if "application/json" in content_type:
        try:
            data = json.loads(body_text)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    return {key: values[-1] for key, values in parse_qs(body_text).items()}


def create_authorization_redirect(params, base_url, env, now=None):
    redirect_uri = params.get("redirect_uri", "")
    state = params.get("state")

    if not redirect_uri:
        raise OAuthError("invalid_request", "redirect_uri is required")

    def redirect_error(error, description):
        return oauth_redirect_error(redirect_uri, error, description, state)

    if params.get("response_type") != "code":
        return redirect_error("invalid_request", "response_type must be code")

    client_id = params.get("client_id", "")
    if not client_id_allowed(client_id, env):
        return redirect_error("invalid_request", "Unknown OAuth client_id")

    code_challenge_method = params.get("code_challenge_method")
    if code_challenge_method and code_challenge_method != "S256":
        return redirect_error("invalid_request", "Only S256 PKCE is supported")

    current_time = int(now if now is not None else time.time())
    payload = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": params.get("code_challenge", ""),
        "resource": params.get("resource") or mcp_resource(base_url),
        "exp": current_time + AUTH_CODE_TTL_SECONDS,
    }
    code = encode_oauth_code(payload, code_secret(env))
    return append_query_params(redirect_uri, {"code": code, "state": state})


def extract_basic_client_auth(authorization_header):
    if not authorization_header:
        return None, None
    scheme, _, value = str(authorization_header).partition(" ")
    if scheme.lower() != "basic" or not value:
        return None, None
    try:
        decoded = base64.b64decode(value).decode("utf-8")
    except Exception:
        return None, None
    client_id, sep, client_secret = decoded.partition(":")
    if not sep:
        return None, None
    return client_id, client_secret


def _is_root_resource(value):
    parsed = urlparse(value)
    return parsed.path in ("", "/") and not parsed.params and not parsed.query and not parsed.fragment


def resources_match(left, right):
    if not left or not right:
        return False
    if left == right:
        return True
    left_parsed = urlparse(left)
    right_parsed = urlparse(right)
    if _is_root_resource(left) and _is_root_resource(right):
        return (
            left_parsed.scheme == right_parsed.scheme
            and left_parsed.netloc == right_parsed.netloc
        )
    return False


def _token_body(api_key):
    return {
        "access_token": api_key,
        "token_type": "Bearer",
        "expires_in": TOKEN_EXPIRES_IN,
        "refresh_token": api_key,
        "scope": DEFAULT_SCOPE,
    }


def create_token_response(params, authorization_header, env, now=None):
    basic_client_id, basic_secret = extract_basic_client_auth(authorization_header)
    client_id = params.get("client_id") or basic_client_id
    grant_type = params.get("grant_type", "")

    if not client_id_allowed(client_id, env):
        raise OAuthError("invalid_client", "Unknown OAuth client_id", status=401)

    api_key = basic_secret or params.get("client_secret")
    if grant_type == "refresh_token":
        api_key = api_key or params.get("refresh_token")

    if not api_key:
        raise OAuthError(
            "invalid_client",
            "client_secret/API key is required for this OAuth shim.",
            status=401,
        )

    if grant_type == "authorization_code":
        code = params.get("code")
        if not code:
            raise OAuthError("invalid_grant", "authorization code is required")
        payload = validate_oauth_code(code, env, now=now)

        if payload.get("client_id") != client_id:
            raise OAuthError("invalid_grant", "Authorization code client_id mismatch")

        redirect_uri = params.get("redirect_uri")
        if redirect_uri and redirect_uri != payload.get("redirect_uri"):
            raise OAuthError("invalid_grant", "Authorization code redirect_uri mismatch")

        resource = params.get("resource")
        code_resource = payload.get("resource")
        if resource and code_resource and not resources_match(resource, code_resource):
            raise OAuthError("invalid_target", "Requested resource does not match authorization code")

    elif grant_type == "refresh_token":
        if not params.get("refresh_token") and not basic_secret:
            raise OAuthError("invalid_grant", "refresh_token/API key is required")

    elif grant_type == "client_credentials":
        pass

    else:
        raise OAuthError("unsupported_grant_type", "Unsupported grant_type")

    return _token_body(api_key)


def oauth_error(error, description, status=400):
    from .http import json_response

    return json_response(
        {"error": error, "error_description": description},
        status=status,
        extra_headers=dict(NO_STORE_HEADERS),
    )


def auth_required_response(request, req_id, env=None):
    from .http import json_response
    from .rpc import rpc_success, tool_result

    body = rpc_success(
        req_id,
        tool_result(
            "Authentication required. Pass your TopYappers API key as a Bearer "
            "token or complete the OAuth connector flow.",
            is_error=True,
        ),
    )
    return json_response(
        body,
        status=401,
        extra_headers={"WWW-Authenticate": bearer_challenge(request, env)},
    )


async def handle_authorize(request, env):
    from .http import redirect_response

    params = query_params(request)
    if request.method == "POST":
        params.update(await read_form(request))
    try:
        location = create_authorization_redirect(params, base_url_for_request(request, env), env)
    except OAuthError as exc:
        return oauth_error(exc.error, exc.description, status=exc.status)
    return redirect_response(location)


async def handle_token(request, env):
    params = await read_form(request)
    auth_header = request.headers.get("Authorization") or ""
    try:
        body = create_token_response(params, auth_header, env)
    except OAuthError as exc:
        return oauth_error(exc.error, exc.description, status=exc.status)

    from .http import json_response

    return json_response(body, status=200, extra_headers=dict(NO_STORE_HEADERS))


def calls_protected_tool(rpc, tool_handlers, public_tools=None):
    public_tools = public_tools or set()
    if not isinstance(rpc, dict) or rpc.get("method") != "tools/call":
        return False
    tool_name = rpc.get("params", {}).get("name", "")
    return tool_name in tool_handlers and tool_name not in public_tools

