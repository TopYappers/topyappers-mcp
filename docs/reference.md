# Reference — Enums & Values

All available enum values for API filters. Use these exact values in your requests.

## Categories

57 content categories for filtering creators and viral content. Use with `mainCategory` (creators) and `categories` (viral content).

```
Arts, Automotive, Beauty & Personal Care, Books & Literature, Business,
Finance, Career & Jobs, Collectibles & Hobbies, Community, Ecommerce,
Crafts & DIY, Culture, Education, Technology, Entertainment, Environment,
Family, Parenting, Fashion, Film, Fitness, Health, Food, Gaming,
Gardening & Agriculture, History, Home, Humor, Law, Government, Lifestyle,
Marketing, Mental Health, Music, News & Media, Outdoors, Nature, Pets,
Animals, Philosophy, Spirituality, Photography, Videography, Politics,
Relationships, Religion, Science, Self-Improvement, Shopping, Social Media,
Social Issues & Activism, Sports, Travel, Vehicles & Transportation,
Virtual Reality, Weapons & Defense, Writing, Kids
```

## Countries

143 countries for geographic filtering. Use full names with `country` (creators) and `countries` (viral content). Song tools use **country codes** instead — use `get_song_countries` to discover valid codes.

<details>
<summary>All 143 countries</summary>

```
United States, China, Japan, Germany, United Kingdom, India, France, Canada,
Italy, South Korea, Australia, Brazil, Spain, Mexico, Indonesia, Netherlands,
Saudi Arabia, Turkey, Switzerland, Taiwan, Poland, Sweden, Belgium, Thailand,
Argentina, Nigeria, Austria, Iran, Norway, United Arab Emirates, Ireland,
Israel, South Africa, Denmark, Singapore, Malaysia, Philippines, Hong Kong,
Colombia, Bangladesh, Egypt, Finland, Chile, Vietnam, Czechia, Romania,
New Zealand, Portugal, Greece, Iraq, Qatar, Peru, Hungary, Kuwait, Ukraine,
Morocco, Slovakia, Puerto Rico, Ecuador, Oman, Kenya, Luxembourg, Cuba,
Sri Lanka, Uzbekistan, Bulgaria, Croatia, Côte d'Ivoire, Belarus, Uruguay,
Panama, Slovenia, Turkmenistan, Lithuania, Lebanon, Tanzania, Jordan, Bahrain,
Serbia, Cameroon, Bolivia, Paraguay, Ghana, Estonia, Uganda, Zambia,
Afghanistan, Bosnia and Herzegovina, Mozambique, Armenia, Georgia, Honduras,
Albania, Madagascar, Namibia, Senegal, Malta, Chad, Niger, Mali, Kyrgyzstan,
Malawi, Rwanda, Burundi, Comoros, Lesotho, Tajikistan, Suriname, Montenegro,
Eswatini, Sierra Leone, Gambia, Guyana, Timor-Leste, Mauritania,
Burkina Faso, Liberia, Cape Verde, Mauritius, Bhutan, Benin,
Central African Republic, Togo, Guinea, Gabon, São Tomé and Príncipe,
Equatorial Guinea, Antigua and Barbuda, Belize, Barbados,
Saint Kitts and Nevis, Vanuatu, Solomon Islands,
Saint Vincent and the Grenadines, Fiji, Samoa, Tonga, Dominica,
Russia, Other
```

</details>

## Sources

Platform sources for creator and video filtering.

```
tiktok, instagram, youtube, twitch, linkedin, twitter (X/Twitter)
```

## Gender

```
male, female
```

## Languages

62 languages for filtering creators by primary content language.

<details>
<summary>All 62 languages</summary>

```
arabic, bengali, bosnian, bulgarian, cantonese, catalan, croatian, czech,
danish, dutch, english, estonian, filipino, finnish, french, german, greek,
gujarati, hausa, hebrew, hindi, hungarian, icelandic, indonesian, italian,
japanese, javanese, kannada, kazakh, korean, latvian, lithuanian, malay,
malayalam, mandarin, marathi, nepali, norwegian, pashto, persian, polish,
portuguese, punjabi, romanian, russian, serbian, sinhala, slovak, slovenian,
somali, spanish, swahili, swedish, tamil, telugu, thai, turkish, ukrainian,
urdu, uzbek, vietnamese, yoruba
```

</details>

## Hair Colors

```
Blonde hair, Brunette hair, Black hair, Red hair, White hair
```

## Races

```
White, Black, Indian, East Asian, Southeast Asian, Middle Eastern, Latino Hispanic
```

## Body Complexions

```
Skinny, Ordinary, Overweight, Hulk
```

## Country Format — Important Distinction

| Context | Format | Example |
|---------|--------|---------|
| Creators (`country`) | Full country name | `"United States"` |
| Viral content (`countries`) | Full country name | `["France", "Germany"]` |
| Song tools (`country`, `country_code`) | Country code | `"US"`, `"GB"`, `"FR"` |

Always use full names for creators and viral content. Always use codes for songs.
