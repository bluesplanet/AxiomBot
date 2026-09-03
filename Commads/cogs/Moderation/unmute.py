import discord
import logging
from config import Type
from utils.send import  send_message




logger = logging.getLogger(__name__)




async def unmute(ctx,membre,raison):

    logger.warning("✅ Entrée ")

    try:
        
        await membre.timeout(
        None,
        reason=raison
        )

        message = f"Le timeout de {membre.mention} a été retiré. Raison: {raison}"
        await send_message(ctx,message,type=Type.SUCCESS)

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