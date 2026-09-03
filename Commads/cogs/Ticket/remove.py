import discord
import logging
from utils.send import  send_message
from config import Type




logger = logging.getLogger(__name__)




async def remove_ticket(ctx,membre,channel):

    """
    Retire les permissions personnalisées d'un membre sur un ticket.

    L'overwrite de permissions associé au membre est supprimé du salon,
    ce qui lui retire l'accès spécifique qui lui avait été accordé sur
    le ticket, sans modifier les permissions des autres membres.

    Args:
        ctx (commands.Context):
            Contexte de la commande Discord.

        membre (discord.Member):
            Membre Discord à retirer du ticket.

        channel (discord.TextChannel):
            Salon correspondant au ticket.

    Returns:
        None:
            La fonction ne retourne aucune valeur.

    Raises:
        discord.Forbidden:
            Si le bot n'a pas les permissions nécessaires pour modifier
            les permissions du salon.

        discord.NotFound:
            Si le membre ou le salon demandé est introuvable.

        discord.HTTPException:
            Si Discord rencontre une erreur lors de la modification
            des permissions.
    """
    
    logger.warning("✅ Entrée ")

    try:
        if channel:
                    
            await channel.set_permissions(
                membre,
                overwrite = None
            )
        message = f"✅ **{membre.mention} a été retiré du ticket.**"
        await send_message(ctx,message,type=Type.SUCCESS)

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
        
