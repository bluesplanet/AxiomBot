import discord
from ...services.Rechercher.convert_type import convert_type
from utils.send import  send_message
from ...services.Rechercher.search.role_intelligent_search import chercher_role_intelligent
from config import Type

import logging
logger = logging.getLogger(__name__)


async def role_remove_one(ctx,membre,role,temps = 10):

    """
    Retire un rôle Discord à un membre.

    Parameters
    ----------
    ctx : commands.Context
        Contexte Discord utilisé pour les logs et les messages.

    membre : discord.Member
        Membre auquel le rôle doit être retiré.

    role : discord.Role
        Rôle à retirer.

    temps : int | None
        Durée d'affichage des messages temporaires.

    Returns
    -------
    None
        Envoie un message de réussite ou d'erreur.
    """

    try:

        await membre.remove_roles(role)
        logger.info(f"Retrait role {role.name} de {membre.name} par {ctx.author.name} réussi | temps : {temps}")
        message = f"**Le rôle {role.mention} a été retiré à {membre.mention}**"
        await send_message(ctx,message,color=Colors.SUCCESS,temps = Durations.SUCCESS)

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




async def retirer(ctx,membres,roles,etendre,temps = 10):

    """
    Retire plusieurs membres de plusieurs rôles Discord.

    Cette fonction recherche les membres et les rôles fournis,
    puis retire chaque rôle trouvé à chaque membre trouvé.

    Parameters
    ----------
    ctx : commands.Context
        Contexte de la commande Discord.

    membres : str
        Entrées représentant les membres auxquels les rôles
        doivent être retirés.

        Plusieurs entrées peuvent être séparées par des espaces.
        Elles sont converties en membres Discord par
        `convert_type()`.

    roles : str
        Entrées représentant les rôles à retirer.
        Plusieurs rôles peuvent être séparés par des espaces.

    etendre : Ouiounon
        Définit si la recherche des membres peut être étendue
        lors de l'utilisation de `convert_type()`.

    temps : int | None
        Durée en secondes pendant laquelle les messages envoyés
        par la fonction restent affichés.

    Process
    -------
    1. Sépare les entrées des membres.
    2. Sépare les entrées des rôles.
    3. Recherche chaque rôle avec `chercher_role_intelligent()`.
    4. Conserve uniquement les rôles trouvés avec le statut `exact`.
    5. Convertit chaque entrée membre avec `convert_type()`.
    6. Retire chaque rôle trouvé à chaque membre trouvé.
    7. Utilise `role_remove_one()` pour effectuer chaque retrait.

    Examples
    --------
    Si trois membres et deux rôles sont trouvés, six opérations
    sont effectuées :

        membre1 -> retrait role1
        membre1 -> retrait role2
        membre2 -> retrait role1
        membre2 -> retrait role2
        membre3 -> retrait role1
        membre3 -> retrait role2

    Returns
    -------
    None
        La fonction effectue directement les opérations Discord.
    """
    try:

        textes = str(membres).split()
        roles = str(roles).split()

        resultas_role = []
        resultas_membre = []
        for role in roles:
            resultas = await chercher_role_intelligent(ctx,role)
            if resultas["status"] == "exact":
                resultas_role.append(resultas["resultat"][0][0])
            else:
                continue
                

        for texte in textes:
            membres = await convert_type(ctx,texte,etendre,temps)
            resultas_membre.extend(membres)

        if not resultas_role:
            message = "**Aucun rôle n'a pu être trouvé.**"
            await send_message(
                ctx,
                message,
                color=Colors.WARNING,
                temps=Durations.WARNING
            )
            return

        if not resultas_membre:
            message = "**Aucun membre n'a pu être trouvé.**"
            await send_message(
                ctx,
                message,
                color=Colors.WARNING,
                temps=Durations.WARNING
            )
            return
        for role in resultas_role:
            for membre in resultas_membre:
                await role_remove_one(ctx,membre,role,temps)

    except Exception:
        message = "Erreur inattendue"
        await send_message(ctx,message,type=Type.WARNING)
        logger.exception(message)
        