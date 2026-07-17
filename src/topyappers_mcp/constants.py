"""Shared constants and schema enums for the TopYappers MCP Worker."""

API_BASE = "https://www.topyappers.com"
PROTOCOL_VERSION = "2025-03-26"
SERVER_NAME = "topyappers"
SERVER_VERSION = "1.0.0"

MCP_PATH = "/mcp"
DEFAULT_OAUTH_CLIENT_ID = "myapp-claude"
DEFAULT_SCOPE = "myapp:read"
TOKEN_EXPIRES_IN = 31536000
AUTH_CODE_TTL_SECONDS = 600

CATEGORIES = [
    "Arts", "Automotive", "Beauty & Personal Care", "Books & Literature",
    "Business", "Finance", "Career & Jobs", "Collectibles & Hobbies",
    "Community", "Ecommerce", "Crafts & DIY", "Culture", "Education",
    "Technology", "Entertainment", "Environment", "Family", "Parenting",
    "Fashion", "Film", "Fitness", "Health", "Food", "Gaming",
    "Gardening & Agriculture", "History", "Home", "Humor", "Law",
    "Government", "Lifestyle", "Marketing", "Mental Health", "Music",
    "News & Media", "Outdoors", "Nature", "Pets", "Animals",
    "Philosophy", "Spirituality", "Photography", "Videography", "Politics",
    "Relationships", "Religion", "Science", "Self-Improvement", "Shopping",
    "Social Media", "Social Issues & Activism", "Sports", "Travel",
    "Vehicles & Transportation", "Virtual Reality", "Weapons & Defense",
    "Writing", "Kids",
]

SOURCES = ["tiktok", "instagram", "youtube", "linkedin", "twitter"]
GENDERS = ["male", "female"]
RACES = [
    "latino hispanic", "middle eastern", "indian", "east asian",
    "white", "black", "southeast asian",
]
HAIR_COLORS = ["black", "brunette", "white", "blonde", "red"]
BODY_COMPLEXIONS = ["skinny", "ordinary", "overweight", "hulk"]
ACCOUNT_TYPES = ["faceless", "ugc", "agc", "clipper", "brand"]
PROMOTED_BUSINESS_TYPES = [
    "B2C apps", "B2B SaaS", "DTC brands", "Ecommerce products",
    "Fintech & banking", "Gaming", "Subscription services",
    "Online courses & info products", "Local services", "Marketplaces",
]
LANGUAGES = [
    "arabic", "bengali", "bosnian", "bulgarian", "cantonese", "catalan",
    "croatian", "czech", "danish", "dutch", "english", "estonian",
    "filipino", "finnish", "french", "german", "greek", "gujarati",
    "hausa", "hebrew", "hindi", "hungarian", "icelandic", "indonesian",
    "italian", "japanese", "javanese", "kannada", "kazakh", "korean",
    "latvian", "lithuanian", "malay", "malayalam", "mandarin", "marathi",
    "nepali", "norwegian", "pashto", "persian", "polish", "portuguese",
    "punjabi", "romanian", "russian", "serbian", "sinhala", "slovak",
    "slovenian", "somali", "spanish", "swahili", "swedish", "tamil",
    "telugu", "thai", "turkish", "ukrainian", "urdu", "uzbek",
    "vietnamese", "yoruba",
]
