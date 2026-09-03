import sqlite3
import logging
from pathlib import Path
logger = logging.getLogger(__name__)




DR_DIR = next(
    p for p in Path(__file__).resolve().parents
    if p.name == "Discord"
)

DR_PAHT = DR_DIR / "guild.db"

def get_connection():
    return sqlite3.connect(DR_PAHT)

def init_databasse():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild(
                guild_id INTEGER PRIMARY KEY,
                joined_at TEXT NOT NULL
            )""")
            
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_role(
                guild_id INTEGER PRIMARY KEY,
                staff_role_id INTEGER,
                admin_role_id INTEGER,
                moderator_role_id INTEGER
            )""")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_config(
                guild_id INTEGER PRIMARY KEY,

                language TEXT NOT NULL DEFAULT 'français',
                prefix TEXT NOT NULL DEFAULT '?',
                
                error_time INTEGER NOT NULL DEFAULT 10,
                success_time INTEGER NOT NULL DEFAULT 10,
                warning_time INTEGER NOT NULL DEFAULT 12,
                info_time INTEGER NOT NULL DEFAULT 15,

                error_color TEXT NOT NULL DEFAULT "#ED4245",
                success_color TEXT NOT NULL DEFAULT "#57F287",
                warning_color TEXT NOT NULL DEFAULT "#FEE75C",
                info_color TEXT NOT NULL DEFAULT "#3498DB",

                updated_at TEXT
            )""")
        
    except sqlite3.Error:
        logger.exception(
            "Erreur lors de l'initialisation de la base de données."
        )

    finally:
        conn.close()
        
init_databasse()
