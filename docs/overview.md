# TopYappers MCP — How It Works

The TopYappers MCP server gives AI agents access to the [TopYappers API](https://docs.topyappers.com) through the Model Context Protocol. It covers four domains:

- **Viral Content** — discover viral TikTok posts with category, country, virality score, music, and hook filters
- **Creators / Influencers** — search and retrieve influencer profiles across TikTok, Instagram, and YouTube
- **Trending Songs** — chart rankings, new entries, song search, history, and week-over-week comparisons
- **Agent Outreach** — inspect your own outreach projects, contacted creators, sent emails, and replies

## Authentication

The MCP uses **Bearer token authentication**. Your TopYappers API key is passed as:

```
Authorization: Bearer <your-topyappers-api-key>
```

The server extracts it and forwards it to the TopYappers API as the `x-ty-api-key` header. No keys are stored on the server.

## Credits & Pricing

Some API calls cost credits. Your remaining balance is returned in the `x-ty-credits` response header.

| Tool | Cost |
|------|------|
| `search_creators` | **Free** |
| `get_creator_profiles` | 1 credit per creator |
| `list_agent_projects` | **Free** |
| `list_contacted_creators` | **Free** |
| `list_agent_messages` | **Free** |
| `search_viral_content` | 1 credit per returned result |
| `search_videos` | 1 credit per returned video |
| All song tools | 10 credits per request |

**Tip:** Always use `search_creators` (free) first to find creator IDs, then call `get_creator_profiles` only for the ones you actually need. Control costs by keeping `pageSize` / `perPage` small when exploring.

## Rate Limits

All endpoints are rate limited to **60 requests per minute** per API key.

When exceeded, you get an HTTP `429` response:

```json
{
  "error": "Too many requests",
  "retryAfter": 45
}
```

Response headers on every request:

| Header | Description |
|--------|-------------|
| `x-ty-credits` | Remaining credit balance |
| `x-ty-rate-limit-remaining` | Requests left in the current minute |
| `x-ty-rate-limit-total` | Total requests allowed per minute (default: 60) |

## Available Tools

| # | Tool | Method | Underlying Endpoint |
|---|------|--------|---------------------|
| 1 | `search_viral_content` | POST | `/api/v1/viral-content` |
| 2 | `search_creators` | GET | `/api/v2/creators/search` |
| 3 | `get_creator_profiles` | POST | `/api/v2/creators/get` |
| 4 | `list_agent_projects` | GET | `/api/v1/agent/projects` |
| 5 | `list_contacted_creators` | GET | `/api/v1/agent/contacted-creators` |
| 6 | `list_agent_messages` | GET | `/api/v1/agent/messages` |
| 7 | `search_videos` | GET | `/api/v1/videos` |
| 8 | `get_song_rankings` | GET | `/api/v1/songs?action=rankings` or `global` |
| 9 | `get_new_song_entries` | GET | `/api/v1/songs?action=new-entries` |
| 10 | `search_songs` | GET | `/api/v1/songs?action=search` |
| 11 | `get_song_history` | GET | `/api/v1/songs?action=song-history` |
| 12 | `compare_song_rankings` | GET | `/api/v1/songs?action=compare` |
| 13 | `get_song_countries` | GET | `/api/v1/songs?action=countries` |
| 14 | `get_song_weeks` | GET | `/api/v1/songs?action=weeks` |

See the individual docs for each domain:

- [Creators & Influencers](./creators.md)
- [Agent Outreach](./agent-outreach.md)
- [Viral Content](./viral-content.md)
- [Videos](./videos.md)
- [Trending Songs](./songs.md)
- [Reference — Enums & Values](./reference.md)
