import logging
from utils.eumu import Ouiounon
from .membre_intelligent_search import chercher_membre_intelligent
from .role_intelligent_search import chercher_role_intelligent

logger = logging.getLogger(__name__)

"""
Module de recherche intelligente des objets Discord.

Ce module centralise la recherche d'objets Discord à partir
d'un texte fourni par l'utilisateur.

Ordre de recherche :
- Membre
- Rôle (si la recherche étendue est autorisée)

Le module retourne le type d'objet trouvé ainsi que le
résultat de la recherche.
"""

async def chercher_objet_discord(ctx, texte, etendre):
    
    logger.info(
        "Trouver le type (Role or Member) | texte=%s",
        texte
    )


    membre = await chercher_membre_intelligent(
        ctx,
        str(texte)
    )
    


    if membre["status"] != "introuvable":

        logger.info(
            "Objet trouvé comme membre"
        )

        return {
            "type": "membre",
            **membre
        }



    logger.debug(
        "Membre non trouvé, recherche rôle [Pesmission d'etendre la recherche : %s]",etendre
    )

    

    role = await chercher_role_intelligent(
        ctx,
        str(texte)
    )

    if etendre == Ouiounon.OUI:
        if role["status"] != "introuvable":

            logger.info(
                "Objet trouvé comme rôle"
            )

            return {
                "type": "role",
                **role
            }



        logger.warning(
            "Objet Discord introuvable | recherche=%s",
            texte
        )


        return {
            "type": "inconnu",
            "status": "introuvable",
            "resultat": []
        }
    
    logger.info("Permission non accordé :%s",etendre)
    logger.warning(
        "Objet Discord introuvable | recherche=%s",
        texte
    )


    return {
        "type": "inconnu",
        "status": "introuvable",
        "resultat": []
    }