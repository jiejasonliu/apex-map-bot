import os

from discord import Activity, ActivityType, Game, Intents
from discord.ext import tasks
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from keep_alive import keep_alive
from replit import db

from cogs.utils import maprotation as mapsutil
from cogs.utils import constants as c

activity = Activity(type=ActivityType.watching, name="jdawg's server 😈")
client = Bot(command_prefix="!", activity=activity, intents=Intents.default())
slash = SlashCommand(client, sync_commands=True)


# runs when bot is online
@client.event
async def on_ready():
    print(f'Online: {client.user}')
    try_update_status.start()


# status update of current map
map_last_fetch = None


@tasks.loop(seconds=1.0)
async def try_update_status():
    global map_last_fetch

    # initialize secs last fetch cache
    if db.get('SECS_LAST_FETCH') == None:
        db['SECS_LAST_FETCH'] = 0

    # get last fetched map if cache is too old (sync purposes)
    if map_last_fetch and db.get('SECS_LAST_FETCH') <= c.INVALIDATE_INT:
        currmap = map_last_fetch
    else:
        response = await mapsutil.getmaps(0)
        currmap = response[0]
        map_last_fetch = currmap
        db['SECS_LAST_FETCH'] = 0

    # build bot status (with rate limit)
    if db['SECS_LAST_FETCH'] % c.STATUS_INT == 0:
        mapname = currmap.name
        secs_remaining = currmap.remaining.totalseconds - db['SECS_LAST_FETCH']
        timeunit = mapsutil.TimeUnit.from_seconds(secs_remaining)
        display = f"{mapname} ({timeunit.display_shorthand()})"
        await client.change_presence(activity=Game(name=display))

    # update seconds elapsed cache
    db['SECS_LAST_FETCH'] = db['SECS_LAST_FETCH'] + 1


# load all cogs when bot starts
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  # strip '.py'
        print('Loaded cog:', filename)

keep_alive()
client.run(os.getenv('TOKEN'))
