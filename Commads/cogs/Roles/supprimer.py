import discord
from utils.send import  send_message
from config import Type
import logging
logger = logging.getLogger(__name__)
async def supprimer(ctx,role,temps=None):


    try:
        
        await role.delete(
            reason=f"Supprimé par {ctx.author}"
        )
        message = f"Le rôle **{role.name}** a été supprimé."
        await send_message(ctx,message,color=Colors.SUCCESS,temps = Durations.SUCCESS)

        
    except discord.Forbidden:
                
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        await send_message(ctx,message,type=Type.ERROR)
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        await send_message(ctx,message,type=Type.ERROR)
        logger.error(message)

    except discord.NotFound:

        messages = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        await send_message(ctx, messages, type=Type.ERROR)
        logger.error(message)

    except Exception:
            message = "Erreur inattendue"
            await send_message(ctx,message,type=Type.WARNING)
            logger.exception(message)
    