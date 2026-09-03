import discord
import logging
from .Embed.create_embed_all import Pagination
from config import Type
from utils.send import  send_message




logger = logging.getLogger(__name__)




async def muteliste(ctx):

    try:

        logger.warning("✅ Entrée ")

        page = []
        nombre = 0
        for membre in ctx.guild.members:

            if membre.timed_out_until is None:
                continue
            if membre.timed_out_until <= discord.utils.utcnow():
                continue
            nombre += 1
            
            page_all += (
                f"Membre : {membre.mention}\n"
                f"ID : {membre.id}\n"
                f"Fin : {membre.timed_out_until.strftime('%d/%m/%Y à %H:%M UTC')}\n\n"
            )

            page.append(
                f"Membre : {membre.mention}\n"
                f"ID : {membre.id}\n"
                f"Fin : {membre.timed_out_until.strftime('%d/%m/%Y à %H:%M UTC')}\n\n"
            )

        if nombre == 0:

            message = "Aucun membre n'est actuellement en timeout."
            await send_message(ctx,message,type=Type.ERROR)

            return

        page_all += f"Total : {nombre} membre(s)."
        page.append(f"Total : {nombre} membre(s).")

        titre = f"Membres actuellement en timeout\n\n"
        titre_all = f"Membres actuellement en timeout\n\n"

        pages = {
            "type" : "membre",
            "pages" : pages,
              "pages_all" : page_all
        }

        view = Pagination(
            pages=pages,
            titre = titre,
            titre_all = titre_all
        )

        await ctx.send(
            embed = view.create_embed(),
            view = view,
            delete_after = 30
        )


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