import discord
from data.config import get_config

class Duration:
    """Durées d'affichage des messages temporaires d'AxiomBot."""
    def __init__(self,config,type):
        self.VALUES = config[f"{type}_time"]

        
class Color:
    """Palette officielle des couleurs d'AxiomBot."""
    def __init__(self,config,type):
        self.VALUES = discord.Colour.from_str(config[f"{type}_color"])
    
class Type:
    ERROR = "error"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"

    

