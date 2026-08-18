
from discord import app_commands
from discord.ext import commands
import logging
from services.Rechercher.convert_type import convert_type
from utils.eumu import Ouiounon

logger = logging.getLogger(__name__)
class Teste(commands.Cog):
    def __int__(self,bot):
        self.bot = bot

    @commands.hybrid_command(name = "teste", description="commade de teste")
    @app_commands.describe(texte = "Pour teste la fonction recherhe")
    async def teste(self ,ctx ,texte : str, etendre: Ouiounon = Ouiounon.NON):
        liste = await convert_type(ctx, texte , etendre)
        for index , membre in enumerate(liste , start=1):
            await ctx.send(f"{membre.mention} tu a éte trouver , trouver index et le : {index}")

    @commands.hybrid_command(name= "pingtoo")
    async def ping(self, ctx):
        await ctx.send("Pong ➡️✅")

    
async def setup(bot):
    await bot.add_cog(Teste(bot))