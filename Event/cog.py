import discord
from textwrap import dedent
from discord.ext import commands
from .member_join import member_join
from .member_remove import membre_remove
from config import Type
import logging





logger = logging.getLogger(__name__)




class Event(commands.Cog):


    def __init__(self,bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_member_join(self,ctx,membre):
        await member_join(ctx,membre)
        
        

    @commands.Cog.listener()
    async def on_member_remove(self,ctx,membre):
        await membre_remove(ctx,membre)
        


async def setup(bot):
    logger.warning("Event cog _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ")
    await bot.add_cog(Event(bot))