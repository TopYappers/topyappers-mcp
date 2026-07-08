"""Reusable MCP prompt templates."""

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
    {
        "name": "creator_reply_context",
        "description": (
            "Look up outreach history for a creator email and prepare context "
            "for a customized reply."
        ),
        "arguments": [
            {
                "name": "creator_email",
                "description": "The creator's email address from the inbox",
                "required": True,
            },
        ],
    },
]


def render_prompt(name, arguments):
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

    if name == "creator_reply_context":
        creator_email = args.get("creator_email", "")
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": (
                        f"Prepare reply context for creator email '{creator_email}':\n\n"
                        f"1. Call list_contacted_creators with creatorEmail: '{creator_email}'.\n"
                        f"2. Call list_agent_messages with creatorEmail: '{creator_email}', "
                        f"direction: 'all', perPage: 50.\n"
                        f"3. Call list_agent_projects if you need to map any project_id to campaign "
                        f"details, deal terms, or custom instructions.\n"
                        f"4. Summarize the relationship so far: original pitch, follow-ups, "
                        f"creator replies, open questions, and likely next best response.\n"
                        f"5. Draft a concise customized reply that references the actual context."
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

