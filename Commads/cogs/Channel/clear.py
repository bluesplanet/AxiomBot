import discord
from utils.send import  send_message
from config import Colors,Durations
import logging



logger = logging.getLogger(__name__)


async def clear(ctx,limite,membre):

    """
Supprime un nombre défini de messages dans le salon.

Exécute
-------
- Vérifie que la limite est supérieure à zéro.
- Si un membre est fourni, supprime uniquement ses messages.
- Sinon, supprime les derniers messages du salon.
- Informe l'utilisateur du nombre de messages supprimés.

Paramètres
----------
ctx : commands.Context
    Contexte Discord de la commande.

limite : int
    Nombre maximal de messages à rechercher et supprimer.

membre : discord.Member, optionnel
    Membre dont les messages doivent être supprimés.
    Si aucun membre n'est fourni, les messages sont supprimés
    sans filtrage par auteur.

Retour
------
None
    Aucun retour. La commande envoie directement un message
    indiquant le résultat de l'opération.
"""

    try:

        logger.warning("✅ Entrée ")

        if limite <= 0:
            message = f"Le nombre de messages doit être supérieur à 0."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return
        
        if membre is not None:
            deleted = await ctx.channel.purge(limit=limite, check=lambda message: message.author == membre)
            message = (
                f"🧹 **{len(deleted)} message(s) supprimé(s)** "
                f"de {membre.mention}."
            )
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)
            return
        
        deleted = await ctx.channel.purge(limit=limite)
        message = f"🧹 {len(deleted)} message(s) supprimé(s)."
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