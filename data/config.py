import sqlite3
import logging
from .data import get_connection
from datetime import datetime, timezone
logger = logging.getLogger(__name__)




def set_config(config):

    """
    Enregistre ou met à jour la configuration d'un serveur.

    Si le serveur n'existe pas dans la base de données, une nouvelle
    configuration est créée avec les valeurs par défaut définies dans
    la table ``guild_config``.

    Si le serveur existe déjà, les valeurs fournies sont utilisées pour
    mettre à jour sa configuration. Une valeur ``None`` conserve la
    valeur actuellement enregistrée.

    Args:
        config (dict[str, str | int | None]):
            Dictionnaire contenant la configuration du serveur.
            Un exempl des configuration par-default

            {
                "guild_id": 123,
                "language": "en",
                "prefix": "?",
                "error_time": 10,
                "success_time": 10,
                "warning_time": 12,
                "info_time": 15,
                "error_color": "#ED4245",
                "success_color": "#57F287",
                "warning_color": "#FEE75C",
                "info_color": "#3498DB",
                "updated_at": None
            }

    Returns:
        bool:
            ``True`` si la configuration a été enregistrée ou mise à jour
            correctement.

        None:
            Si une erreur SQLite ou une autre erreur inattendue survient.
    """

    try:

        guild_id = config["guild_id"]
        
        conn = get_connection()
        cursor = conn.cursor()

        verification = get_config(guild_id)
        if verification is None:

            columns = []
            values = []

            for colum,value in config.items():
                columns.append(colum)
                values.append(value)

                
            placeholder = ", ".join(["?"]*len(values))
            column_names = ", ".join(columns)

            cursor.execute(f"""
                INSERT INTO guild_config ({column_names})
                VALUES ({placeholder})
            """,values)

        else:

            updates = []
            values = []
            
            for key,value in config.items():

                if key != "guild_id":

                    updates.append(f"{key} = ?")
                    values.append(value)

            values.append(guild_id)
            
            cursor.execute(
                f"""
                UPDATE guild_config
                SET {", ".join(updates)}
                WHERE guild_id = ?
                """,
                values
            )

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




def get_config(guild_id):

    """
    Récupère la configuration enregistrée d'un serveur.

    Args:
        guild_id (int): ID du serveur Discord.

    Returns:
        dict[str, str | int | None] | None:
            Dictionnaire contenant la configuration du serveur :

            - "guild_id" : ID du serveur.
            - "language" : Langue utilisée par le bot.
            - "prefix" : Préfixe des commandes.
            - "error_time" : Durée d'affichage des messages d'erreur.
            - "success_time" : Durée d'affichage des messages de succès.
            - "warning_time" : Durée d'affichage des messages d'avertissement.
            - "info_time" : Durée d'affichage des messages d'information.
            - "error_color" : Couleur des messages d'erreur.
            - "success_color" : Couleur des messages de succès.
            - "warning_color" : Couleur des messages d'avertissement.
            - "info_color" : Couleur des messages d'information.
            - "updated_at" : Date de dernière modification.

            Retourne None si le serveur n'existe pas ou en cas d'erreur.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT language,prefix,error_time,success_time,warning_time,info_time,error_color,success_color,warning_color,info_color,updated_at
            FROM guild_config
            WHERE guild_id = ?
        """,(guild_id,))    

        result = cursor.fetchone()
        
        if result is None:
            return None
        
        results ={
            "language" : result[0],
            "prefix" : result[1],
            "error_time" : result[2],
            "success_time" : result[3],
            "warning_time" : result[4],
            "info_time" : result[5],
            "error_color" : result[6],
            "success_color" : result[7],
            "warning_color" : result[8],
            "info_color" : result[9],
            "updated_at" : result[10]
        }

        return results
        
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