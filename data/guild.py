import sqlite3
import logging
from datetime import datetime, timezone
from .data import get_connection
logger = logging.getLogger(__name__)



def set_guild(guild_id):

    """
    Ajoute un serveur à la base de données s'il n'est pas déjà enregistré.

    La date d'ajout est enregistrée automatiquement en UTC.

    Args:
        guild_id (int): ID du serveur Discord.

    Returns:
        bool: True si l'enregistrement réussit, sinon False.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO guild(
                guild_id,
                joined_at
            )
            VALUES(?,?)
            
        """,(guild_id,datetime.now(timezone.utc).isoformat()))

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



def get_guild(guild_id):

    """
    Récupère la date d'enregistrement d'un serveur.

    Args:
        guild_id (int): ID du serveur Discord.

    Returns:
        str | None: Date d'enregistrement au format ISO 8601,
            ou None si le serveur n'est pas enregistré ou en cas d'erreur.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT joined_at
            FROM guild
            WHERE guild_id = ?
        """,(guild_id,))

        result = cursor.fetchone()

        return result[0] if result else None

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
