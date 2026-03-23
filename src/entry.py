"""
TopYappers MCP Server — Cloudflare Workers (Python)

An MCP (Model Context Protocol) server that proxies the TopYappers API,
enabling AI agents to discover viral content, trending songs, and influencers.

Authentication: Clients pass their TopYappers API key as a Bearer token
in the Authorization header. The server forwards it to the TopYappers API.
"""

from js import Response, Headers, fetch
import js
from pyodide.ffi import to_js
import json
from urllib.parse import urlencode


# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════

API_BASE = "https://www.topyappers.com"
PROTOCOL_VERSION = "2025-03-26"
SERVER_NAME = "topyappers"
SERVER_VERSION = "1.0.0"

CATEGORIES = [
    "Arts", "Automotive", "Beauty & Personal Care", "Books & Literature",
    "Business", "Finance", "Career & Jobs", "Collectibles & Hobbies",
    "Community", "Ecommerce", "Crafts & DIY", "Culture", "Education",
    "Technology", "Entertainment", "Environment", "Family", "Parenting",
    "Fashion", "Film", "Fitness", "Health", "Food", "Gaming",
    "Gardening & Agriculture", "History", "Home", "Humor", "Law",
    "Government", "Lifestyle", "Marketing", "Mental Health", "Music",
    "News & Media", "Outdoors", "Nature", "Pets", "Animals",
    "Philosophy", "Spirituality", "Photography", "Videography", "Politics",
    "Relationships", "Religion", "Science", "Self-Improvement", "Shopping",
    "Social Media", "Social Issues & Activism", "Sports", "Travel",
    "Vehicles & Transportation", "Virtual Reality", "Weapons & Defense",
    "Writing", "Kids",
]

SOURCES = ["tiktok", "instagram", "youtube"]
GENDERS = ["male", "female"]
LANGUAGES = [
    "arabic", "bengali", "bosnian", "bulgarian", "cantonese", "catalan",
    "croatian", "czech", "danish", "dutch", "english", "estonian",
    "filipino", "finnish", "french", "german", "greek", "gujarati",
    "hausa", "hebrew", "hindi", "hungarian", "icelandic", "indonesian",
    "italian", "japanese", "javanese", "kannada", "kazakh", "korean",
    "latvian", "lithuanian", "malay", "malayalam", "mandarin", "marathi",
    "nepali", "norwegian", "pashto", "persian", "polish", "portuguese",
    "punjabi", "romanian", "russian", "serbian", "sinhala", "slovak",
    "slovenian", "somali", "spanish", "swahili", "swedish", "tamil",
    "telugu", "thai", "turkish", "ukrainian", "urdu", "uzbek",
    "vietnamese", "yoruba",
]


# ═══════════════════════════════════════════════════════════════════════════
# Tool definitions
# ═══════════════════════════════════════════════════════════════════════════

