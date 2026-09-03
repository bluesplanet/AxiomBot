import discord
import logging
from config import Type
from utils.send import send_message


logger = logging.getLogger(__name__)


async def debannir(ctx,idmenbre,raison):

    logger.warning("✅ Entrée ")

    try:
        
        user = await ctx.bot.fetch_user(int(idmenbre))
        await ctx.guild.unban(user, reason=raison)
        message = f"{user} a été débanni. **Raison :** {raison}"
        await send_message(ctx,message,color=Colors.SUCCESS ,temps = Durations.SUCCESS)

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