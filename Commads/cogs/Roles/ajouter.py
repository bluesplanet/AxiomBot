import discord
from ...services.Rechercher.convert_type import convert_type
from utils.send import  send_message
from ...services.Rechercher.search.role_intelligent_search import chercher_role_intelligent
import logging
from config import Type

logger = logging.getLogger(__name__)



async def role_add_one(ctx,membre,role,temps):

    """

    Une fonction pour prend en charger l'ajout d'une seul perssonne :

    Prend en entrée:
        membre : Membre (objet discord obligatoire)
        role : Role (objet discord obligatoire)
        temps : {
        temps on seconde (ex : temps = 20 / suprimmes les message aprés 20 seconde) 
        (int obligatiore)
        NB : Certaine message sont encombrent ou sont temporair c'est pour ca que c'est on seconde est non on minute 
        }
    Operation:
        Ajout le perssone de Varibla "membre" à Variable "Rola" . Fin tache
    
    Return:
        None

    Exection(Gestion de erreur):
        except discord.Forbidden:
        except discord.HTTPException:
        except Exception:

    """

    try:

        logger.warning("✅ Entrée ")

        await membre.add_roles(role)
        logger.info(f"Ajout role {role.name} à {membre.name} par {ctx.author.name} réussi | temps : {temps}") 
        message = f"**Le rôle {role.mention} a été ajouté à {membre.mention}**"
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

    
    


async def ajouter(ctx,membres,roles,etendre,temps):

    """
    Ajoute plusieurs membres à plusieurs rôles Discord.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    membres : str
        Entrées représentant les membres à ajouter.
        Plusieurs entrées peuvent être fournies et sont séparées
        par des espaces.

        Les entrées sont converties par `convert_type()`.
        Une entrée peut notamment représenter un membre, une
        mention, un ID ou, selon la configuration, un rôle.

    roles : str
        Entrées représentant les rôles auxquels les membres
        doivent être ajoutés.
        Plusieurs rôles peuvent être fournis et sont séparés
        par des espaces.

    etendre : Ouiounon
        Définit si la recherche peut être étendue lors de la
        conversion des entrées.

    temps : int
        Durée en secondes pendant laquelle les messages temporaires
        restent affichés.

    Fonctionnement
    --------------
    1. Sépare les entrées membres.
    2. Recherche et convertit chaque entrée en membre Discord.
    3. Sépare les entrées rôles.
    4. Recherche chaque rôle avec `chercher_role_intelligent()`.
    5. Conserve uniquement les rôles trouvés avec une correspondance
       exacte.
    6. Ajoute chaque membre trouvé à chaque rôle trouvé.

    Exemple
    -------
    Si `membres` contient trois membres et `roles` contient deux rôles,
    la fonction tente d'effectuer six opérations :

        membre1 → rôle1
        membre1 → rôle2
        membre2 → rôle1
        membre2 → rôle2
        membre3 → rôle1
        membre3 → rôle2

    Retour
    ------
    None
        La fonction effectue les opérations directement et ne retourne
        aucune valeur.
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
                await role_add_one(ctx,membre,role,temps)

    except Exception:
        message = "Erreur inattendue"
        await send_message(ctx,message,type=Type.WARNING)
        logger.exception(message)

    

