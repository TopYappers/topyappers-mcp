# Viral Content

Discover and analyze viral TikTok content. Filter by categories, countries, view counts, virality scores, date ranges, music, and opening hooks.

## Tool: `search_viral_content`

**Endpoint:** `POST /api/v1/viral-content`
**Cost:** 1 credit per returned result

## Parameters

All parameters are optional. Combine multiple filters for targeted results.

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `categories` | string[] | Content categories ([see values](./reference.md#categories)) | `["Fitness", "Food"]` |
| `countries` | string[] | Full country names ([see values](./reference.md#countries)) | `["United States", "France"]` |
| `viewsMin` | integer | Minimum views | `100000` |
| `viewsMax` | integer | Maximum views | `10000000` |
| `viralityScoreMin` | number | Minimum virality score (0–1) | `0.5` |
| `viralityScoreMax` | number | Maximum virality score (0–1) | `1.0` |
| `followersMin` | integer | Minimum creator followers | `1000` |
| `followersMax` | integer | Maximum creator followers | `1000000` |
| `dateCreatedFrom` | string | Posts on or after this date (YYYY-MM-DD) | `"2024-01-01"` |
| `dateCreatedTo` | string | Posts on or before this date (YYYY-MM-DD) | `"2024-12-31"` |
| `musicTitle` | string | Music/sound title (case-insensitive partial match) | `"original sound"` |
| `hook` | string | Video opening hook text (case-insensitive partial match) | `"wait for it"` |
| `page` | integer | Page number (default: 1) | `1` |
| `pageSize` | integer | Results per page (default: 12, max: 100) | `12` |

## Understanding Virality Score

The virality score is calculated as **views ÷ followers**, normalized to a 0–1 range. It measures how well a video performed relative to the creator's audience size.

| Score | Meaning |
|-------|---------|
| 0.0–0.2 | Normal performance |
| 0.2–0.5 | Above average — good engagement |
| 0.5–0.8 | Highly viral — significant reach beyond followers |
| 0.8–1.0 | Extremely viral — massive breakout content |

A video with 1M views from a creator with 10K followers (high virality) is far more notable than 1M views from someone with 10M followers (low virality). Use `viralityScoreMin: 0.3` for quality results, `0.5` for highly viral only.

## Example Response

```json
{
  "message": "OK",
  "params": {
    "categories": ["Music"],
    "countries": ["United States"],
    "viewsMin": 10000,
    "viralityScoreMin": 0.5,
    "page": 1,
    "pageSize": 12
  },
  "response": {
    "data": [
      {
        "id": "post_abc123",
        "videoUrl": "https://...",
        "thumbnailUrl": "https://...",
        "caption": "This song is stuck in my head 🎵",
        "views": 2500000,
        "likes": 180000,
        "comments": 4200,
        "shares": 25000,
        "viralityScore": 0.83,
        "followers": 3000,
        "category": "Music",
        "country": "United States",
        "musicTitle": "original sound - artist_name",
        "creatorUsername": "creator123",
        "hook": "You need to hear this",
        "createdAt": "2024-06-15T14:30:00Z"
      }
    ],
    "page": 1,
    "pageSize": 12,
    "totalPages": 100,
    "totalResults": 1200
  }
}
```

## Use Cases

### Find viral content in a niche

```json
{
  "categories": ["Fitness"],
  "viralityScoreMin": 0.5,
  "pageSize": 10
}
```

### Find viral posts using a trending sound

```json
{
  "musicTitle": "original sound",
  "viewsMin": 500000,
  "pageSize": 20
}
```

### Find viral content from small creators

```json
{
  "followersMax": 50000,
  "viralityScoreMin": 0.7,
  "viewsMin": 100000,
  "pageSize": 10
}
```

### Find viral content with strong hooks

```json
{
  "hook": "wait for it",
  "viralityScoreMin": 0.3,
  "pageSize": 12
}
```

### Find recent viral content in a country

```json
{
  "countries": ["United Kingdom"],
  "dateCreatedFrom": "2026-01-01",
  "viewsMin": 100000,
  "pageSize": 15
}
```
