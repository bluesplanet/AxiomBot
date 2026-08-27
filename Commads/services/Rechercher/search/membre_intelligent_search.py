import logging
from difflib import SequenceMatcher


logger  = logging.getLogger(__name__)


async def chercher_membre_intelligent(ctx, nom):

    """
    Recherche un membre Discord avec une correspondance intelligente.

    La fonction compare le nom fourni par l'utilisateur avec :
    - le nom utilisateur Discord
    - le nom affiché du membre

    Elle utilise un score de similarité pour trouver :
    - une correspondance exacte
    - un résultat fiable
    - plusieurs propositions possibles
    - aucun résultat

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord contenant le serveur.

    nom : str
        Nom ou pseudo recherché.

    Retour
    ------
    dict
        Résultat contenant :
        - status :
            "exact"        → membre trouvé avec certitude
            "plusieurs"    → plusieurs membres proches
            "propositions" → suggestions possibles
            "introuvable"  → aucun membre trouvé

        - resultat :
            Liste des membres trouvés avec leur score.
            Format :
            [(member, score)]
    """

    logger.info(
        "Recherche membre intelligente | recherche=%s",
        nom
    )

    nom = nom.lower()

    propositions = []
    meilleur_resultat = []
    resultats = []


    for member in ctx.guild.members:

        noms = {
            member.name.lower(),
            member.display_name.lower()
        }


        for nom_membres in noms:

            scor = SequenceMatcher(
                None,
                nom,
                nom_membres
            ).ratio()


            logger.debug(
                "Comparaison membre | recherche=%s | membre=%s | score=%.2f",
                nom,
                nom_membres,
                scor
            )


            if scor >= 0.45:

                resultats.append(
                    (member, scor)
                )


    logger.info(
        "Comparaison terminée | résultats trouvés=%s",
        len(resultats)
    )


    resultats.sort(
        key=lambda x: x[1],
        reverse=True
    )


    for member, scor in resultats:

        if scor == 1.0:

            logger.info(
                "Correspondance exacte membre | nom=%s | score=%.2f",
                member.display_name,
                scor
            )

            return {
                "status": "exact",
                "resultat": [(member, scor)]
            }


        elif scor >= 0.85:

            meilleur_resultat.append(
                (member, scor)
            )


        elif scor >= 0.45:

            propositions.append(
                (member, scor)
            )


    if len(meilleur_resultat) == 1:

        logger.info(
            "Membre fiable trouvé | nom=%s",
            meilleur_resultat[0][0].display_name
        )

        return {
            "status": "exact",
            "resultat": meilleur_resultat
        }


    elif len(meilleur_resultat) > 1:

        logger.warning(
            "Plusieurs membres proches trouvés | nombre=%s",
            len(meilleur_resultat)
        )

        return {
            "status": "plusieurs",
            "resultat": meilleur_resultat
        }


    elif propositions:

        logger.info(
            "Propositions membres trouvées | nombre=%s",
            len(propositions)
        )

        return {
            "status": "propositions",
            "resultat": propositions
        }


    else:

        logger.warning(
            "Aucun membre trouvé | recherche=%s",
            nom
        )

        return {
            "status": "introuvable",
            "resultat": []
        }