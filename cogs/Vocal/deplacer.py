import discord
from utils.send import  send_message
from config import Colors,Durations
import logging



logger = logging.getLogger(__name__)




async def deplacer_vocal(ctx, membre,salon):

    logger.warning("✅ Entrée ")

    try:

        if membre.voice is None:
            message = f"{membre.mention} n'est connecté à aucun salon vocal."
            send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return 
        
        await membre.move_to(salon)
        message = f"{membre.mention} a été déplacé vers {salon.name}."
        await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)

    except discord.Forbidden:
                                   
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        await send_message(ctx,message,color=Colors.ERROR , temps = Durations.ERROR)
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        await send_message(ctx,message,color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except discord.NotFound:

        message = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        await send_message(ctx, message, color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except Exception:

        message = "Erreur inattendue"
        await send_message(ctx,message,color=Colors.WARNING,temps = Durations.WARNING)
        logger.exception(message)