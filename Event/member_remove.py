import discord
import logging
from textwrap import dedent
from .Data.Databasse import get
from utils.send import send_message
from config import Type

logger = logging.getLogger(__name__)


async def membre_remove(membre):

    """
    Gère le départ d'un membre du serveur.

    Récupère la configuration du serveur, envoie un message d'au revoir
    dans le canal configuré, puis tente d'envoyer le même message au membre
    en message privé.

    Args:
        membre: Membre Discord ayant quitté le serveur.
    """

    try:
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