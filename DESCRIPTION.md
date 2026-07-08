# TopYappers

Social media intelligence for AI agents. Access viral content discovery, influencer search across TikTok, Instagram & YouTube, trending song charts, and TopYappers outreach agent email history — all through a single MCP connection.

## What it does

TopYappers gives AI agents real-time access to social media data across three domains:

- **Viral Content** — Discover trending TikTok posts filtered by category, country, virality score (views÷followers), date range, music/sound, and opening hooks. Understand what's going viral and why.
- **Creators & Influencers** — Search a database of 30M+ creators across TikTok, Instagram, and YouTube using 20+ filters including AI-analyzed niches, promoted products, follower ranges, engagement rates, country, language, and hashtags. Creator search is free — you only pay when fetching full profiles.
- **Trending Songs** — Access weekly song chart rankings by country, track new chart entries, search by title or artist, view historical performance, and compare charts week-over-week.
- **Agent Outreach** — Inspect your own outreach projects, contacted creators, sent emails, and creator replies so AI can draft informed follow-ups from inbox context.

## Tools

| Tool | Description | Cost |
|------|-------------|------|
| `search_viral_content` | Find viral TikTok posts by category, country, views, virality score, dates, music, hooks | 1 credit/result |
| `search_creators` | Search influencers across TikTok, Instagram, YouTube with 20+ filters | **Free** |
| `get_creator_profiles` | Fetch full creator profiles — followers, engagement, email, bio, niches, promoted products | 1 credit/creator |
| `list_agent_projects` | List outreach projects and campaign context | **Free** |
| `list_contacted_creators` | List creators contacted via email, with reply and thread context | **Free** |
| `list_agent_messages` | List sent and received outreach emails by creator, project, thread, or direction | **Free** |
| `search_videos` | Search videos by engagement metrics, hashtags, text in descriptions | 1 credit/video |
| `get_song_rankings` | Country or global trending song chart rankings | 10 credits |
| `get_new_song_entries` | Newly charting songs that just entered rankings | 10 credits |
| `search_songs` | Search songs by title or artist name | 10 credits |
| `get_song_history` | Track a song's chart performance over time | 10 credits |
| `compare_song_rankings` | Compare song charts between two weeks | 10 credits |
| `get_song_countries` | List available countries for song data | 10 credits |
| `get_song_weeks` | List available weeks for a country | 10 credits |

## Use cases

- **Influencer marketing** — Find creators in specific niches who match a brand's target audience, with contact emails and engagement data
- **Content strategy** — Analyze what's going viral in your category to inform content creation
- **Trend monitoring** — Track trending songs and sounds before they peak, ideal for music marketing and content timing
- **Reply personalization** — Turn an inbox email into creator, campaign, thread, and prior-message context for better follow-ups
- **Competitive intelligence** — Discover which products competitors are promoting through influencers
- **Market research** — Understand engagement patterns across countries, categories, and platforms

## Key features

- **Credit-efficient design** — Creator search is free; agents find matching IDs first, then only fetch profiles for relevant creators
- **Rich filtering** — 20+ filters for creators including AI-analyzed `nichesToPromote` for semantic niche matching
- **Cross-platform** — Single interface for TikTok, Instagram, and YouTube data
- **Built-in agent guidance** — Includes detailed instructions and prompt templates to help agents use tools effectively
- **No data stored** — API keys are forwarded as Bearer tokens; nothing is stored on the server

## Authentication

Use `https://mcp.topyappers.com/mcp` as the hosted MCP connector URL.

For Claude Web/Desktop custom connectors, choose OAuth with client ID `myapp-claude` and use your TopYappers API key as the client secret. This OAuth flow is a connector shim: the API key becomes the MCP bearer access token.

Other MCP clients can pass the same API key as a Bearer token in the `Authorization` header. Get a key at [topyappers.com/profile](https://www.topyappers.com/profile).

## Links

- [TopYappers Platform](https://www.topyappers.com)
- [API Documentation](https://docs.topyappers.com)
- [MCP Documentation](https://www.topyappers.com/mcp)
- [GitHub](https://github.com/topyappers/topyappers-mcp)
