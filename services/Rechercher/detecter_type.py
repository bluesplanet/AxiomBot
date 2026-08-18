import re
import logging
from enum import Enum
logger = logging.getLogger(__name__)


class TypeEntre(Enum):

    """
    Types d'entrée reconnus.

    MENTION_MEMBRE : Mention d'un membre Discord (<@123456789>)
    MENTION_ROLE   : Mention d'un rôle Discord (<@&123456789>)
    ID             : Identifiant Discord numérique
    NOM            : Nom classique
    INVALIDE       : Entrée vide ou invalide
    """

    MENTION_MEMBRE = "mention_membre"
    MENTION_ROLE = "mention_role"
    ID = "id"
    NOM = "nom"
    INVALIDE = "invalide"




def detecter_type(entree):

    """
    Détecte automatiquement le type d'une entrée utilisateur.

    Paramètres
    ----------
    entree : str
        Texte fourni par l'utilisateur.

    Retour
    ------
    TypeEntre
        Le type détecté :
        - MENTION_MEMBRE
        - MENTION_ROLE
        - ID
        - NOM
        - INVALIDE
    """

    logger.info(
        f"Détection du type |entree : %s", entree
    )

    if not entree:

        logger.warning("Entrée vide reçue")
        return TypeEntre.INVALIDE

    if re.findall(r"<@!?(\d+)>", entree):

        logger.debug("Type détecté : mention membre")
        return TypeEntre.MENTION_MEMBRE

    if re.findall(r"<@&(\d+)>", entree):

        logger.debug("Type détecté : mention rôle")
        return TypeEntre.MENTION_ROLE

    if re.fullmatch(r"\d+", entree):

        logger.debug("Type détecté : ID Discord")
        return TypeEntre.ID

    logger.debug("Type détecté : nom")
    return TypeEntre.NOM