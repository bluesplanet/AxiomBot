import sqlite3
import logging
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "warns.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()




logger = logging.getLogger(__name__)




def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():

    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS warns(
                guild_id INTEGER NOT NULL,
                membre_id INTEGER NOT NULL,
                warn_count INTEGER NOT NULL DEFAULT 0,
                UNIQUE(guild_id, membre_id)
            )
        """)

        conn.commit()

    except sqlite3.Error:
        logger.exception("Erreur lors de l'initialisation de la base de données.")

    finally:
        conn.close()


init_database()

def  check_warnings(guild_id,membre_id):

    """
    Vérifie le nombre d'avertissements d'un membre sur un serveur.

    Si le membre possède 3 avertissements ou plus, la ligne est
    supprimée de la base de données et la fonction retourne True.

    Sinon, la ligne est conservée et la fonction retourne False.

    Args:
        guild_id (int): Identifiant du serveur Discord.
        membre_id (int): Identifiant du membre Discord.

    Returns:
        bool:
            True si le membre atteint 3 avertissements ou plus,
            False sinon ou en cas d'erreur SQLite.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        
        cursor.execute("""
            SELECT warn_count
            FROM warns
            WHERE guild_id = ? AND membre_id = ?
        """, (guild_id,membre_id))

        result = cursor.fetchone()

        if result is None:
            conn.close()
            return False

        warm_count = result[0]

        if warm_count >= 3:
            cursor.execute("""
                DELETE FROM warns
                WHERE guild_id = ? AND membre_id = ?
            """,(guild_id,membre_id))
            conn.commit()
            conn.close()
            return True

        conn.commit()
        conn.close()
        return False
        
        
    except sqlite3.Error:
        logger.exception(
            "Erreur SQLite lors de l'enregistrement du ticket."
        )
        return False
        
    finally:
        conn.close()


def set_warm(guild_id,membre_id):

    """
    Ajoute un avertissement à un membre.

    Si le membre n'a aucun avertissement enregistré, une nouvelle
    ligne est créée avec un compteur à 1. Si une ligne existe déjà,
    le compteur est augmenté de 1.

    Après l'ajout, la fonction vérifie automatiquement si le membre
    atteint 3 avertissements.

    Args:
        guild_id (int): Identifiant du serveur Discord.
        membre_id (int): Identifiant du membre Discord.

    Returns:
        bool:
            True si le membre atteint 3 avertissements ou plus,
            False si le seuil n'est pas atteint ou en cas d'erreur SQLite.
    """
     
    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO warns (guild_id, membre_id, warn_count)
            VALUES (?, ?, 1)
            ON CONFLICT(guild_id, membre_id)
            DO UPDATE SET warn_count = warn_count + 1
        """,(guild_id,membre_id))

        conn.commit()

        return check_warnings(guild_id,membre_id)



    except sqlite3.Error:
            logger.exception(
                "Erreur SQLite lors de l'enregistrement du ticket."
            )
            return False
    
    finally:
        conn.close()
