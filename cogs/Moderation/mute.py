import discord
import logging
from datetime import timedelta
from config import Colors,Durations
from utils.send import  send_message



logger = logging.getLogger(__name__)



async def mute(ctx,membre,raison ,heure, minute):

    logger.warning("✅ Entrée ")

    try:

        if heure == 0 and minute == 0:
            message = "Tu dois mettre une durée supérieure à 0."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return

        
        duree = timedelta(
            hours=heure,
            minutes=minute
        )


        if duree.total_seconds() > 28 * 24 * 60 * 60:
            message = f"La durée maximale est de 28 jours."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return

    
        await membre.timeout(
            duree,
            reason=raison
        )

        
        message = f"{membre.mention} a été mute pendant {heure}h {minute}min."
        await send_message(ctx,message,color=Colors.SUCCESS,temps = Durations.SUCCESS)

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