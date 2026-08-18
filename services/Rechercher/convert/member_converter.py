import re
import logging


logger = logging.getLogger(__name__)


def convert_montion_membre(ctx, entree):
    
    """
    Convertit une mention Discord en objet Member.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte de la commande Discord.
    entree : str
        Mention du membre fournie par l'utilisateur.

    Retour
    ------
    list
        Liste contenant le membre trouvé.
        Retourne une liste vide si aucun membre n'est trouvé.
    """

    logger.info(
        "Conversion mention membre",
        f"|entree : {entree}"
       
    )

    liste_temp = []

    ids = re.findall(r"<@!?(\d+)>", entree)

    if not ids:

        logger.warning(
            "Aucun ID membre trouvé ",
            "|entree : {entree}"
        )

        return []


    membre_id = int(ids[0])

    logger.debug(
        "ID membre extrait",
        f"|id : {membre_id}"    
    )

    membre = ctx.guild.get_member(membre_id)

    if not membre:

        logger.warning(
            "Membre introuvable",
            f"|id : {membre_id}"
            
        )

        return []


    logger.info(
        "Membre trouvé",
        f"| nom : {membre.display_name}",
        f"| id : {membre.id}"
    )


    liste_temp.append(membre)

    return liste_temp




def cherch_membre_convert(ctx, nom):

    logger.info(
        "Recherche membre par nom",
        f"| recherche : {nom}"
        
    )


    liste_temp = []

    for membre in ctx.guild.members:

        if membre.name.lower() == nom:

            logger.debug(
                "Correspondance username ",
                f"| membre : {membre.display_name}"                
            )

            liste_temp.append(membre)


        if membre.display_name.lower() == nom:

            logger.debug(
                "Correspondance display_name ",
                f"|membre : {membre.display_name}"
                
            )

            liste_temp.append(membre)


    logger.info(
        "Recherche membre terminée ",
        f"|résultats : { len(liste_temp)}"  
    )


    return liste_temp
