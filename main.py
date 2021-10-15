import os

from discord import Activity, ActivityType, Game, Intents
from discord.ext import tasks
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from keep_alive import keep_alive

from cogs.utils import maprotation as mapsutil
from cogs.utils import constants as c

default_activity = Activity(type=ActivityType.watching, name="jdawg's server 😈")
client = Bot(command_prefix="!", activity=default_activity, intents=Intents.default())
slash = SlashCommand(client, sync_commands=True)


# runs when bot is online
@client.event
async def on_ready():
    print(f'Online: {client.user}')
    try_update_status.start()


# map status cache
map_last_fetch = None
secs_last_fetch = 0

@tasks.loop(seconds=1.0)
async def try_update_status():
    global map_last_fetch, secs_last_fetch

    # get last fetched map if cache is too old (sync purposes)
    if map_last_fetch and secs_last_fetch <= c.INVALIDATE_INT:
        currmap = map_last_fetch
    else:
        response = await mapsutil.getmaps(0)
        currmap = response[0]
        map_last_fetch = currmap
        secs_last_fetch = 0

    # build bot status (with rate limit)
    if secs_last_fetch % c.STATUS_INT == 0:
        mapname = currmap.name
        secs_remaining = currmap.remaining.totalseconds - secs_last_fetch
        timeunit = mapsutil.TimeUnit.from_seconds(secs_remaining)
        display = f"{mapname} ({timeunit.display_shorthand()})"
        await client.change_presence(activity=Game(name=display))

    # update seconds elapsed cache
    secs_last_fetch = secs_last_fetch + 1


# load all cogs when bot starts
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  # strip '.py'
        print('Loaded cog:', filename)

keep_alive()
client.run(os.getenv('TOKEN'))
