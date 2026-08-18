import re
import logging


logger = logging.getLogger(__name__)



def convet_montion_role(ctx, entree):
     
    """
    Convertit une mention de rôle en liste de membres.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte de la commande Discord.
    entree : str
        Mention du rôle fournie par l'utilisateur.

    Retour
    ------
    list
        Liste des membres possédant le rôle.
        Retourne une liste vide si le rôle est introuvable.
    """

    logger.info(
        "Conversion mention rôle | entree=%s",
        entree
    )

    ids = re.findall(r"<@&(\d+)>", entree)

    if not ids:
        logger.warning(
            "Aucun ID rôle trouvé dans la mention | entree=%s",
            entree
        )
        return []

    role_id = int(ids[0])

    logger.debug(
        "ID rôle extrait | id=%s",
        role_id
    )

    role = ctx.guild.get_role(role_id)

    if not role:

        logger.warning(
            "Rôle introuvable | id=%s",
            role_id
        )

        return []


    logger.info(
        "Rôle trouvé ",
        f"| nom : {role.name}",
        f"| id : {role.id}",
        f"| membres : {len(role.members)}"
    )

    return role.members




def cherch_role_convert(ctx, nom):

    """
    Recherche un rôle par son nom et retourne ses membres.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte de la commande Discord.
    nom : str
        Nom du rôle recherché.

    Retour
    ------
    list
        Liste des membres possédant le rôle.
        Retourne une liste vide si aucun rôle n'est trouvé.
    """
     
    logger.info(
        "Recherche rôle par nom",
        f"|recherche : {nom}",    
    )


    for role in ctx.guild.roles:

        if role.name.lower() == nom:

            logger.info(
                "Rôle trouvé ",
                f"| nom : {role.name}",
                f"| id : {role.id}",
                f"| membres : {len(role.members)}"
            )

            return role.members



    logger.warning(
        "Aucun rôle trouvé",
        f"|recherche : {nom}"
        
    )


    return []