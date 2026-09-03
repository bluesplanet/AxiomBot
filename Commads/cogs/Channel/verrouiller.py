import discord
from utils.send import  send_message
from config import Type
import logging



logger = logging.getLogger(__name__)




async def salon_verrouiller(ctx):
    

    """
    Verrouille le salon actuel pour @everyone.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    Retour
    ------
    None
        Modifie les permissions du salon et envoie un message de résultat.
    """

    try:

        logger.warning("✅ Entrée ")

        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages is False:

            message = "🔒** Le salon et déja verrouillé **"
            await send_message(ctx, message,type=Type.SUCCESS)

        else:
            overwrite.send_messages = False

            
            await ctx.channel.set_permissions(
                ctx.guild.default_role,
                overwrite=overwrite
            )
            message = "🔒** Salon verrouillé **"
            await send_message(ctx, message,type=Type.SUCCESS)

    except discord.Forbidden:
                           
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        await send_message(ctx,message,type=Type.ERROR)
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        await send_message(ctx,message,type=Type.ERROR)
        logger.error(message)

    except discord.NotFound:

        message = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        await send_message(ctx, message, type=Type.ERROR)
        logger.error(message)

    except Exception:

        message = "Erreur inattendue"
        await send_message(ctx,message,type=Type.WARNING)
        logger.exception(message)