# (key): name in API --> (value): display name
APEX_MAPS = {
    "World's Edge": "World's Edge 🗺️",
    "Kings Canyon": "Kings Canyon 🏜️",
    "Olympus": "Olympus 🏙️",
    "Storm Point": "Storm Point ⛈️"
}

# number of queries in the API call (?next={...})
DEFAULT_COUNT = 3

# when to update the discord bot status (how many seconds to wait per update)
RATE_LIMIT_INT = 10

# when to force invalidate status and pull from API again (seconds)
FORCE_INVALIDATE_INT = 1800

##########################
### DO NOT TOUCH BELOW ###
##########################
DAY_UNIT = 86400