TOOLS = [
    {
        "name": "search_viral_content",
        "description": (
            "Discover viral TikTok content. Filter by content category, country, "
            "view count, virality score (views÷followers ratio, 0–1), date range, "
            "music/sound title, and opening hook text. Returns video URLs, engagement "
            "metrics, virality scores, and creator info. Costs 1 credit per result."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "array",
                    "items": {"type": "string", "enum": CATEGORIES},
                    "description": "Content categories to filter by (e.g. ['Music', 'Fashion'])",
                },
                "countries": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Countries to filter by using full names "
                        "(e.g. ['United States', 'France', 'United Kingdom'])"
                    ),
                },
                "viewsMin": {
                    "type": "integer",
                    "description": "Minimum number of views",
                },
                "viewsMax": {
                    "type": "integer",
                    "description": "Maximum number of views",
                },
                "viralityScoreMin": {
                    "type": "number",
                    "description": (
                        "Minimum virality score (0–1). Higher means more viral "
                        "relative to follower count. 0.5+ is highly viral."
                    ),
                },
                "viralityScoreMax": {
                    "type": "number",
                    "description": "Maximum virality score (0–1)",
                },
                "followersMin": {
                    "type": "integer",
                    "description": "Minimum creator followers",
                },
                "followersMax": {
                    "type": "integer",
                    "description": "Maximum creator followers",
                },
                "dateCreatedFrom": {
                    "type": "string",
                    "description": "Posts created on or after this date (YYYY-MM-DD)",
                },
                "dateCreatedTo": {
                    "type": "string",
                    "description": "Posts created on or before this date (YYYY-MM-DD)",
                },
                "musicTitle": {
                    "type": "string",
                    "description": "Filter by music/sound title (case-insensitive partial match)",
                },
                "hook": {
                    "type": "string",
                    "description": "Filter by video opening hook text (case-insensitive partial match)",
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "pageSize": {
                    "type": "integer",
                    "description": "Results per page (default: 12, max: 100)",
                    "default": 12,
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "search_creators",
        "description": (
            "Search for influencers and creators across TikTok, Instagram, and YouTube. "
            "Filter by followers, average views, engagement rate, content category, country, "
            "language, bio keywords, promoted products, niches, hashtags, username, and email. "
            "This endpoint is FREE — it returns creator IDs. Pass those IDs to "
            "get_creator_profiles to fetch full profiles with details. "
            "The 'nichesToPromote' filter is especially powerful for AI-analyzed niche matching "
            "(e.g. 'SaaS', 'skincare', 'fitness supplements')."
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
                "engagementRateMin": {
                    "type": "number",
                    "description": "Minimum engagement rate as percentage (e.g. 2.5 for 2.5%)",
                },
                "engagementRateMax": {
                    "type": "number",
                    "description": "Maximum engagement rate as percentage",
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
                "mainCategory": {
                    "type": "string",
                    "enum": CATEGORIES,
                    "description": "Main content category",
                },
                "subCategory": {
                    "type": "string",
                    "description": "Sub-category free text (e.g. 'streetwear', 'vegan recipes')",
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
                        "AI-analyzed niches, comma-separated. Best discovery filter. "
                        "Examples: 'SaaS', 'skincare,beauty', 'fitness supplements'"
                    ),
                },
                "country": {
                    "type": "string",
                    "description": "Creator's country (e.g. 'France', 'United States')",
                },
                "source": {
                    "type": "string",
                    "enum": SOURCES,
                    "description": "Platform source",
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
    },
    {
        "name": "get_creator_profiles",
        "description": (
            "Fetch full creator/influencer profiles by their IDs (obtained from "
            "search_creators). Returns detailed profiles including follower count, "
            "average views, engagement rate, categories, bio, promoted products, "
            "niches, country, email, hashtags, and more. "
            "Costs 1 credit per creator returned."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "userIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Creator IDs from search_creators results "
                        "(e.g. ['instagram_57971538386', 'tiktok_12345'])"
                    ),
                },
            },
            "required": ["userIds"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "search_videos",
        "description": (
            "Search for video content from TikTok, Instagram, and YouTube. "
            "Filter by creator handle, follower count, views, likes, comments, "
            "shares, hashtags, and text search in descriptions/captions. "
            "Sort by views, likes, shares, or follower count. "
            "Returns video metadata, engagement metrics, and subtitles. "
            "Costs 1 credit per video returned."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "userHandle": {
                    "type": "string",
                    "description": "Filter by specific creator handle/username",
                },
                "userFollowersMin": {
                    "type": "integer",
                    "description": "Minimum creator followers",
                },
                "userFollowersMax": {
                    "type": "integer",
                    "description": "Maximum creator followers",
                },
                "viewsMin": {
                    "type": "integer",
                    "description": "Minimum video views",
                },
                "viewsMax": {
                    "type": "integer",
                    "description": "Maximum video views",
                },
                "likesMin": {
                    "type": "integer",
                    "description": "Minimum likes",
                },
                "likesMax": {
                    "type": "integer",
                    "description": "Maximum likes",
                },
                "commentsMin": {
                    "type": "integer",
                    "description": "Minimum comments",
                },
                "commentsMax": {
                    "type": "integer",
                    "description": "Maximum comments",
                },
                "sharesMin": {
                    "type": "integer",
                    "description": "Minimum shares",
                },
                "sharesMax": {
                    "type": "integer",
                    "description": "Maximum shares",
                },
                "hashtags": {
                    "type": "string",
                    "description": "Filter by hashtags, comma-separated (e.g. 'fashion,streetwear,ootd')",
                },
                "textSearch": {
                    "type": "string",
                    "description": "Search keywords in video description/caption (e.g. 'workout routine')",
                },
                "sortBy": {
                    "type": "string",
                    "enum": ["user_followers", "views", "shares", "likes"],
                    "description": "Field to sort results by",
                },
                "sortOrder": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Sort direction (default: desc)",
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "perPage": {
                    "type": "integer",
                    "description": "Results per page (default: 20, max: 100)",
                    "default": 20,
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "get_song_rankings",
        "description": (
            "Get trending song chart rankings for a specific country or globally. "
            "Pass a country code (e.g. 'US', 'GB', 'FR') for country-specific charts, "
            "or set global=true for worldwide rankings. Optionally specify a week in "
            "ISO format (YYYY-Www, e.g. '2026-W04'). Omit week for the latest data. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB', 'FR'). Omit for global rankings.",
                },
                "global_rankings": {
                    "type": "boolean",
                    "description": "Set to true for global rankings instead of country-specific",
                    "default": False,
                },
                "week": {
                    "type": "string",
                    "description": "Week in ISO format (YYYY-Www, e.g. '2026-W04'). Omit for latest.",
                },
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "get_new_song_entries",
        "description": (
            "Get songs that newly entered the chart for a specific country. "
            "Shows fresh trending songs that just appeared on the rankings. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB', 'FR')",
                },
            },
            "required": ["country"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "search_songs",
        "description": (
            "Search for songs by title or artist name. Returns matching songs "
            "with chart performance data. Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "Search query — song title or artist name",
                },
            },
            "required": ["q"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "get_song_history",
        "description": (
            "Get the full chart performance history of a specific song over time. "
            "Shows rank progression week by week. Requires song_id (obtainable from "
            "get_song_rankings or search_songs results) and a country_code. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "song_id": {
                    "type": "string",
                    "description": "Song ID from rankings or search results",
                },
                "country_code": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB')",
                },
            },
            "required": ["song_id", "country_code"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "compare_song_rankings",
        "description": (
            "Compare song chart rankings between two different weeks for a country. "
            "Shows position changes, new entries, and drops between the two weeks. "
            "Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB')",
                },
                "week1": {
                    "type": "string",
                    "description": "First week in ISO format (e.g. '2026-W03')",
                },
                "week2": {
                    "type": "string",
                    "description": "Second week in ISO format (e.g. '2026-W04')",
                },
            },
            "required": ["country", "week1", "week2"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "get_song_countries",
        "description": (
            "Get the list of available countries (with their codes) for the "
            "Songs API. Use this to discover valid country codes before calling "
            "other song tools. Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
    {
        "name": "get_song_weeks",
        "description": (
            "Get available weeks for a specific country in the Songs API. "
            "Use this to discover valid week values before querying rankings "
            "or comparisons. Costs 10 credits per request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country_code": {
                    "type": "string",
                    "description": "Country code (e.g. 'US', 'GB')",
                },
            },
            "required": ["country_code"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": True},
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# JSON-RPC helpers
# ═══════════════════════════════════════════════════════════════════════════

def rpc_success(req_id, result):
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def rpc_error(req_id, code, message):
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def tool_result(text, is_error=False):
    return {
        "content": [{"type": "text", "text": text}],
        **({"isError": True} if is_error else {}),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Instructions for AI agents
# ═══════════════════════════════════════════════════════════════════════════

INSTRUCTIONS = """# TopYappers MCP — Agent Guide

You have access to the TopYappers API through this MCP server. It lets you discover **viral content**, **trending songs**, and **influencers/creators** across TikTok, Instagram, and YouTube.

## 1. Finding Viral Content

Use `search_viral_content` to discover viral TikTok posts.

**Key filters:**
- `categories` — content categories (e.g. `["Fitness", "Food"]`). Use the exact enum values like "Beauty & Personal Care", "Crafts & DIY", etc.
- `countries` — full country names (e.g. `["United States", "France"]`), NOT country codes.
- `viralityScoreMin` — the virality score is views÷followers (0–1). Use 0.3+ for moderately viral, 0.5+ for highly viral.
- `dateCreatedFrom` / `dateCreatedTo` — filter by date range (YYYY-MM-DD format).
- `musicTitle` — find posts using a specific trending sound (partial match).
- `hook` — filter by the opening hook text of videos (partial match).

**Cost:** 1 credit per returned result. Control costs with `pageSize` (default 12, max 100).

## 2. Finding Creators / Influencers

This is a **two-step workflow** to save credits:

**Step 1 — Search (FREE):** Call `search_creators` with filters. This returns creator IDs, not full profiles. Use as many filters as relevant:
- `mainCategory` — exact enum values like "Fashion", "Technology", "Fitness"
- `source` — "tiktok", "instagram", or "youtube"
- `nichesToPromote` — the most powerful filter. AI-analyzed niches, free text. Examples: "SaaS", "skincare", "fitness supplements", "meal prep"
- `country` — full country name (e.g. "France", "United States")
- `language` — lowercase (e.g. "english", "spanish", "french")
- `followersMin` / `followersMax` — follower range
- `engagementRateMin` — percentage (e.g. 2.5 for 2.5%)
- `hashtags` — comma-separated, AND matching (e.g. "fitness,gym" requires both)
- `bio` — keyword search in bio text
- `emailExists` — set `true` to only get creators with contact email

**CRITICAL — AND matching for nichesToPromote, promotedProducts, and hashtags:**
These fields use AND logic when comma-separated. Passing `nichesToPromote=skincare,beauty` only returns creators matching BOTH terms, which can return zero results. **Always search ONE keyword at a time** and combine the userIds from multiple searches. Since search is free, run several narrow searches instead of one broad one:
1. `nichesToPromote=skincare` → collect userIds
2. `nichesToPromote=beauty` → collect userIds
3. Deduplicate and pass the merged list to `get_creator_profiles`

**Step 2 — Get profiles (1 credit each):** Pass the `userIds` from Step 1 to `get_creator_profiles`. Returns full profiles with follower count, engagement rate, bio, email, promoted products, etc.

**Pagination:** Use `page` and `perPage` in search. Check `response.total_pages` and `response.next_page` to know if more results exist.

## 3. Finding Videos

Use `search_videos` to find specific video content.

**Key filters:**
- `textSearch` — search in video descriptions/captions (e.g. "workout routine")
- `hashtags` — comma-separated (e.g. "fashion,streetwear,ootd")
- `sortBy` — "views", "likes", "shares", or "user_followers"
- `sortOrder` — "desc" (default) or "asc"
- Engagement ranges: `viewsMin`/`viewsMax`, `likesMin`/`likesMax`, etc.

**Cost:** 1 credit per video returned.

## 4. Trending Songs

Multiple tools for song chart data. All cost **10 credits per request**.

**Common workflows:**
- **Get current charts:** `get_song_rankings` with `country: "US"` (or `global_rankings: true`)
- **See what's new:** `get_new_song_entries` with a country code
- **Find a song:** `search_songs` with `q: "song title or artist"`
- **Track a song:** `get_song_history` with `song_id` and `country_code`
- **Compare weeks:** `compare_song_rankings` with `country`, `week1`, `week2`

**Important:** Song tools use **country codes** (e.g. "US", "GB", "FR"), NOT full names. Use `get_song_countries` to discover valid codes. Weeks use ISO format: "YYYY-Www" (e.g. "2026-W04").

## Credit costs summary

| Tool | Cost |
|------|------|
| search_creators | FREE |
| get_creator_profiles | 1 credit per creator |
| search_viral_content | 1 credit per result |
| search_videos | 1 credit per video |
| All song tools | 10 credits per request |

## Tips for agents

- **One keyword per search for nichesToPromote/promotedProducts/hashtags:** These are AND filters. Multiple comma-separated values require ALL to match. Always run separate searches with one keyword each, then merge the userIds. Search is free so there's no cost.
- **Be credit-efficient:** Start with `search_creators` (free) before calling `get_creator_profiles`. Use smaller `pageSize` / `perPage` when exploring.
- **Combine filters wisely:** Mix different filter types (category + followers + country) for targeted results, but keep AND text filters (nichesToPromote, promotedProducts, hashtags) to a single value per call.
- **nichesToPromote is your best friend:** For finding creators who'd be a good fit for a product, `nichesToPromote` uses AI-analyzed data and supports free text search. Run multiple single-keyword searches to cover different angles.
- **Virality score:** A video with 1M views from a creator with 10K followers (score ~1.0) is far more impressive than 1M views from someone with 10M followers (score ~0.1).
- **Country format matters:** Viral content and creators use full names ("United States"). Songs use codes ("US").
"""


# ═══════════════════════════════════════════════════════════════════════════
# MCP Prompts — reusable workflow templates for agents
# ═══════════════════════════════════════════════════════════════════════════

PROMPTS = [
    {
        "name": "find_viral_content",
        "description": (
            "Discover viral TikTok content for a specific niche or topic. "
            "Returns a guided workflow to find the most viral posts."
        ),
        "arguments": [
            {
                "name": "topic",
                "description": "The content topic, niche, or category (e.g. 'fitness', 'cooking', 'tech reviews')",
                "required": True,
            },
            {
                "name": "country",
                "description": "Target country (full name, e.g. 'United States')",
                "required": False,
            },
        ],
    },
    {
        "name": "find_creators_for_product",
        "description": (
            "Find influencers/creators who would be a great fit for promoting "
            "a specific product or service. Uses the free search + profile workflow."
        ),
        "arguments": [
            {
                "name": "product",
                "description": "The product, service, or brand to find creators for (e.g. 'skincare brand', 'SaaS tool', 'fitness app')",
                "required": True,
            },
            {
                "name": "platform",
                "description": "Preferred platform: tiktok, instagram, or youtube",
                "required": False,
            },
            {
                "name": "country",
                "description": "Target country (full name, e.g. 'France')",
                "required": False,
            },
        ],
    },
    {
        "name": "trending_songs_report",
        "description": (
            "Generate a trending songs report for a country — current rankings, "
            "new entries, and week-over-week changes."
        ),
        "arguments": [
            {
                "name": "country_code",
                "description": "Country code (e.g. 'US', 'GB', 'FR')",
                "required": True,
            },
        ],
    },
    {
        "name": "competitor_content_analysis",
        "description": (
            "Analyze a specific creator's content — find their videos, "
            "see what performs well, and discover similar creators in the same niche."
        ),
        "arguments": [
            {
                "name": "username",
                "description": "Creator's handle/username to analyze",
                "required": True,
            },
            {
                "name": "platform",
                "description": "Platform: tiktok, instagram, or youtube",
                "required": False,
            },
        ],
    },
]


def _render_prompt(name, arguments):
    """Generate the messages for a prompt invocation."""
    args = {a["name"]: a.get("value", "") for a in (arguments or [])}

    if name == "find_viral_content":
        topic = args.get("topic", "trending content")
        country = args.get("country", "")
        country_filter = f', countries: ["{country}"]' if country else ""
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": (
                        f"Find the most viral TikTok content about '{topic}'. "
                        f"Here's what I'd like you to do:\n\n"
                        f"1. Use search_viral_content with a relevant category for '{topic}'"
                        f"{country_filter}, set viralityScoreMin to 0.3 for quality results, "
                        f"and pageSize to 10.\n"
                        f"2. Review the results — highlight the top posts by virality score.\n"
                        f"3. For each top post, note: the hook text, view count, virality score, "
                        f"music used, and the creator's username.\n"
                        f"4. Identify patterns: what hooks, music, or formats are working?\n"
                        f"5. Summarize actionable takeaways for creating viral content in this niche."
                    ),
                },
            }
        ]

    if name == "find_creators_for_product":
        product = args.get("product", "a product")
        platform = args.get("platform", "")
        country = args.get("country", "")
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": (
                        f"Find the best influencers/creators to promote '{product}'. "
                        f"Follow this workflow:\n\n"
                        f"1. Use search_creators with nichesToPromote set to relevant terms for "
                        f"'{product}'"
                        f"{f', source: \"{platform}\"' if platform else ''}"
                        f"{f', country: \"{country}\"' if country else ''}"
                        f", followersMin: 10000, engagementRateMin: 2.0, emailExists: true, "
                        f"perPage: 20.\n"
                        f"2. Take the returned userIds and call get_creator_profiles to fetch "
                        f"full details.\n"
                        f"3. For each creator, evaluate: follower count, engagement rate, "
                        f"bio relevance, categories, promoted products (check for competitor "
                        f"conflicts), and available email.\n"
                        f"4. Rank the top 5-10 creators by fit for '{product}' and explain why "
                        f"each is a good match.\n"
                        f"5. Provide their contact emails and suggested outreach talking points."
                    ),
                },
            }
        ]

    if name == "trending_songs_report":
        cc = args.get("country_code", "US")
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": (
                        f"Create a trending songs report for country code '{cc}':\n\n"
                        f"1. Call get_song_rankings with country: '{cc}' to get current charts.\n"
                        f"2. Call get_new_song_entries with country: '{cc}' to see fresh entries.\n"
                        f"3. Get the available weeks with get_song_weeks for country_code: '{cc}', "
                        f"then call compare_song_rankings with the two most recent weeks.\n"
                        f"4. Compile a report covering:\n"
                        f"   - Top 10 songs with rank, artist, and weeks on chart\n"
                        f"   - Notable new entries and their initial positions\n"
                        f"   - Biggest movers (up and down) between the two weeks\n"
                        f"   - Any patterns or trends (genres, artists dominating, etc.)"
                    ),
                },
            }
        ]

    if name == "competitor_content_analysis":
        username = args.get("username", "")
        platform = args.get("platform", "")
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": (
                        f"Analyze the creator '@{username}' and their content:\n\n"
                        f"1. Use search_creators with username: '{username}'"
                        f"{f', source: \"{platform}\"' if platform else ''}"
                        f" to find their profile ID.\n"
                        f"2. Call get_creator_profiles with the returned userId for full details.\n"
                        f"3. Use search_videos with userHandle: '{username}', sortBy: 'views', "
                        f"sortOrder: 'desc' to find their top-performing content.\n"
                        f"4. Analyze:\n"
                        f"   - Their niche and content category\n"
                        f"   - Top videos: what topics, hashtags, and formats perform best?\n"
                        f"   - Engagement metrics: views, likes, comments, shares ratios\n"
                        f"5. Then search_creators with the same mainCategory and similar "
                        f"follower range to find comparable creators in their space.\n"
                        f"6. Summarize findings with actionable insights."
                    ),
                },
            }
        ]

    return [
        {
            "role": "user",
            "content": {"type": "text", "text": f"Unknown prompt: {name}"},
        }
    ]


