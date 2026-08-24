import discord
from utils.send import  send_message
import logging
from config import Colors,Durations
logger = logging.getLogger(__name__)



async def renommer(ctx,role,nouveau_nom,temps):

    """
    Renomme un rôle Discord.

    Exécute
    -------
    - Vérifie que le rôle n'est pas le rôle @everyone.
    - Récupère le nom actuel du rôle.
    - Renomme le rôle avec le nouveau nom.
    - Indique dans la raison de modification quel utilisateur a effectué l'action.
    - Informe l'utilisateur du changement effectué.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    role : discord.Role
        Rôle Discord à renommer.

    nouveau_nom : str
        Nouveau nom à attribuer au rôle.

    temps : int | float
        Durée utilisée pour l'affichage du message de confirmation.

    Retour
    ------
    None
        Aucun retour.
    """

    try:

        logger.warning("✅ Entrée ")
        
        if role == ctx.guild.default_role:
            message = "Le rôle @everyone ne peut pas être renommé."
            await send_message(ctx,message,color=Colors.ERROR ,temps = Durations.ERROR)
            return

        ancien_nom = role.name
        await role.edit(
            name = nouveau_nom,
            reason = f"Renommé par {ctx.author}"
        )

        message = f"**Le rôle ~~{ancien_nom}~~ a été renommé en {nouveau_nom}**"
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
