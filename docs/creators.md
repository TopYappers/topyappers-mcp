# Creators & Influencers

Search for influencers and creators across TikTok, Instagram, and YouTube. This uses a **two-step workflow** to save credits.

## Workflow

1. **Search** creators with filters (FREE) → returns `userIds`
2. **Get** full profiles by passing those `userIds` → costs 1 credit per creator
3. **Paginate** using `page` and `perPage`

## Step 1: Search Creators (Free)

**Tool:** `search_creators`
**Endpoint:** `GET /api/v2/creators/search`
**Cost:** Free

Returns an array of creator IDs (e.g. `["instagram_57971538386", "tiktok_12345"]`) that you pass to Step 2.

### Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `followersMin` | integer | Minimum followers | `10000` |
| `followersMax` | integer | Maximum followers | `1000000` |
| `averageViewsMin` | integer | Minimum average views per post | `5000` |
| `averageViewsMax` | integer | Maximum average views per post | `500000` |
| `engagementRateMin` | number | Minimum engagement rate (%) | `2.5` |
| `engagementRateMax` | number | Maximum engagement rate (%) | `10` |
| `age` | string | Age group, comma-separated | `"20-29,30-39"` |
| `gender` | string | `"male"` or `"female"` | `"female"` |
| `mainCategory` | string | Content category ([see values](./reference.md#categories)) | `"Fashion"` |
| `subCategory` | string | Sub-category, free text | `"streetwear"` |
| `bio` | string | Keywords in creator's bio | `"tiktok shop"` |
| `promotedProducts` | string | Products creator promoted, comma-separated | `"beef tallow,feastables"` |
| `nichesToPromote` | string | AI-analyzed niches, comma-separated | `"SaaS,skincare"` |
| `country` | string | Full country name ([see values](./reference.md#countries)) | `"France"` |
| `source` | string | `"tiktok"`, `"instagram"`, or `"youtube"` | `"instagram"` |
| `username` | string | Creator handle | `"mrbeast"` |
| `language` | string | Content language ([see values](./reference.md#languages)) | `"english"` |
| `hashtags` | string | Hashtags, comma-separated (AND match) | `"fitness,gym"` |
| `emailExists` | boolean | Only creators with email available | `true` |
| `email` | string | Find by exact email | `"john@example.com"` |
| `page` | integer | Page number (default: 1) | `1` |
| `perPage` | integer | Results per page (default: 10, max: 100) | `20` |

### Example Response

```json
{
  "message": "OK",
  "params": { "page": 1, "perPage": 10 },
  "response": {
    "data": [
      "instagram_57971538386",
      "instagram_58848167468",
      "instagram_52172673568"
    ],
    "page": 1,
    "next_page": 2,
    "total_pages": 10000
  }
}
```

Use `next_page` and `total_pages` for pagination. When `next_page` is `0`, there are no more pages.

## Step 2: Get Creator Profiles

**Tool:** `get_creator_profiles`
**Endpoint:** `POST /api/v2/creators/get`
**Cost:** 1 credit per creator

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `userIds` | string[] | **Required.** Creator IDs from search results |

### Example Response

```json
{
  "data": [
    {
      "id": "instagram_57971538386",
      "username": "creator_handle",
      "followers": 120000,
      "averageViews": 45000,
      "engagementRate": 3.2,
      "age": "20-29",
      "gender": "female",
      "mainCategory": "fashion",
      "subCategory": "streetwear",
      "bio": "Fashion creator sharing streetwear fits",
      "promotedProducts": ["beef tallow"],
      "nichesToPromote": ["fashion", "streetwear"],
      "country": "France",
      "source": "instagram",
      "email": "creator@example.com",
      "language": "french",
      "hashtags": ["fashion", "streetwear", "ootd"]
    }
  ]
}
```

## Power Filters

### nichesToPromote

**This is the most powerful filter for finding relevant creators.** It's a free-text search against AI-analyzed niche data for each creator.

> **Important: AND matching.** When you pass multiple comma-separated values, ALL of them must match. This dramatically narrows results and can return zero hits. **Search one keyword at a time and combine results across multiple calls.** Since search is free, there's no credit cost.

**Do this:**
1. `nichesToPromote=skincare` → get results
2. `nichesToPromote=beauty` → get results
3. Combine/deduplicate the userIds from both calls

**Don't do this:**
- `nichesToPromote=skincare,beauty,wellness` → requires ALL three to match, likely returns very few or zero results

More examples of good single-keyword searches:
- `nichesToPromote=SaaS` — creators suited for promoting software products
- `nichesToPromote=skincare` — creators in the skincare space
- `nichesToPromote=fitness supplements` — creators who promote fitness products
- `nichesToPromote=meal prep` — food/health creators

Be creative with search terms — it's a discovery tool. Run multiple searches with different terms to cast a wider net.

### promotedProducts

Find creators who have promoted specific products. For example, `promotedProducts=Beef Tallow` returns all creators who mentioned this product. Great for finding creators experienced with products similar to yours.

> **Important: AND matching.** Same as `nichesToPromote` — multiple comma-separated values use AND logic. If you pass `promotedProducts=beef tallow,feastables`, only creators who promoted **both** products are returned. **Search one product at a time** and combine results for broader discovery.

### hashtags

Comma-separated, uses AND matching — all specified hashtags must be present in the creator's content. The `#` prefix is optional and stripped automatically.

> **Important: AND matching applies here too.** `hashtags=fitness,gym` only returns creators who use BOTH #fitness AND #gym. For broader results, search one hashtag per call and merge the results.

### General tip for all AND filters

Since `search_creators` is **free**, the best strategy is always:

1. Run multiple narrow searches with **one keyword each**
2. Collect all `userIds` from every search
3. Deduplicate the combined list
4. Call `get_creator_profiles` once with the merged IDs

This gives you the broadest coverage without missing creators who match only some of your keywords.
