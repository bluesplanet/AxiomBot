import discord
import logging
from config import Colors,Durations
from .utils.send import send_message
from .Embed.create_embed_all import Pagination


logger = logging.getLogger(__name__)


async def listban(ctx):

    logger.warning("➡️✅ Entrée ")

    try:
        
        bans = [entry async for entry in ctx.guild.bans()]
        if not bans:
            message = "Liste vide"
            await send_message(
                ctx,
                message,
                color=Colors.ERROR,
                temps=Durations.ERROR
            )
            return

        
        pages = {
            "type" : "membre",
            "pages" : bans
        }

        titre= "La liste des ban"
        titre_all = titre

        view = Pagination(
            pages=pages,
            titre=titre,
            titre_all=titre_all
        )
    
        await ctx.send(
            embed = view.create_embed(),
            view = view,
            delete_after = Durations.SUCCESS
        )


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
