import discord
from utils.send import  send_message
from config import Colors,Durations
import logging



logger = logging.getLogger(__name__)




async def limite_vocal(ctx,salon,limite):

    logger.warning("✅ Entrée ")

    try:

        if limite == 0:

            message = "Non non non, pas de 0 ici petit"
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.WARNING)
            return

        if limite == 999:

            message = "Serieusement"
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)
            return

        await salon.edit(user_limit=limite)
        message = f"Limite du salon définie à {limite} membres."
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