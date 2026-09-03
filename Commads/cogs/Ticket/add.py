import discord
import logging
from utils.send import  send_message
from config import Type




logger = logging.getLogger(__name__)




async def add_ticket(ctx,membre,channel):

    """
    Ajoute un membre à un ticket en lui accordant les permissions nécessaires.

    Le membre peut alors consulter le salon, envoyer des messages et
    accéder à l'historique du ticket. Les permissions des autres membres
    du salon ne sont pas modifiées.

    Args:
        ctx (commands.Context):
            Contexte de l'exécution de la commande.

        channel (discord.TextChannel):
            Salon correspondant au ticket dans lequel le membre doit
            être ajouté.

        membre (discord.Member):
            Membre Discord à autoriser dans le ticket.

    Returns:
        None:
            La fonction ne retourne aucune valeur.

    Raises:
        discord.Forbidden:
            Si le bot ne possède pas les permissions nécessaires pour
            modifier les permissions du salon.

        discord.NotFound:
            Si le salon ou le membre demandé est introuvable.

        discord.HTTPException:
            Si Discord rencontre une erreur lors de la modification
            des permissions.
    """

    logger.warning("✅ Entrée ")

    try:
        if channel:
                    
            await channel.set_permissions(
                membre,
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        message = f"✅ **{membre.mention} a été ajouté au ticket.**"
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
        