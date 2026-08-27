import sqlite3
import logging
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent / "database"
DB_DIR.mkdir(parents=True,exist_ok=True)

DB_PATH = DB_DIR / "basse.db"

logger = logging.getLogger(__name__)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings (
                guild_id INTEGER,
                welcome_channel_id INTEGER,
                bey_channel_id INTEGER,
                UNIQUE(guild_id)
            )
        """)

        conn.commit()

    except sqlite3.Error:
        logger.exception("Erreur lors de l'initialisation de la base de données.")

    finally:
        conn.close()


init_database()

def set(guild_id,welcome_channel_id = None,bey_channel_id = None):
    
    """
    Configure ou met à jour les salons associés à un serveur.

    Si le serveur n'existe pas dans la base de données, une nouvelle
    configuration est créée. S'il existe déjà, seuls les paramètres
    fournis sont mis à jour.

    Args:
        guild_id (int): ID du serveur Discord.
        welcome_channel_id (int | None): ID du salon de bienvenue à configurer.
        bey_channel_id (int | None): ID du salon BEY à configurer.

    Returns:
        bool: True si l'opération a réussi, sinon False.
    """
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if welcome_channel_id is not None:
            cursor.execute("""
                INSERT INTO guild_settings(guild_id,welcome_channel_id)
                VALUES(?,?)
                ON CONFLICT(guild_id)
                DO UPDATE SET welcome_channel_id = excluded.welcome_channel_id
            """,(guild_id,welcome_channel_id))

        if bey_channel_id is not None:
            cursor.execute("""
                INSERT INTO guild_settings(guild_id,bey_channel_id)
                VALUES(?,?)
                ON CONFLICT(guild_id)
                DO UPDATE SET bey_channel_id = excluded.bey_channel_id
            """,(guild_id,bey_channel_id))

        conn.commit()
        return True

    except sqlite3.Error:
            logger.exception(
                "Erreur SQLite lors de l'enregistrement du ticket."
            )
            return False
    
    finally:
        conn.close()

def get(guild_id):

    """
    Récupère la configuration des salons d'un serveur.

    Args:
        guild_id (int): ID du serveur Discord.

    Returns:
        dict | None: Dictionnaire contenant les IDs des salons configurés,
        ou None si aucune configuration n'existe ou si une erreur survient.
    
        {
            "welcome_channel_id": resultas[0],
            "bey_channel_id": resultas[1]
        }
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT welcome_channel_id, bey_channel_id
            FROM guild_settings
            WHERE guild_id = ?
        """,(guild_id,))

        resultas = cursor.fetchone()

        if resultas is None:
            return None

        bib = {
            "welcome_channel_id" : resultas[0],
            "bey_channel_id" : resultas[1]
            }
        
        return bib

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