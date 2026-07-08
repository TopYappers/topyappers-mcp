"""TopYappers API client for Cloudflare Python Workers."""

from js import Headers, fetch
import js
from pyodide.ffi import to_js
import json
from urllib.parse import urlencode

from .constants import API_BASE


def _clean_params(params):
    """Prepare params for URL encoding: drop None, stringify booleans/lists."""
    cleaned = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, bool):
            cleaned[k] = "true" if v else "false"
        elif isinstance(v, list):
            cleaned[k] = ",".join(str(item).strip() for item in v if str(item).strip())
        else:
            cleaned[k] = v
    return cleaned


async def api_get(path, params, api_key):
    clean = _clean_params(params)
    url = f"{API_BASE}{path}"
    if clean:
        url += "?" + urlencode(clean)

    headers = Headers.new()
    headers.set("x-ty-api-key", api_key)
    headers.set("Accept", "application/json")

    resp = await fetch(
        url,
        to_js({"method": "GET", "headers": headers}, dict_converter=js.Object.fromEntries),
    )
    text = await resp.text()

    if resp.status != 200:
        return None, f"TopYappers API error (HTTP {resp.status}): {text}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        return None, f"Invalid JSON from API: {text[:500]}"


async def api_post(path, body, api_key):
    url = f"{API_BASE}{path}"

    headers = Headers.new()
    headers.set("x-ty-api-key", api_key)
    headers.set("Content-Type", "application/json")
    headers.set("Accept", "application/json")

    resp = await fetch(
        url,
        to_js(
            {"method": "POST", "headers": headers, "body": json.dumps(body)},
            dict_converter=js.Object.fromEntries,
        ),
    )
    text = await resp.text()

    if resp.status != 200:
        return None, f"TopYappers API error (HTTP {resp.status}): {text}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        return None, f"Invalid JSON from API: {text[:500]}"
