"""Tool registry for the TopYappers MCP server."""

from . import (
    compare_song_rankings,
    get_creator_profiles,
    get_new_song_entries,
    get_song_countries,
    get_song_history,
    get_song_rankings,
    get_song_weeks,
    list_agent_messages,
    list_agent_projects,
    list_contacted_creators,
    search_creators,
    search_songs,
    search_videos,
    search_viral_content,
)

TOOL_MODULES = [
    search_viral_content,
    search_creators,
    get_creator_profiles,
    list_agent_projects,
    list_contacted_creators,
    list_agent_messages,
    search_videos,
    get_song_rankings,
    get_new_song_entries,
    search_songs,
    get_song_history,
    compare_song_rankings,
    get_song_countries,
    get_song_weeks,
]

TOOLS = [module.TOOL for module in TOOL_MODULES]
TOOL_HANDLERS = {module.TOOL["name"]: module.handle for module in TOOL_MODULES}

PUBLIC_TOOLS = set()

