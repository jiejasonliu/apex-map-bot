from discord.ext.commands import Cog
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

from .utils import maprotation as mapsutil
from .utils import constants as c


class WhenCommand(Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name='when', 
        description='Know when a specific Apex map is in rotation!',
        options=[
            create_option(
                name="option",
                description="Choose a map to query 🔍",
                required=True,
                option_type=3,
                choices=[
                    create_choice(name=v, value=k) for k,v in c.APEX_MAPS.items()
                ]
            )
        ]
    )
    async def _when(self, ctx, option):
        response = await mapsutil.getmaps(filter=option)
        result = await mapsutil.stringifymaps(response)
        await ctx.send(result)
    
def setup(client):
    client.add_cog(WhenCommand(client))