# ═══════════════════════════════════════════════════════════════════════════
# MCP protocol handlers
# ═══════════════════════════════════════════════════════════════════════════

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
    arguments = params.get("arguments", [])
    prompt = next((p for p in PROMPTS if p["name"] == name), None)
    if not prompt:
        return rpc_error(req_id, -32602, f"Unknown prompt: {name}")
    messages = _render_prompt(name, arguments)
    return rpc_success(req_id, {"messages": messages})


# ═══════════════════════════════════════════════════════════════════════════
# TopYappers API client
# ═══════════════════════════════════════════════════════════════════════════

def _clean_params(params):
    """Prepare params for URL encoding: drop None, stringify booleans."""
    cleaned = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, bool):
            cleaned[k] = "true" if v else "false"
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


# ═══════════════════════════════════════════════════════════════════════════
# Tool handlers
# ═══════════════════════════════════════════════════════════════════════════

_VIRAL_CONTENT_KEYS = [
    "categories", "countries", "viewsMin", "viewsMax",
    "viralityScoreMin", "viralityScoreMax", "followersMin", "followersMax",
    "dateCreatedFrom", "dateCreatedTo", "musicTitle", "hook",
    "page", "pageSize",
]

_CREATOR_SEARCH_KEYS = [
    "followersMin", "followersMax", "averageViewsMin", "averageViewsMax",
    "engagementRateMin", "engagementRateMax", "age", "gender",
    "mainCategory", "subCategory", "bio", "promotedProducts",
    "nichesToPromote", "country", "source", "username",
    "language", "hashtags", "emailExists", "email", "page", "perPage",
]

