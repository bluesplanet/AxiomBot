from .detecter_type import TypeEntre , detecter_type
import logging
from .embed.embed import role_plusieurs,role_propositions,role_introuvable
from .embed.embed import membre_plusieurs,membre_propositions,membre_introuvable
from utils.eumu import Ouiounon
from .convert.member_converter import convert_montion_membre
from .search.chercher_objet_discord import chercher_objet_discord

logger = logging.getLogger(__name__)


async def convert_type(ctx, entree, etendre ,temps = None):
    

    logger.info(
        "Début conversion | entree=%s",
        entree
    )

    membres_liste = []

    texte = str(entree)

    logger.debug(
        "Conversion en texte | texte=%s",
        texte
    )

    type_entree = detecter_type(texte)

    logger.info(
        "Type identifié | type=%s",
        type_entree
    )


    if type_entree == TypeEntre.MENTION_MEMBRE:

        logger.info(
            "Conversion mention membre"
        )

        membres_liste.extend(
            convert_montion_membre(ctx, texte)
        )

        logger.info(
            "Mention membre convertie | nombre=%s",
            len(membres_liste)
        )


    elif type_entree == TypeEntre.MENTION_ROLE:

        logger.info(
            "Conversion mention rôle"
        )

        membres_liste.extend(
            convert_montion_membre(ctx, texte)
        )

        logger.info(
            "Mention rôle convertie | membres=%s",
            len(membres_liste)
        )


    elif type_entree == TypeEntre.ID:

        logger.info(
            "Recherche par ID | id=%s",
            texte
        )

        membre = ctx.guild.get_member(int(texte))

        if membre:

            logger.info(
                "Membre trouvé | nom=%s | id=%s",
                membre.display_name,
                membre.id
            )

            membres_liste.append(membre)

        else:

            role = ctx.guild.get_role(int(texte))

            if role:

                logger.info(
                    "Rôle trouvé | nom=%s | id=%s",
                    role.name,
                    role.id
                )

                membres_liste.extend(
                    role.members
                )

            else:

                logger.warning(
                    "Aucun membre ou rôle trouvé avec ID=%s",
                    texte
                )


    elif type_entree == TypeEntre.NOM:


        logger.info(
            "Recherche par nom | texte=%s",
            texte
        )




        object = await chercher_objet_discord(
            ctx,
            texte,
            etendre
        )


        logger.info(
            "Résultat recherche | type=%s | status=%s",
            object.get("type"),
            object.get("status")
        )


        if object["type"] == "membre":


            if object["status"] == "exact":

                membre = object["resultat"][0][0]

                logger.info(
                    "Membre exact trouvé | nom=%s | id=%s",
                    membre.display_name,
                    membre.id
                )

                membres_liste.append(membre)


            elif object["status"] == "plusieurs":

                logger.warning(
                    "Plusieurs membres trouvés | recherche=%s | nombre=%s",
                    texte,
                    len(object["resultat"])
                )

                await membre_plusieurs(ctx,texte,object,temps)

            elif object["status"] == "propositions":

                logger.warning(
                    "Propositions membres | recherche=%s | nombre=%s",
                    texte,
                    len(object["resultat"])
                )

                await membre_propositions(ctx,texte,object,temps)


            elif object["status"] == "introuvable":

                logger.warning(
                "Membre introuvable | recherche=%s",
                texte
                )

                await membre_introuvable(ctx,texte,temps)
        

        if object["type"] == "role" and etendre == Ouiounon.NON:


            if object["status"] == "exact":

                role = object["resultat"][0][0]

                logger.info(
                    "Rôle exact trouvé | nom=%s | id=%s",
                    role.name,
                    role.id
                )
                logger.info("Trasformation de l'object role on liste role.membres" )
                membres_liste.extend(
                    role.members
                )


            elif object["status"] == "plusieurs":

                logger.warning(
                    "Plusieurs rôles trouvés | recherche=%s | nombre=%s",
                    texte,
                    len(object["resultat"])
                )

                await role_plusieurs(ctx,texte,object,temps)


            elif object["status"] == "propositions":

                logger.warning(
                    "Propositions rôles | recherche=%s | nombre=%s",
                    texte,
                    len(object["resultat"])
                )

                await role_propositions(ctx,texte,object,temps)

            elif object["status"] == "introuvable":

                logger.warning(
                    "Rôle introuvable | recherche=%s",
                    texte
                )

                await role_introuvable(ctx,texte,temps)
                

    logger.debug(
        "Liste avant suppression doublons | membres=%s",
        membres_liste
    )


    dictionnaire = {}

    for member in membres_liste:
        dictionnaire[member.id] = member


    membres_liste = list(
        dictionnaire.values()
    )


    logger.info(
        "Conversion terminée | nombre_membres=%s",
        len(membres_liste)
    )


    logger.debug(
        "Résultat final | membres=%s",
        membres_liste
    )


    return membres_liste