# Videos

Search for video content from creators across TikTok, Instagram, and YouTube. Filter by engagement metrics, hashtags, text search, and sort results.

## Tool: `search_videos`

**Endpoint:** `GET /api/v1/videos`
**Cost:** 1 credit per returned video

## Parameters

All parameters are optional. Combine filters to narrow results.

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `userHandle` | string | Filter by specific creator handle | `"mrbeast"` |
| `userFollowersMin` | integer | Minimum creator followers | `10000` |
| `userFollowersMax` | integer | Maximum creator followers | `1000000` |
| `viewsMin` | integer | Minimum video views | `5000` |
| `viewsMax` | integer | Maximum video views | `500000` |
| `likesMin` | integer | Minimum likes | `100` |
| `likesMax` | integer | Maximum likes | `50000` |
| `commentsMin` | integer | Minimum comments | `10` |
| `commentsMax` | integer | Maximum comments | `5000` |
| `sharesMin` | integer | Minimum shares | `5` |
| `sharesMax` | integer | Maximum shares | `1000` |
| `hashtags` | string | Hashtags, comma-separated | `"fashion,streetwear,ootd"` |
| `textSearch` | string | Keywords in description/caption | `"workout routine"` |
| `sortBy` | string | Sort field: `"views"`, `"likes"`, `"shares"`, `"user_followers"` | `"views"` |
| `sortOrder` | string | `"desc"` (default) or `"asc"` | `"desc"` |
| `page` | integer | Page number (default: 1) | `1` |
| `perPage` | integer | Results per page (default: 20, max: 100) | `20` |

## Example Response

```json
{
  "data": [
    {
      "iv_id": "vid_abc123",
      "user_id": "12345",
      "user_handle": "fitness_creator",
      "video_id": "7123456789",
      "source": "tiktok",
      "comments": 342,
      "description": "5 minute morning workout routine #fitness #gym #workout",
      "hashtags": ["fitness", "gym", "workout"],
      "likes": 15200,
      "shares": 890,
      "subtitles": null,
      "user_followers": 85000,
      "views": 450000,
      "date_created_timestamp": 1710547200
    }
  ],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 1500,
    "totalPages": 75
  }
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `iv_id` | string | Internal video identifier |
| `user_id` | string | Platform user identifier |
| `user_handle` | string | Creator handle/username |
| `video_id` | string | Platform video identifier |
| `source` | string | `"tiktok"`, `"instagram"`, or `"youtube"` |
| `comments` | integer | Comment count |
| `description` | string | Video caption/description |
| `hashtags` | string[] | Associated hashtags |
| `likes` | integer | Like count |
| `shares` | integer | Share count |
| `subtitles` | array or null | Subtitle data if available |
| `user_followers` | integer | Creator's follower count |
| `views` | integer | View count |
| `date_created_timestamp` | number | Unix timestamp (seconds) |

## Use Cases

### Find a specific creator's top videos

```json
{
  "userHandle": "creator_name",
  "sortBy": "views",
  "sortOrder": "desc",
  "perPage": 10
}
```

### Find high-engagement videos in a niche

```json
{
  "hashtags": "skincare,routine",
  "viewsMin": 100000,
  "likesMin": 5000,
  "sortBy": "likes",
  "sortOrder": "desc"
}
```

### Search videos by topic

```json
{
  "textSearch": "morning routine",
  "viewsMin": 50000,
  "sortBy": "views",
  "sortOrder": "desc",
  "perPage": 20
}
```

### Find viral videos from small creators

```json
{
  "userFollowersMax": 50000,
  "viewsMin": 500000,
  "sortBy": "views",
  "sortOrder": "desc"
}
```
