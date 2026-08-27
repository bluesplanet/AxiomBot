import discord
from textwrap import dedent
from discord.ext import commands
from utils.send import send_message
from config import Colors,Durations
import logging
from .Data.Databasse import set,get




logger = logging.getLogger(__name__)




class Event(commands.Cog):


    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self,membre):
        
        guild = membre.guild

        config = get(guild.id)

        if config is None:
            logger.error("Configuration du serveur introuvable.")
            return
        
        channel_id = config["welcome_channel_id"] 

        if channel_id is None:
            logger.error("Welcome_channel vide")
            return

        embed = discord.Embed(
            title=f"🎉 Bienvenue sur {membre.guild.name} !",
            description=dedent(f"""
            Bonjour {membre.mention} 👋

            Nous sommes ravis de t'accueillir parmi nous !

            Prends quelques instants pour découvrir le serveur et n'hésite pas à participer aux discussions. Nous espérons que tu passeras un excellent moment avec la communauté.
            """),
            color=discord.Color.green()
        )

        embed.add_field(
            name="👥 Membres",
            value=dedent(f"Tu es le **{membre.guild.member_count}ᵉ** membre du serveur !"),
            inline=True
        )

        embed.set_footer(
            text=f"Bon séjour sur {membre.guild.name} !❤"
        )

        embed.set_thumbnail(
            url=membre.avatar.url if membre.avatar else membre.default_avatar.url
        )

        welcom_channel = guild.get_channel(channel_id)
        await welcom_channel.send(embed=embed)




    @commands.Cog.listener()
    async def on_member_remove(self,membre):
        guild = membre.guild

        config = get(guild.id)

        if config is None:
            logger.error("Configuration du serveur introuvable.")
            return
    
        bey_channel_id = config["bey_channel_id"]

        if bey_channel_id is None:
            logger.error("Bey_channel vide")
            return

        embed = discord.Embed(
            title=f"👋 Au revoir {membre.name} !",
            description=dedent(f"""
            Nous sommes désolés de te voir partir, {membre.mention}.

            N'hésite pas à revenir à tout moment si tu changes d'avis !
            """),
            color=discord.Color.red()
        )

        embed.add_field(
            name="👥 Membres",
            value=dedent(f"Il ne reste plus que **{membre.guild.member_count}** membres sur le serveur."),
            inline=True
        )

        embed.set_footer(
            text=f"À bientôt sur {membre.guild.name} !"
        )

        embed.set_thumbnail(
            url=membre.avatar.url if membre.avatar else membre.default_avatar.url
        )

        bey_channel = guild.get_channel(bey_channel_id)
        await bey_channel.send(embed=embed)

        try:
        
            await membre.send(embed=embed)

        except discord.Forbidden:
            logger.warning(
                f"Impossible d'envoyer le message privé à {membre}."
            )

        except discord.HTTPException:
            logger.exception(
                "Erreur Discord lors de l'envoi du message privé."
            )
        


async def setup(bot):
    logger.warning("Event cog _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ")
    await bot.add_cog(Event(bot))