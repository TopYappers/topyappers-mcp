"""Instructions exposed to MCP clients during initialization."""

INSTRUCTIONS = """# TopYappers MCP — Agent Guide

You have access to the TopYappers API through this MCP server. It lets you discover **viral content**, **trending songs**, and **influencers/creators** across TikTok, Instagram, and YouTube. It also lets you inspect your own **outreach agent projects and email history** so you can reason about creator replies with context.

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

**Step 1 — Search (FREE):** Call `search_creators` with filters. This returns creator IDs, not full profiles.

**Start with `nichesToPromote`** — the primary discovery filter. It uses AI-analyzed niche data that is very granular. Think specific products and use cases, not broad categories:
- `nichesToPromote=calorie counter` — calorie tracking / diet apps
- `nichesToPromote=ai tools` — AI and productivity tools
- `nichesToPromote=standing desk` — office / ergonomics products
- `nichesToPromote=budget travel` — travel on a budget
- `nichesToPromote=new moms` — parenting / baby products
- `nichesToPromote=protein powder` — fitness supplements
- `nichesToPromote=Shopify` — ecommerce creators

Then narrow with additional filters:
- `source` — "tiktok", "instagram", "youtube", "linkedin", or "twitter" (X/Twitter)
- `country` — full country name (e.g. "France", "United States")
- `followersMin` / `followersMax` — follower range
- `averageViewsMin` / `averageViewsMax` — average post/video view range; use `averageViewsMin: 100000` for "100k+ views"
- `engagementRateMin` — percentage (e.g. 2.5 for 2.5%)
- `gender` — "male" or "female"; use `female` for women
- `race` — ethnicity/race; use `latino hispanic` for Latino, Latina, or Hispanic requests
- `language` — lowercase (e.g. "english", "spanish", "french")
- `emailExists` — set `true` to only get creators with contact email
- `mainCategory` — broad category like "Fashion", "Technology" (use only when nichesToPromote isn't specific enough)
- `bio` — keyword search in bio text
- `keywords` — general keyword search across searchable creator fields; comma-separated terms are OR-searched
- `hashtags` — AND matching, search one at a time

**CRITICAL — AND matching for nichesToPromote, promotedProducts, and hashtags:**
These fields use AND logic when comma-separated. Passing `nichesToPromote=skincare,beauty` only returns creators matching BOTH terms, which can return zero results. **Always search ONE keyword at a time** and combine the userIds from multiple searches. Since search is free, run 5+ narrow searches with different keywords to cast the widest net:

Example for a calorie counting app:
1. `nichesToPromote=calorie counter` → collect userIds
2. `nichesToPromote=calorie tracking` → collect userIds
3. `nichesToPromote=weight loss` → collect userIds
4. `nichesToPromote=meal prep` → collect userIds
5. `nichesToPromote=fitness nutrition` → collect userIds
6. Deduplicate and pass the merged list to `get_creator_profiles`

The niche data is very granular — it understands specific products, use cases, and sub-niches. Be creative with search terms: `calorie counter`, `ai tools`, `standing desk`, `budget travel`, `study tips`, `new moms`, etc.

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

## 5. Agent Outreach Messages

Use these tools when the user asks about messages sent by the TopYappers outreach agent, creators who replied, or how to respond to an email in their inbox.

**Common workflow for an inbox reply:**
1. Call `list_contacted_creators` with `creatorEmail` set to the email address from the inbox.
2. Call `list_agent_messages` with the same `creatorEmail` and `direction: "all"` to retrieve sent emails and inbound replies.
3. Call `list_agent_projects` if you need to map `project_id` to campaign details, target audience, deal terms, or custom outreach instructions.
4. Optionally call `search_creators` with `email` or `get_creator_profiles` with the returned `creator_id` if you need public creator profile data.

**Important:** `list_agent_messages` returns plain-text bodies. Use the newest inbound message plus the earlier outbound context to draft a specific reply. These outreach tools are free and do not consume credits.

## Credit costs summary

| Tool | Cost |
|------|------|
| search_creators | FREE |
| get_creator_profiles | 1 credit per creator |
| list_agent_projects | FREE |
| list_contacted_creators | FREE |
| list_agent_messages | FREE |
| search_viral_content | 1 credit per result |
| search_videos | 1 credit per video |
| All song tools | 10 credits per request |

## Tips for agents

- **Always start with nichesToPromote:** The primary filter for creator discovery. It uses AI-analyzed niche data that is very granular — specific products (`calorie counter`, `standing desk`), use cases (`meal prep`, `budget travel`), audiences (`new moms`, `college students`), and tools (`ChatGPT`, `Notion`, `Shopify`). Think specific, not broad.
- **Run 5+ niche searches per query:** nichesToPromote is an AND filter. Always search ONE keyword per call and run at least 5 searches with different keywords describing the target from different angles. For a skincare brand: `skincare`, `beauty routine`, `skin health`, `anti aging`, `dermatology`. Merge and deduplicate all results. Search is free.
- **Prefer nichesToPromote over mainCategory:** mainCategory is broad (e.g. "Technology" returns millions). nichesToPromote is granular (e.g. "ai tools" or "calorie counter" returns targeted results). Use mainCategory only as a fallback when you can't think of specific niche terms.
- **Be credit-efficient:** Start with `search_creators` (free) before calling `get_creator_profiles`. Use smaller `pageSize` / `perPage` when exploring.
- **Combine filters wisely:** Mix nichesToPromote with followers + country + source for targeted results, but always keep nichesToPromote to a single keyword per call.
- **Virality score:** A video with 1M views from a creator with 10K followers (score ~1.0) is far more impressive than 1M views from someone with 10M followers (score ~0.1).
- **Country format matters:** Viral content and creators use full names ("United States"). Songs use codes ("US").
"""
