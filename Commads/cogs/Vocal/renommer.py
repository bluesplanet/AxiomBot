import discord
from utils.send import  send_message
from config import Type
import logging



logger = logging.getLogger(__name__)



async def renommer_vocal(ctx,salon,nouveau_nom):

    logger.warning("✅ Entrée ")

    try:
        await salon.edit(name=nouveau_nom)
        message = f"Le salon vocal est maintenant : {nouveau_nom}"
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