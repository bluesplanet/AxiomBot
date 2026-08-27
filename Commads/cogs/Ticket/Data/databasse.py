import sqlite3
import logging
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "tiket.db"

logger = logging.getLogger(__name__)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket (
                guild_id INTEGER,
                channel_id INTEGER,
                author_id INTEGER,
                status TEXT NOT NULL DEFAULT 'active',
                UNIQUE(guild_id, author_id)
            )
        """)

        conn.commit()

    except sqlite3.Error:
        logger.exception("Erreur lors de l'initialisation de la base de données.")

    finally:
        conn.close()


init_database()




def set_tiket(guild_id : int, author_id : int, channel_id : int):

    """
    Enregistre un ticket dans la base de données.

    Exécute
    -------
    - Vérifie que les IDs sont des entiers positifs.
    - Enregistre le ticket dans SQLite.
    - Refuse un ticket déjà existant.
    - Ferme la connexion à la base de données.

    Paramètres
    ----------
    guild_id : int
        ID du serveur.

    author_id : int
        ID de l'auteur du ticket.

    channel_id : int
        ID du salon du ticket.

    Retour
    ------
    bool
        True si le ticket est enregistré.
        False si les IDs sont invalides, si le ticket existe déjà
        ou si une erreur SQLite survient.
    """

    if not all(
        isinstance(value, int) and value > 0
        for value in (guild_id, author_id, channel_id)
    ):
        logger.critical(
            "Tentative d'enregistrement d'un ticket avec des IDs invalides."
        )
        return False

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO ticket(
                guild_id,
                author_id,
                channel_id
            )
            VALUES (?, ?, ?)
        """, (guild_id, author_id, channel_id))

        conn.commit()

        # 1 = insertion effectuée, 0 = insertion ignorée
        if cursor.rowcount == 0:
            logger.warning(
                "Ticket déjà existant | guild=%s | author=%s",
                guild_id,
                author_id
            )

            return False
        

        return True

    except sqlite3.Error:
        logger.exception(
            "Erreur SQLite lors de l'enregistrement du ticket."
        )
        return False

    finally:
        conn.close()




def get_tiket(guild_id, author_id=None, channel_id=None):

    """
    Récupère les informations d'un ticket.

    Exécute
    -------
    - Recherche un ticket par son auteur ou son salon.
    - Récupère l'ID correspondant et son statut.

    Paramètres
    ----------
    guild_id : int
        ID du serveur.

    author_id : int, optionnel
        ID de l'auteur du ticket.

    channel_id : int, optionnel
        ID du salon du ticket.

    Retour
    ------
    tuple[int, str] | None
        Retourne l'ID et le statut du ticket.
        Retourne None si aucun ticket correspondant n'existe.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if author_id is not None:
            cursor.execute("""
                SELECT channel_id, status
                FROM ticket
                WHERE guild_id = ? AND author_id = ?
            """, (guild_id, author_id))

        elif channel_id is not None:
            cursor.execute("""
                SELECT author_id, status
                FROM ticket
                WHERE guild_id = ? AND channel_id = ?
            """, (guild_id, channel_id))

        else:
            return None

        result = cursor.fetchone()

        return result if result else None

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

    

    
def update_ticket(guild_id,author_id = None,channel_id = None,status = None):

    """
    Met à jour les informations d'un ticket dans la base de données.

    Exécute
    -------
    - Met à jour le statut du ticket si ``status`` est fourni.
    - Met à jour l'ID du salon si ``author_id`` est fourni.
    - Enregistre les modifications dans la base de données.

    Paramètres
    ----------
    guild_id : int
        ID du serveur auquel appartient le ticket.

    channel_id : int
        ID actuel ou nouvel ID du salon du ticket.

    status : str, optionnel
        Nouveau statut du ticket, par exemple ``"active"`` ou
        ``"corbeille"``.

    author_id : int, optionnel
        ID de l'auteur du ticket. Utilisé pour retrouver son ticket
        et mettre à jour son ``channel_id``.

    Retour
    ------
    bool
        True si la mise à jour est exécutée.
        False si aucun paramètre de mise à jour n'est fourni.
    """
     
    try:

        conn = get_connection()
        cursor = conn.cursor()
        
        if status is not None:
            cursor.execute("""
                UPDATE ticket
                SET status = ?
                WHERE guild_id = ? AND channel_id = ?
            """, (status, guild_id, channel_id))

        elif author_id is not None:
            cursor.execute("""
                UPDATE ticket
                SET channel_id = ?
                WHERE guild_id = ? AND  author_id = ?;
            """,(channel_id,guild_id,author_id))

        else:
            logger.warning(
                "update_ticket appelée sans status ni author_id | guild=%s channel=%s",
                guild_id,
                channel_id
            )
            return False

    
        conn.commit()
        return True
    except sqlite3.Error:
        logger.exception("Erreur lors de la récupération du ticket.")
        return None

    except Exception:
        logger.exception("Erreur inattendue lors de la récupération du ticket.")
        return None

    finally:
        conn.close()

