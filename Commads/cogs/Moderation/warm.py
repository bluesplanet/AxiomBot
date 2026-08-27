import discord
import logging
from config import Colors,Durations
from utils.send import  send_message
from .Data.databasse import set_warm


logger = logging.getLogger(__name__)


async def execut_warn(ctx, membre, raison):

    """
    Avertit un membre et applique automatiquement un bannissement
    après trois avertissements.

    Le membre reçoit un message privé pour l'informer de son
    avertissement. Si le troisième avertissement est atteint,
    le membre est banni automatiquement après avoir été informé.

    Un message est également envoyé dans le contexte de la commande
    afin d'informer les administrateurs de l'action effectuée.

    Args:
        ctx (commands.Context):
            Contexte de la commande Discord.

        membre (discord.Member):
            Membre Discord auquel l'avertissement est attribué.

        raison (str):
            Raison de l'avertissement.

    Returns:
        None:
            La fonction ne retourne aucune valeur. Elle effectue
            directement l'avertissement ou le bannissement.

    Raises:
        discord.Forbidden:
            Si le bot n'a pas les permissions nécessaires ou si
            l'envoi du message privé est impossible.

        discord.NotFound:
            Si le membre ou la ressource demandée n'existe plus.

        discord.HTTPException:
            Si Discord rencontre une erreur lors de la requête.
    """

    logger.warning("✅ Entrée")


    try:

        resultat = set_warm(ctx.guild.id, membre.id)

        if resultat is True:
            # Le membre vient d'atteindre 3 warns
            try:
                message = (
                    f"**Vous avez été banni de {ctx.guild.name}.**\n"
                    f"Vous avez atteint **3 avertissements**.\n"
                    f"**Dernière raison :** {raison}\n\n"
                )
                await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS,destinataire=membre)

                message = (
                f"**{membre.name}** a été banni via AxiomBot.\n"
                f"**Raison :** 3 avertissements atteints.\n"
                )
                await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)
                
            except discord.Forbidden:
                logger.warning(
                    f"Impossible d'envoyer un DM à {membre}."
                )

            await membre.ban(
                reason=f"3 avertissements atteints. Dernière raison : {raison}"
            )

            return

        # Pas encore 3 warns
        # Ici tu peux récupérer le nombre actuel pour l'afficher
        try:

            message = (
                f"⚠️ **Vous avez reçu un avertissement **\n\n"
                f"**Raison :** {raison}\n\n"
                f"3 avertissements entraînent un bannissement."
            )
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS,destinataire=membre)

            message = f"**{membre.name}** a été averti via AxiomBot.\n"
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)

        except discord.Forbidden:
            logger.warning(
                f"Impossible d'envoyer un DM à {membre}."
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