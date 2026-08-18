import logging
import colorlog

# création du Handler (Affichage dans le console)
handler = colorlog.StreamHandler()

# Foramt des logs
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s  | %(asctime)s | %(name)s:%(lineno)d | %(funcName)s() | %(message)s",
    
    datefmt="%Y-%m-%d",
    log_colors={
        "DEBUG": "white",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
)

# On donne le format au Handler
handler.setFormatter(formatter)

# Logger principal
logger = logging.getLogger()

# Niveau minimum des logs
logger.setLevel(logging.DEBUG)

# Évite d'ajouter plusieurs fois le même handler
if not logger.handlers:
    logger.addHandler(handler)
