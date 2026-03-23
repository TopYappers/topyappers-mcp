# TopYappers MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server deployed on **Cloudflare Workers** (Python) that gives AI agents access to the [TopYappers API](https://docs.topyappers.com) for discovering viral content, trending songs, and influencers.

## Features

| Tool | Description | Cost |
|------|-------------|------|
| `search_viral_content` | Find viral TikTok posts by category, country, views, virality score, dates, music, hooks | 1 credit/result |
| `search_creators` | Search influencers across TikTok, Instagram, YouTube with 20+ filters | **Free** |
| `get_creator_profiles` | Fetch full creator profiles by IDs | 1 credit/creator |
| `search_videos` | Search videos by engagement, hashtags, text | 1 credit/video |
| `get_song_rankings` | Country or global song chart rankings | 10 credits |
| `get_new_song_entries` | Newly charting songs for a country | 10 credits |
| `search_songs` | Search songs by title/artist | 10 credits |
| `get_song_history` | Song chart performance over time | 10 credits |
| `compare_song_rankings` | Compare charts between two weeks | 10 credits |
| `get_song_countries` | List available countries for song data | 10 credits |
| `get_song_weeks` | List available weeks for a country | 10 credits |

## Prerequisites

- [Cloudflare account](https://dash.cloudflare.com/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/) (`npm install -g wrangler`)
- [TopYappers API key](https://www.topyappers.com/profile)

## Deploy

### Manual

```bash
cd topyappers-mcp
npx wrangler login
npx wrangler deploy
```

### CI/CD (GitHub Actions)

Deploys automatically on every push to `main`. Set these repository secrets in **Settings → Secrets and variables → Actions**:

| Secret | Where to find it |
|--------|-----------------|
| `CLOUDFLARE_API_TOKEN` | [Cloudflare Dashboard → API Tokens](https://dash.cloudflare.com/profile/api-tokens) — create a token with **Edit Cloudflare Workers** permission |
| `CLOUDFLARE_ACCOUNT_ID` | [Cloudflare Dashboard → Workers & Pages → Overview](https://dash.cloudflare.com/) — shown in the right sidebar |

You can also trigger a deploy manually from the **Actions** tab using the "Run workflow" button.

After deploying, your MCP server will be available at:
```
https://topyappers-mcp.<your-subdomain>.workers.dev
```

### Custom Domain

To use a custom domain like `mcp.topyappers.com`:

1. Make sure the root domain (e.g. `topyappers.com`) is added as a zone in your Cloudflare account
2. In `wrangler.toml`, uncomment and edit the routes section:
   ```toml
   [[routes]]
   pattern = "mcp.topyappers.com"
   custom_domain = true
   ```
3. Deploy — Cloudflare will automatically create the DNS record and provision an SSL certificate
4. Alternatively, configure it in the Cloudflare Dashboard: **Workers & Pages → topyappers-mcp → Settings → Domains & Routes → Add → Custom Domain**

## Authentication

The MCP server uses **Bearer token authentication**. Clients pass their TopYappers API key as a Bearer token in the `Authorization` header. The server forwards it to the TopYappers API as the `x-ty-api-key` header.

Alternatively, you can set a default API key as a Cloudflare Worker secret:

```bash
npx wrangler secret put TOPYAPPERS_API_KEY
```

The server checks the `Authorization: Bearer` header first, then falls back to the `TOPYAPPERS_API_KEY` secret.

## MCP Client Configuration

### Cursor

Add to your Cursor MCP settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "topyappers": {
      "url": "https://topyappers-mcp.<your-subdomain>.workers.dev",
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
      "url": "https://topyappers-mcp.<your-subdomain>.workers.dev",
      "headers": {
        "Authorization": "Bearer YOUR_TOPYAPPERS_API_KEY"
      }
    }
  }
}
```

## Documentation

Detailed docs for each API domain:

- [**Overview** — how it works, auth, credits](./docs/overview.md)
- [**Creators & Influencers** — search workflow, parameters, power filters](./docs/creators.md)
- [**Viral Content** — filters, virality score, use cases](./docs/viral-content.md)
- [**Videos** — search, sort, engagement filters](./docs/videos.md)
- [**Trending Songs** — rankings, new entries, history, comparisons](./docs/songs.md)
- [**Reference** — all enums, countries, categories, languages](./docs/reference.md)

## Example Agent Workflows

### Find viral fitness content from the US

1. Agent calls `search_viral_content` with `categories: ["Fitness"]`, `countries: ["United States"]`, `viralityScoreMin: 0.5`
2. Gets back viral videos with engagement metrics and creator info

### Discover fashion influencers on Instagram

1. Agent calls `search_creators` with `source: "instagram"`, `mainCategory: "Fashion"`, `followersMin: 50000` (free)
2. Agent calls `get_creator_profiles` with the returned `userIds` (1 credit each)
3. Gets full profiles with email, bio, engagement rate, etc.

### Find trending songs in the UK

1. Agent calls `get_song_rankings` with `country: "GB"`
2. Gets the latest chart with song titles, artists, ranks, and movement
3. Optionally calls `get_song_history` for deeper analysis of a specific song

## Rate Limits

- **60 requests per minute** per API key
- HTTP 429 responses include `retryAfter` indicating seconds to wait

## Development

For local development/testing, you can use Wrangler's dev mode:

```bash
npx wrangler dev
```

This starts a local server at `http://localhost:8787` that you can point your MCP client to.
