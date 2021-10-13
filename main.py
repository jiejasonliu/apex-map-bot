import os

from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

client = Bot(command_prefix="!", intents=Intents.default())
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():   
    print(f'Online: {client.user}')   
    
# reload cogs
@client.command()
async def reload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            extension = f'cogs.{filename[:-3]}' # strip '.py'
            client.unload_extension(extension)
            client.load_extension(extension)
            print('Reloaded cog:', filename)

# load all cogs when bot starts
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') # strip '.py'
        print('Loaded cog:', filename)

client.run(os.getenv('TOKEN'))
