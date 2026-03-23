# Trending Songs

Access trending songs data, chart rankings, and historical performance across different countries and time periods. All song tools cost **10 credits per request**.

## Important: Country Codes

Song tools use **country codes** (e.g. `"US"`, `"GB"`, `"FR"`), NOT full country names. Use `get_song_countries` to discover valid codes.

## Important: Week Format

Weeks use ISO format: `YYYY-Www`

- `YYYY` — four-digit year
- `W` — literal letter "W"
- `ww` — two-digit week number (01–53)

Examples: `"2026-W01"`, `"2026-W04"`, `"2025-W52"`

Use `get_song_weeks` with a country code to discover available weeks.

---

## Tools

### get_song_rankings

Get trending song chart rankings for a specific country or globally.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country` | string | Country code (e.g. `"US"`, `"GB"`). Omit for global. |
| `global_rankings` | boolean | Set `true` for worldwide rankings |
| `week` | string | Week in ISO format. Omit for latest data. |

**Example — US rankings for a specific week:**

```json
{ "country": "US", "week": "2026-W04" }
```

**Example — latest global rankings:**

```json
{ "global_rankings": true }
```

**Response format:**

```json
{
  "message": "OK",
  "action": "rankings",
  "credits_used": 10,
  "response": {
    "data": [
      {
        "id": "song_123",
        "title": "Song Title",
        "artist": "Artist Name",
        "rank": 1,
        "previous_rank": 3,
        "weeks_on_chart": 5,
        "peak_rank": 1
      }
    ]
  }
}
```

---

### get_new_song_entries

Songs that newly entered the chart for a country.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country` | string | **Required.** Country code |

```json
{ "country": "US" }
```

---

### search_songs

Search for songs by title or artist name.

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | **Required.** Search query — song title or artist |

```json
{ "q": "Taylor Swift" }
```

---

### get_song_history

Full chart performance history of a specific song over time.

| Parameter | Type | Description |
|-----------|------|-------------|
| `song_id` | string | **Required.** Song ID (from rankings or search) |
| `country_code` | string | **Required.** Country code |

```json
{ "song_id": "123456", "country_code": "US" }
```

---

### compare_song_rankings

Compare chart rankings between two different weeks.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country` | string | **Required.** Country code |
| `week1` | string | **Required.** First week (ISO format) |
| `week2` | string | **Required.** Second week (ISO format) |

```json
{ "country": "US", "week1": "2026-W03", "week2": "2026-W04" }
```

---

### get_song_countries

Get the list of available countries and their codes. No parameters required.

```json
{}
```

---

### get_song_weeks

Get available weeks for a specific country.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country_code` | string | **Required.** Country code |

```json
{ "country_code": "US" }
```

---

## Common Workflows

### Get current trending songs in a country

1. `get_song_rankings` with `country: "US"` (omit `week` for latest)
2. Review the top songs, their ranks, and weeks on chart

### Discover what's new on the charts

1. `get_new_song_entries` with `country: "US"`
2. See which songs just entered the rankings

### Track a song's performance

1. `search_songs` with `q: "song name"` to find the `song_id`
2. `get_song_history` with `song_id` and `country_code` to see rank over time

### Analyze week-over-week chart movement

1. `get_song_weeks` with `country_code: "US"` to find available weeks
2. `compare_song_rankings` with the two most recent weeks
3. Identify biggest movers, new entries, and exits

### Generate a full trending report

1. `get_song_rankings` — current top songs
2. `get_new_song_entries` — fresh entries
3. `compare_song_rankings` — movement vs last week
4. Compile insights: dominant artists, genre trends, risers/fallers
