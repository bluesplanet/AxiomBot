from enum import Enum


class configtype(Enum):

    Language = "language"
    Prefix = "prefix"  



class configtype_staff(Enum):
    Staff = "staff"
    moderator = "moderator"
    admin = "admin"