_VIDEO_SEARCH_KEYS = [
    "userHandle", "userFollowersMin", "userFollowersMax",
    "viewsMin", "viewsMax", "likesMin", "likesMax",
    "commentsMin", "commentsMax", "sharesMin", "sharesMax",
    "hashtags", "textSearch", "sortBy", "sortOrder",
    "page", "perPage",
]


def _pick(args, keys):
    return {k: args[k] for k in keys if k in args}


async def handle_search_viral_content(args, api_key):
    body = _pick(args, _VIRAL_CONTENT_KEYS)
    data, err = await api_post("/api/v1/viral-content", body, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_search_creators(args, api_key):
    params = _pick(args, _CREATOR_SEARCH_KEYS)
    data, err = await api_get("/api/v2/creators/search", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_get_creator_profiles(args, api_key):
    user_ids = args.get("userIds")
    if not user_ids or not isinstance(user_ids, list):
        return tool_result(
            "Error: 'userIds' is required and must be a non-empty array of strings.",
            is_error=True,
        )
    data, err = await api_post("/api/v2/creators/get", {"userIds": user_ids}, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_search_videos(args, api_key):
    params = _pick(args, _VIDEO_SEARCH_KEYS)
    data, err = await api_get("/api/v1/videos", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_get_song_rankings(args, api_key):
    params = {"action": "global" if args.get("global_rankings") else "rankings"}
    if "country" in args:
        params["country"] = args["country"]
    if "week" in args:
        params["week"] = args["week"]
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_get_new_song_entries(args, api_key):
    params = {"action": "new-entries", "country": args["country"]}
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_search_songs(args, api_key):
    params = {"action": "search", "q": args["q"]}
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_get_song_history(args, api_key):
    params = {
        "action": "song-history",
        "song_id": args["song_id"],
        "country_code": args["country_code"],
    }
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_compare_song_rankings(args, api_key):
    params = {
        "action": "compare",
        "country": args["country"],
        "week1": args["week1"],
        "week2": args["week2"],
    }
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_get_song_countries(args, api_key):
    params = {"action": "countries"}
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


async def handle_get_song_weeks(args, api_key):
    params = {"action": "weeks", "country_code": args["country_code"]}
    data, err = await api_get("/api/v1/songs", params, api_key)
    if err:
        return tool_result(err, is_error=True)
    return tool_result(json.dumps(data, indent=2))


TOOL_HANDLERS = {
    "search_viral_content": handle_search_viral_content,
    "search_creators": handle_search_creators,
    "get_creator_profiles": handle_get_creator_profiles,
    "search_videos": handle_search_videos,
    "get_song_rankings": handle_get_song_rankings,
    "get_new_song_entries": handle_get_new_song_entries,
    "search_songs": handle_search_songs,
    "get_song_history": handle_get_song_history,
    "compare_song_rankings": handle_compare_song_rankings,
    "get_song_countries": handle_get_song_countries,
    "get_song_weeks": handle_get_song_weeks,
}


# ═══════════════════════════════════════════════════════════════════════════
# HTTP layer
# ═══════════════════════════════════════════════════════════════════════════

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, Mcp-Session-Id",
    "Access-Control-Max-Age": "86400",
}


def json_response(body, status=200):
    headers = Headers.new()
    headers.set("Content-Type", "application/json")
    for k, v in CORS_HEADERS.items():
        headers.set(k, v)
    return Response.new(json.dumps(body), status=status, headers=headers)


def empty_response(status=202):
    headers = Headers.new()
    for k, v in CORS_HEADERS.items():
        headers.set(k, v)
    return Response.new("", status=status, headers=headers)


def extract_api_key(request):
    auth = request.headers.get("Authorization") or ""
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return None


async def handle_rpc(rpc, api_key, env):
    """Process a single JSON-RPC message. Returns a response dict or None for notifications."""
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
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        handler = TOOL_HANDLERS.get(tool_name)
        if not handler:
            return rpc_error(req_id, -32602, f"Unknown tool: {tool_name}")

        resolved_key = api_key or getattr(env, "TOPYAPPERS_API_KEY", None)
        if not resolved_key:
            return rpc_success(
                req_id,
                tool_result(
                    "Authentication required. Pass your TopYappers API key as a "
                    "Bearer token in the Authorization header.",
                    is_error=True,
                ),
            )

        try:
            result = await handler(arguments, resolved_key)
            return rpc_success(req_id, result)
        except Exception as e:
            return rpc_success(
                req_id,
                tool_result(f"Tool execution error: {str(e)}", is_error=True),
            )

    if is_notification:
        return None

    return rpc_error(req_id, -32601, f"Method not found: {method}")


# ═══════════════════════════════════════════════════════════════════════════
# Cloudflare Workers entry point
# ═══════════════════════════════════════════════════════════════════════════

async def on_fetch(request, env):
    if request.method == "OPTIONS":
        headers = Headers.new()
        for k, v in CORS_HEADERS.items():
            headers.set(k, v)
        return Response.new("", status=204, headers=headers)

    if request.method == "GET":
        return json_response({
            "name": SERVER_NAME,
            "version": SERVER_VERSION,
            "protocol": "MCP",
            "description": (
                "TopYappers MCP Server — discover viral content, trending songs, "
                "and influencers across TikTok, Instagram, and YouTube."
            ),
            "tools": len(TOOLS),
        })

    if request.method == "DELETE":
        return empty_response(200)

    if request.method != "POST":
        return json_response({"error": "Method not allowed. Use POST for MCP messages."}, status=405)

    try:
        body_text = await request.text()
        rpc = json.loads(body_text)
    except Exception:
        return json_response(rpc_error(None, -32700, "Parse error: invalid JSON"))

    api_key = extract_api_key(request)

    if isinstance(rpc, list):
        results = []
        for msg in rpc:
            result = await handle_rpc(msg, api_key, env)
            if result is not None:
                results.append(result)
        if results:
            return json_response(results)
        return empty_response()

    result = await handle_rpc(rpc, api_key, env)
    if result is None:
        return empty_response()
    return json_response(result)
