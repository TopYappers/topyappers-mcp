# TopYappers MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that gives AI agents access to the [TopYappers API](https://docs.topyappers.com) for discovering viral content, trending songs, influencers, and outreach agent email history.

## Available Tools

| Tool | Description | Cost |
|------|-------------|------|
| `search_viral_content` | Find viral TikTok posts by category, country, views, virality score, dates, music, hooks | 1 credit/result |
| `search_creators` | Search influencers across TikTok, Instagram, YouTube with 20+ filters | **Free** |
| `get_creator_profiles` | Fetch full creator profiles by IDs | 1 credit/creator |
| `list_agent_projects` | List outreach agent projects and campaign context | **Free** |
| `list_contacted_creators` | List creators contacted via agent email, with reply/thread context | **Free** |
| `list_agent_messages` | List sent and received outreach emails by creator, project, thread, or direction | **Free** |
| `search_videos` | Search videos by engagement, hashtags, text | 1 credit/video |
| `get_song_rankings` | Country or global song chart rankings | 10 credits |
| `get_new_song_entries` | Newly charting songs for a country | 10 credits |
| `search_songs` | Search songs by title/artist | 10 credits |
| `get_song_history` | Song chart performance over time | 10 credits |
| `compare_song_rankings` | Compare charts between two weeks | 10 credits |
| `get_song_countries` | List available countries for song data | 10 credits |
| `get_song_weeks` | List available weeks for a country | 10 credits |

## Getting Started

1. Get a TopYappers API key at [topyappers.com/profile](https://www.topyappers.com/profile)
2. Add the MCP server to your client (see below)

## Setup

### Claude Code (CLI)

```bash
claude mcp add --transport http topyappers https://mcp.topyappers.com \
  --header "Authorization: Bearer YOUR_TOPYAPPERS_API_KEY"
```

Or add to `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "topyappers": {
      "type": "http",
      "url": "https://mcp.topyappers.com",
      "headers": {
        "Authorization": "Bearer YOUR_TOPYAPPERS_API_KEY"
      }
    }
  }
}
```

### Cursor

Add to your MCP settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "topyappers": {
      "url": "https://mcp.topyappers.com",
      "headers": {
        "Authorization": "Bearer YOUR_TOPYAPPERS_API_KEY"
      }
    }
  }
}
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%/Claude/claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "topyappers": {
      "url": "https://mcp.topyappers.com",
      "headers": {
        "Authorization": "Bearer YOUR_TOPYAPPERS_API_KEY"
      }
    }
  }
}
```

## Authentication

Pass your TopYappers API key as a Bearer token in the `Authorization` header. The server forwards it to the TopYappers API — no keys are stored on the server.

## Documentation

Detailed docs for each API domain:

- [**Overview** — how it works, auth, credits](./docs/overview.md)
- [**Creators & Influencers** — search workflow, parameters, power filters](./docs/creators.md)
- [**Agent Outreach** — projects, contacted creators, sent messages, replies](./docs/agent-outreach.md)
- [**Viral Content** — filters, virality score, use cases](./docs/viral-content.md)
- [**Videos** — search, sort, engagement filters](./docs/videos.md)
- [**Trending Songs** — rankings, new entries, history, comparisons](./docs/songs.md)
- [**Reference** — all enums, countries, categories, languages](./docs/reference.md)

## Example Workflows

### Find viral fitness content from the US

1. Call `search_viral_content` with `categories: ["Fitness"]`, `countries: ["United States"]`, `viralityScoreMin: 0.5`
2. Get back viral videos with engagement metrics and creator info

### Discover fashion influencers on Instagram

1. Call `search_creators` with `source: "instagram"`, `mainCategory: "Fashion"`, `followersMin: 50000` (free)
2. Call `get_creator_profiles` with the returned `userIds` (1 credit each)
3. Get full profiles with email, bio, engagement rate, etc.

### Find trending songs in the UK

1. Call `get_song_rankings` with `country: "GB"`
2. Get the latest chart with song titles, artists, ranks, and movement
3. Call `get_song_history` for deeper analysis of a specific song

### Draft a reply to a creator who emailed back

1. Call `list_contacted_creators` with `creatorEmail: "creator@example.com"`
2. Call `list_agent_messages` with the same `creatorEmail` and `direction: "all"`
3. Use the original pitch, follow-ups, inbound reply, and project details to draft a customized response

## Rate Limits

- **60 requests per minute** per API key
- HTTP 429 responses include `retryAfter` indicating seconds to wait

## Links

- [TopYappers Platform](https://www.topyappers.com)
- [API Documentation](https://docs.topyappers.com)
- [Get an API Key](https://www.topyappers.com/profile)
