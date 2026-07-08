import base64
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from topyappers_mcp.oauth import (  # noqa: E402
    OAuthError,
    create_authorization_redirect,
    create_token_response,
    decode_oauth_code,
    mcp_resource,
    protected_resource_metadata,
    resources_match,
    validate_oauth_code,
)


class Env:
    OAUTH_CODE_SECRET = "unit-test-secret"


class Request:
    url = "https://example.com/.well-known/oauth-protected-resource/mcp"


class OAuthShimTests(unittest.TestCase):
    def test_mcp_protected_resource_metadata_is_exact(self):
        metadata = protected_resource_metadata(Request(), Env(), "/mcp")
        self.assertEqual(metadata["resource"], "https://example.com/mcp")

    def test_authorization_redirect_contains_code_and_state(self):
        location = create_authorization_redirect(
            {
                "response_type": "code",
                "client_id": "myapp-claude",
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "code_challenge": "challenge",
                "code_challenge_method": "S256",
                "state": "abc123",
                "resource": "https://example.com/mcp",
            },
            "https://example.com",
            Env(),
            now=1000,
        )
        parsed = urlparse(location)
        query = parse_qs(parsed.query)
        self.assertEqual(query["state"], ["abc123"])
        payload = decode_oauth_code(query["code"][0], Env.OAUTH_CODE_SECRET)
        self.assertEqual(validate_oauth_code(query["code"][0], Env(), now=1000), payload)
        self.assertEqual(payload["resource"], "https://example.com/mcp")

    def test_token_response_returns_client_secret_without_pkce_verifier(self):
        location = create_authorization_redirect(
            {
                "response_type": "code",
                "client_id": "myapp-claude",
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "code_challenge": "challenge",
                "code_challenge_method": "S256",
                "resource": "https://example.com/mcp",
            },
            "https://example.com",
            Env(),
            now=1000,
        )
        code = parse_qs(urlparse(location).query)["code"][0]
        body = create_token_response(
            {
                "grant_type": "authorization_code",
                "client_id": "myapp-claude",
                "client_secret": "USER_API_KEY",
                "code": code,
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "resource": "https://example.com/mcp",
            },
            "",
            Env(),
            now=1000,
        )
        self.assertEqual(body["access_token"], "USER_API_KEY")
        self.assertEqual(body["refresh_token"], "USER_API_KEY")

    def test_basic_auth_password_becomes_access_token(self):
        auth = base64.b64encode(b"myapp-claude:BASIC_API_KEY").decode("ascii")
        body = create_token_response(
            {"grant_type": "client_credentials"},
            f"Basic {auth}",
            Env(),
        )
        self.assertEqual(body["access_token"], "BASIC_API_KEY")

    def test_token_resource_must_match_mcp_path_exactly(self):
        location = create_authorization_redirect(
            {
                "response_type": "code",
                "client_id": "myapp-claude",
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "resource": "https://example.com/mcp",
            },
            "https://example.com",
            Env(),
            now=1000,
        )
        code = parse_qs(urlparse(location).query)["code"][0]
        with self.assertRaises(OAuthError):
            create_token_response(
                {
                    "grant_type": "authorization_code",
                    "client_id": "myapp-claude",
                    "client_secret": "USER_API_KEY",
                    "code": code,
                    "resource": "https://example.com/mcp/",
                },
                "",
                Env(),
                now=1000,
            )

    def test_root_slash_resources_are_equivalent_only_at_root(self):
        self.assertTrue(resources_match("https://example.com", "https://example.com/"))
        self.assertFalse(resources_match("https://example.com/mcp", "https://example.com/mcp/"))
        self.assertEqual(mcp_resource("https://example.com/"), "https://example.com/mcp")


if __name__ == "__main__":
    unittest.main()
