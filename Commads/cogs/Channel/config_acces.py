import discord
from utils.send import  send_message
from config import Colors,Durations
from ...services.Rechercher.search.role_intelligent_search import chercher_role_intelligent
import logging



logger = logging.getLogger(__name__)




async def salon_config_acces(ctx,channel,role):

    """
    Donne l'accès à un salon aux membres possédant un rôle.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    channel : discord.TextChannel
        Salon dont les permissions sont modifiées.

    role : discord.Role
        Rôle autorisé à voir et écrire dans le salon.

    Retour
    ------
    None
        Modifie les permissions et envoie un message de confirmation.
    """

    try:

        logger.warning("✅ Entrée ")
                
        await channel.set_permissions(
            role,
            view_channel=True,
            send_messages=True
        )

        message = f"Les personnes qui ont le rôle {role.mention} peuvent accéder au salon {channel.mention}"
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

    


async def salon_config_acces_multi(ctx,channel,roles):

    """
    Configure l'accès d'un salon pour plusieurs rôles.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    channel : discord.TextChannel
        Salon dont les permissions sont modifiées.

    roles : str
        Liste de rôles à rechercher et à autoriser.

    Retour
    ------
    None
        Configure les permissions pour les rôles trouvés.
    """
    try:

        logger.warning("✅ Entrée ")
        
        if roles is None:
            message = "Roles = None"
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return
        
        logger.warning("➡️✅ Entrée ")

        await channel.set_permissions(
        channel.guild.default_role,
        view_channel=False,
        send_messages=False
        )

        
        roles = str(roles).split()
        

        for role in roles:
            resultas = await chercher_role_intelligent(ctx,role)
            if resultas["status"] == "exact":
                rolex = resultas["resultat"][0][0]
                await salon_config_acces(ctx,channel,rolex)
            

    except Exception:
    
            message = "Erreur inattendue"
            await send_message(ctx,message,color=Colors.WARNING,temps = Durations.WARNING)
            logger.exception(message)
    