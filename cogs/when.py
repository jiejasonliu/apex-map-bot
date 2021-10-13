import json
import requests

from discord.ext import commands
from discord.ext.commands import Cog
from discord_slash import cog_ext

class WhenCommand(Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name='when', description='Know when a specific Apex map is in rotation!')
    async def _when(self, ctx):
        _ = await get_maps()
        await ctx.send('pong')

def setup(client):
    client.add_cog(WhenCommand(client))

class CurrentMap:
    def __init__(self, name, remaining):
        self.name = name
        self.remaining = remaining # TimeUnit

class NextMap:
    def __init__(self, name, timestamp, duration):
        self.name = name
        self.timestamp = timestamp
        self.duration = duration


class TimeUnit:
    def __init__(self, h=0, m=0, s=0):
        self.hours = h
        self.minutes = m
        self.seconds = s

# returns a tuple of (CurrentMap, NextMap[] <of length count>)
async def get_maps(count=3):
    try:
        response = requests.get(f"https://fn.alphaleagues.com/v2/apex/map/?next={count}")
        json_data = json.loads(response.text)
        
        # filter out "br" only (i.e. ignore "arenas" and other gamemodes)
        json_br = json_data['br']

        # generate Current Map
        name = json_br['map']
        totalseconds = json_br['times']['remaining']['seconds'] # e.g. 3555
        minutes = totalseconds // 60
        seconds = totalseconds % 60
        currmap = CurrentMap(name, TimeUnit(m=minutes, s=seconds))

        # generate Next Map objects
        nextmaps = []
        for j in json_br['next']:
            nextmap = NextMap(j['map'], j['timestamp'], j['duration'])
            nextmaps.append(nextmap)

        return (currmap, nextmaps)

    except Exception as e:
        print(e)
        return None