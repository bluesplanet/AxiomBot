import discord
import logging
from textwrap import dedent
from .Data.Databasse import get


logger = logging.getLogger(__name__)


async def member_join(membre):

    try:
        guild = membre.guild        
        config = get(guild.id)

        if config is None:
            logger.error("Configuration du serveur introuvable.")
            return 
        
        channel_id = config["welcome_channel_id"] 

        if channel_id is None:
            logger.error("Configuration de Welcome_channel introuvable. ")
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

    except discord.Forbidden:
                            
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        logger.error(message)

    except discord.NotFound:

        message = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        logger.error(message)

    except Exception:

        message = "Erreur inattendue"
        logger.exception(message)
