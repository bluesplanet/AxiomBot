import discord
from .Data.databasse import get_tiket
from utils.send import  send_message
from config import Durations,Colors
from .corbaille import remove_corbaille
import logging



logger = logging.getLogger(__name__)




async def delet_utilisateur(ctx):

    """
    Ferme le ticket de l'utilisateur.

    Exécute
    -------
    - Récupère le ticket associé à l'utilisateur.
    - Crée la catégorie « Corbail » si nécessaire.
    - Déplace le ticket dans cette catégorie.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord.

    Retour
    ------
    None
        Aucun retour.
    """

    try:
        
        logger.warning("✅ Entrée ")

        channel_id = get_tiket(ctx.guild.id, ctx.author.id)
        
        if channel_id[0] is None:
            message = "Tu n'as aucun ticket ouvert."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return

        channel = ctx.guild.get_channel(channel_id[0])
        
        
        if channel is None:
            message = "Ton ticket n'existe plus ou n'est plus accessible."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return

        await remove_corbaille(ctx,channel)

    except discord.Forbidden:
                    
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        await send_message(ctx,message,color=Colors.ERROR , temps = Durations.ERROR)
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        await send_message(ctx,message,color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except discord.NotFound:

        messages = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        await send_message(ctx, messages, color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except Exception:
            message = "Erreur inattendue"
            await send_message(ctx,message,color=Colors.WARNING,temps = Durations.WARNING)
            logger.exception(message)





async def delet_staff(ctx):

    """
    Ferme le ticket actuel en tant que membre du staff.

    Exécute
    -------
    - Vérifie que le salon actuel est un ticket.
    - Récupère l'auteur du ticket.
    - Crée la catégorie « Corbail » si nécessaire.
    - Déplace le ticket dans la catégorie « Corbail ».

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord.

    Retour
    ------
    None
        Aucun retour.
    """

    try:

        logger.warning("✅ Entrée ")
        
        author_id = get_tiket(ctx.guild.id,channel_id=ctx.channel.id)

        if author_id is None or not ctx.channel.name.lower().startswith("ticket-"):
            message = ("Tu dois être dans le ticket de la personne que tu veux fermer.")
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return

        await remove_corbaille(ctx,ctx.channel)
        
        
        
        
    except discord.Forbidden:
                    
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        await send_message(ctx,message,color=Colors.ERROR , temps = Durations.ERROR)
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        await send_message(ctx,message,color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except discord.NotFound:

        messages = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        await send_message(ctx, messages, color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except Exception:
            message = "Erreur inattendue"
            await send_message(ctx,message,color=Colors.WARNING,temps = Durations.WARNING)
            logger.exception(message)