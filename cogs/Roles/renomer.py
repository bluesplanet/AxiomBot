import discord
from .utils.send import send_message
import logging
from config import Colors,Durations
logger = logging.getLogger(__name__)



async def renommer(ctx,role,nouveau_nom,temps=None):
    try:
        if role == ctx.guild.default_role:
            message = "Le rôle @everyone ne peut pas être renommé."
            await send_message(ctx,message,color=Colors.ERROR ,temps = Durations.ERROR)

        ancien_nom = role.name
        await role.edit(
            name = nouveau_nom,
            reason = f"Renommé par {ctx.author}"
        )

        message = f"**Le rôle ~~{ancien_nom}~~ a été renommé en {nouveau_nom.mention}**"
        await send_message(ctx,message,color=Colors.SUCCESS , temps = Durations.SUCCESS)

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
