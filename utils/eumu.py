from enum import Enum

class Ouiounon(Enum):
    OUI = "Oui"
    NON = "Non"


class info_type(Enum):
    GENERAL = "general"          
    PERMISSIONS = "permissions"  
    MEMBERS = "members"          
    CHANNELS = "channels"         
    STATS = "stats"             
                  