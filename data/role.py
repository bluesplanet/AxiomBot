import sqlite3
import logging
from .data import get_connection

logger = logging.getLogger(__name__)

def set_role(guild_id,staff_role_id = None,admin_role_id = None,moderator_role_id = None):
    
    """
    Enregistre ou met à jour les rôles configurés pour un serveur.

    Si le serveur n'existe pas dans la table, une nouvelle entrée est créée.
    S'il existe déjà, les IDs des rôles sont mis à jour.

    Args:
        guild_id (int): ID du serveur Discord.
        staff_role_id (int | None): ID du rôle staff, ou None si non défini.
        admin_role_id (int | None): ID du rôle administrateur, ou None si non défini.
        moderator_role_id (int | None): ID du rôle modérateur, ou None si non défini.

    Returns:
        bool: True si l'enregistrement ou la mise à jour réussit.
        None: Si une erreur survient.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO guild_role(
            guild_id,
            staff_role_id,
            admin_role_id,
            moderator_role_id
        )
        VALUES(?,?,?,?)

        ON CONFLICT(guild_id)
        DO UPDATE SET
            staff_role_id = excluded.staff_role_id,
            admin_role_id = excluded.admin_role_id,
            moderator_role_id = excluded. moderator_role_id 
        """,(guild_id,staff_role_id,admin_role_id,moderator_role_id))

        conn.commit()
        return True

    except sqlite3.Error:
        logger.exception(
            "Erreur SQLite lors de la récupération du ticket."
        )
        return None

    except Exception:
        logger.exception(
            "Erreur inattendue lors de la récupération du ticket."
        )
        return None

    finally:
        conn.close()
    


def get_role(guild_id):

    """
    Récupère les IDs des rôles configurés pour un serveur.

    Args:
        guild_id (int): ID du serveur Discord.

    Returns:
        dict[str, int | None] | None:
            Dictionnaire contenant les IDs des rôles configurés :
            - "staff_role_id" : ID du rôle staff.
            - "admin_role_id" : ID du rôle administrateur.
            - "moderator_role_id" : ID du rôle modérateur.

            Retourne None si le serveur n'est pas trouvé ou si une erreur survient.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT staff_role_id,admin_role_id,moderator_role_id   
            FROM guild_role
            WHERE guild_id = ?
        """,(guild_id,))

        resultat = cursor.fetchone

        if resultat is None:
            return None
        
        resultas = {
            "staff_role_id" : resultat[0],
            "admin_role_id" : resultat[1],
            "moderator_role_id" : resultat[2]
        }
        return resultas

    except sqlite3.Error:
        logger.exception(
            "Erreur SQLite lors de la récupération du ticket."
        )
        return None

    except Exception:
        logger.exception(
            "Erreur inattendue lors de la récupération du ticket."
        )
        return None

    finally:
        conn.close()

    