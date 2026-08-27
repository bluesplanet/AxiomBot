from discord.ext import commands
from discord import app_commands
import discord
from utils.send import send_message
from Event.Data.Databasse import set
from config import Durations,Colors




class Config(commands.Cog):
    def __init__(self,bot):
        self.bot = bot




    @commands.hybrid_command(name="config_welcome",description="Configure le salon utilisé pour les messages de bienvenue.")
    @app_commands.describe(channel="Le salon où les messages de bienvenue seront envoyés.")
    async def config_welcom(self,ctx,channel : discord.TextChannel ):
        resultat = set(ctx.guild.id,welcome_channel_id=channel.id)

        if resultat:
            message = (
                f"✅ Le salon de bienvenue a été configuré sur {channel.mention}."
            )
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)

        else:
            message = "❌ Impossible de configurer le salon de bienvenue."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)




    @commands.hybrid_command(name="config_bey",description="Configure le salon utilisé pour les messages de bienvenue.")
    @app_commands.describe(channel = "Configure le salon utilisé pour les messages de départ.")
    async def config_bey(self,ctx,channel : discord.TextChannel ):

        resultat = set(ctx.guild.id,bey_channel_id=channel.id)

        if resultat:
            message = (f"✅ Le salon de départ a été configuré sur {channel.mention}.")
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)

        else:
            message = "❌ Impossible de configurer le salon de départ."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)

        

async def setup(bot):
    await bot.add_cog(Config(bot))