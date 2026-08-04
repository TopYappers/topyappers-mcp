"""MCP tool: search_creators."""

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
        "name": "search_creators",
        "description": (
            "Search for influencers and creators across TikTok, Instagram, YouTube, "
            "Twitch, LinkedIn, and X/Twitter. "
            "This endpoint is FREE — it returns creator IDs. Pass those IDs to "
            "get_creator_profiles to fetch full profiles. "
            "Start with 'nichesToPromote' — the primary discovery filter. It uses AI-analyzed "
            "niche data that is very granular and specific: 'calorie counter', 'ai tools', "
            "'standing desk', 'budget travel', 'new moms'. "
            "IMPORTANT: nichesToPromote uses AND logic — always search ONE keyword per call "
            "and run 5+ searches with different keywords, then merge results. "
            "Use 'mainCategory' only as a fallback when niche terms aren't specific enough."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "followersMin": {
                    "type": "integer",
                    "description": "Minimum followers",
                },
                "followersMax": {
                    "type": "integer",
                    "description": "Maximum followers",
                },
                "averageViewsMin": {
                    "type": "integer",
                    "description": "Minimum average views per post",
                },
                "averageViewsMax": {
                    "type": "integer",
                    "description": "Maximum average views per post",
                },
                "averageLikesMin": {
                    "type": "integer",
                    "description": "Minimum average likes per post",
                },
                "averageLikesMax": {
                    "type": "integer",
                    "description": "Maximum average likes per post",
                },
                "engagementRateMin": {
                    "type": "number",
                    "description": "Minimum engagement rate as percentage (e.g. 2.5 for 2.5%)",
                },
                "engagementRateMax": {
                    "type": "number",
                    "description": "Maximum engagement rate as percentage",
                },
                "uploadsPerWeekMin": {
                    "type": "number",
                    "description": "Minimum estimated posts/uploads per week",
                },
                "uploadsPerWeekMax": {
                    "type": "number",
                    "description": "Maximum estimated posts/uploads per week",
                },
                "uploadsPerMonthMin": {
                    "type": "number",
                    "description": "Minimum estimated posts/uploads per month",
                },
                "uploadsPerMonthMax": {
                    "type": "number",
                    "description": "Maximum estimated posts/uploads per month",
                },
                "avgVideoDurationSecondsMin": {
                    "type": "number",
                    "description": "Minimum average video duration in seconds",
                },
                "avgVideoDurationSecondsMax": {
                    "type": "number",
                    "description": "Maximum average video duration in seconds",
                },
                "promotionsCountMin": {
                    "type": "integer",
                    "description": "Minimum number of detected promotional posts",
                },
                "promotionsCountMax": {
                    "type": "integer",
                    "description": "Maximum number of detected promotional posts",
                },
                "affiliatePostsCountMin": {
                    "type": "integer",
                    "description": "Minimum number of detected affiliate posts",
                },
                "affiliatePostsCountMax": {
                    "type": "integer",
                    "description": "Maximum number of detected affiliate posts",
                },
                "sponsorshipPostsCountMin": {
                    "type": "integer",
                    "description": "Minimum number of detected sponsorship posts",
                },
                "sponsorshipPostsCountMax": {
                    "type": "integer",
                    "description": "Maximum number of detected sponsorship posts",
                },
                "age": {
                    "type": "string",
                    "description": "Age group, comma-separated for multiple (e.g. '20-29,30-39')",
                },
                "gender": {
                    "type": "string",
                    "enum": GENDERS,
                    "description": "Creator gender",
                },
                "race": {
                    "type": "string",
                    "description": (
                        "Creator ethnicity/race, comma-separated for multiple. "
                        "Allowed values: latino hispanic, middle eastern, indian, "
                        "east asian, white, black, southeast asian. Use "
                        "'latino hispanic' for Latino, Latina, or Hispanic requests."
                    ),
                },
                "hairColor": {
                    "type": "string",
                    "description": "Hair color, comma-separated. Allowed: black, brunette, white, blonde, red.",
                },
                "bodyComplexion": {
                    "type": "string",
                    "description": "Body type, comma-separated. Allowed: skinny, ordinary, overweight, hulk.",
                },
                "mainCategory": {
                    "type": "string",
                    "enum": CATEGORIES,
                    "description": "Main content category",
                },
                "subCategories": {
                    "type": "string",
                    "description": "Sub-categories, comma-separated free text (e.g. 'streetwear,vegan recipes')",
                },
                "subCategory": {
                    "type": "string",
                    "description": "Deprecated alias for subCategories; prefer subCategories.",
                },
                "bio": {
                    "type": "string",
                    "description": "Keywords to search in creator's bio (e.g. 'tiktok shop')",
                },
                "promotedProducts": {
                    "type": "string",
                    "description": (
                        "Products/services creator has promoted, comma-separated "
                        "(e.g. 'beef tallow,feastables')"
                    ),
                },
                "nichesToPromote": {
                    "type": "string",
                    "description": (
                        "AI-analyzed niches — the most powerful creator discovery filter. "
                        "Free text, very granular: 'calorie counter', 'ai tools', 'standing desk', "
                        "'budget travel', 'new moms'. ALWAYS pass ONE keyword only per call — "
                        "this is an AND filter. Run 5+ separate searches with different keywords "
                        "and combine the results for best coverage."
                    ),
                },
                "promotedBusinessType": {
                    "type": "string",
                    "enum": PROMOTED_BUSINESS_TYPES,
                    "description": "Business type the creator is suitable to promote",
                },
                "accountType": {
                    "type": "string",
                    "enum": ACCOUNT_TYPES,
                    "description": "Creator/account type",
                },
                "country": {
                    "type": "string",
                    "description": "Creator's country (e.g. 'France', 'United States')",
                },
                "source": {
                    "type": "string",
                    "enum": SOURCES,
                    "description": "Platform source (use 'twitter' for X/Twitter)",
                },
                "username": {
                    "type": "string",
                    "description": "Filter by creator handle/username",
                },
                "language": {
                    "type": "string",
                    "enum": LANGUAGES,
                    "description": "Creator's primary content language",
                },
                "hashtags": {
                    "type": "string",
                    "description": (
                        "Hashtags in creator content, comma-separated. AND matching — "
                        "all must be present. '#' prefix optional. (e.g. 'fitness,gym')"
                    ),
                },
                "keywords": {
                    "type": "string",
                    "description": (
                        "General keyword search across searchable creator fields. "
                        "Comma-separated terms are OR-searched."
                    ),
                },
                "keywordsExcluded": {
                    "type": "string",
                    "description": "Comma-separated keywords to exclude from text searches.",
                },
                "emailExists": {
                    "type": "boolean",
                    "description": "Only return creators with an available email address",
                },
                "email": {
                    "type": "string",
                    "description": "Find creator by exact email address",
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "perPage": {
                    "type": "integer",
                    "description": "Results per page (default: 10, max: 100)",
                    "default": 10,
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    }

_CREATOR_SEARCH_KEYS = [
    "followersMin", "followersMax", "averageViewsMin", "averageViewsMax",
    "averageLikesMin", "averageLikesMax", "engagementRateMin",
    "engagementRateMax", "uploadsPerWeekMin", "uploadsPerWeekMax",
    "uploadsPerMonthMin", "uploadsPerMonthMax",
    "avgVideoDurationSecondsMin", "avgVideoDurationSecondsMax",
    "promotionsCountMin", "promotionsCountMax",
    "affiliatePostsCountMin", "affiliatePostsCountMax",
    "sponsorshipPostsCountMin", "sponsorshipPostsCountMax",
    "age", "gender", "race", "hairColor", "bodyComplexion",
    "mainCategory", "subCategories", "subCategory", "bio",
    "promotedProducts", "nichesToPromote", "promotedBusinessType",
    "accountType", "country", "source", "username", "language",
    "hashtags", "keywords", "keywordsExcluded", "emailExists",
    "email", "page", "perPage",
]

def _pick(args, keys):
    return {k: args[k] for k in keys if k in args}

async def handle(args, api_key):
    params = _pick(args, _CREATOR_SEARCH_KEYS)
    if "subCategory" in params and "subCategories" not in params:
        params["subCategories"] = params["subCategory"]
    params.pop("subCategory", None)
    data, err = await api_get("/api/v2/creators/search", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))
