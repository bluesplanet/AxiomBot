from difflib import SequenceMatcher
import logging


logger = logging.getLogger(__name__)


async def chercher_role_intelligent(ctx, nom):

    """
    Recherche un rôle Discord avec une correspondance intelligente.

    Cette fonction compare le nom fourni par l'utilisateur avec
    les rôles présents dans le serveur grâce à un score de similarité.
    Elle permet de détecter :
    - Une correspondance exacte
    - Un rôle fortement similaire
    - Plusieurs propositions possibles
    - Aucun résultat trouvé

    Paramètres
    ----------
    ctx : commands.Context
        Contexte de la commande Discord contenant le serveur.

    nom : str
        Nom du rôle recherché par l'utilisateur.

    Retour
    ------
    dict
        Contient :
        - status : état de la recherche
            "exact"        → rôle trouvé avec certitude
            "plusieurs"    → plusieurs rôles proches trouvés
            "propositions" → résultats possibles
            "introuvable"  → aucun rôle trouvé

        - resultat : liste des rôles trouvés avec leur score
          sous la forme :
          [(role, score)]
    """

    logger.info(
        "Recherche rôle intelligente | recherche=%s",
        nom
    )


    nom = nom.lower()

    propositions = []
    meilleur_resultat = []
    resultats = []


    for role in ctx.guild.roles:

        nom_role = role.name.lower()


        scor = SequenceMatcher(
            None,
            nom,
            nom_role
        ).ratio()


        logger.debug(
            "Comparaison rôle | recherche=%s | rôle=%s | score=%.2f",
            nom,
            nom_role,
            scor
        )


        if scor >= 0.50:

            resultats.append(
                (role, scor)
            )


    logger.info(
        "Comparaison rôles terminée | résultats=%s",
        len(resultats)
    )


    resultats.sort(
        key=lambda x: x[1],
        reverse=True
    )


    for role, scor in resultats:


        if scor == 1.0:

            logger.info(
                "Correspondance exacte rôle | rôle=%s",
                role.name
            )

            return {
                "status": "exact",
                "resultat": [(role, scor)]
            }


        elif scor >= 0.90:

            meilleur_resultat.append(
                (role, scor)
            )


        elif scor >= 0.50:

            propositions.append(
                (role, scor)
            )


    if len(meilleur_resultat) == 1:

        logger.info(
            "Rôle fiable trouvé | rôle=%s",
            meilleur_resultat[0][0].name
        )

        return {
            "status": "exact",
            "resultat": meilleur_resultat
        }


    elif len(meilleur_resultat) > 1:

        logger.warning(
            "Plusieurs rôles proches trouvés | nombre=%s",
            len(meilleur_resultat)
        )

        return {
            "status": "plusieurs",
            "resultat": meilleur_resultat
        }


    elif propositions:

        logger.info(
            "Propositions rôles trouvées | nombre=%s",
            len(propositions)
        )

        return {
            "status": "propositions",
            "resultat": propositions
        }


    else:

        logger.warning(
            "Aucun rôle trouvé | recherche=%s",
            nom
        )

        return {
            "status": "introuvable",
            "resultat": []
        }
