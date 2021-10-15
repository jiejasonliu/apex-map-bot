import os

from discord import Activity, ActivityType, Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from keep_alive import keep_alive

default_activity = Activity(type=ActivityType.watching,
                            name="jdawg's server 😈")
client = Bot(command_prefix="!",
             activity=default_activity,
             intents=Intents.default())
slash = SlashCommand(client, sync_commands=True)


# runs when bot is online
@client.event
async def on_ready():
    print(f'Online: {client.user}')


# load all cogs when bot starts
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  # strip '.py'
        print('Loaded cog:', filename)

keep_alive()
client.run(os.getenv('TOKEN'))
