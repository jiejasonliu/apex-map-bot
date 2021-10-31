from discord import Game
from discord.ext import tasks
from discord.ext.commands import Cog

from .utils import maprotation as mapsutil
from .utils import constants as c


class StatusTask(Cog):
    def __init__(self, client):
        self.client = client
        self.map_last_fetch = None
        self.secs_last_fetch = 0

    @Cog.listener()
    async def on_ready(self):
        self.try_update_status.start()

    @tasks.loop(seconds=1.0)
    async def try_update_status(self):
        # get last fetched map unless cache is too old (sync purposes)
        if self.map_last_fetch and self.secs_last_fetch <= c.INVALIDATE_INT:
            currmap = self.map_last_fetch
        else:
            try:
                response = await mapsutil.getmaps(0)
                currmap = response[0]
                self.map_last_fetch = currmap
                self.secs_last_fetch = 0
            except Exception as err:
                print(err)
                return

        # build bot status (with rate limit)
        if self.secs_last_fetch % c.RATE_LIMIT_INT == 0:
            mapname = currmap.name
            secs_remaining = currmap.remaining.totalseconds - self.secs_last_fetch

            # need to update, map changed since last fetch
            if secs_remaining <= 0:
                self.map_last_fetch = None
                return

            timeunit = mapsutil.TimeUnit.from_seconds(secs_remaining)
            display = f"{mapname} ({timeunit.display_shorthand()})"
            await self.client.change_presence(activity=Game(name=display))

        # update seconds elapsed cache
        self.secs_last_fetch += 1


def setup(client):
    client.add_cog(StatusTask(client))
