import logging
import discord
from enum import Enum
from discord import app_commands
from discord.ext import commands
from .utils.send import send_message
from .ajouter import ajouter
from .retirer import retirer
from .renomer import renommer
from .supprimer import supprimer
from .info_role.info import info_role_embed




logger = logging.getLogger(__name__)



class Ouiounon(Enum):
    OUI = "Oui"
    NON = "Non"


class info_type(Enum):
    GENERAL = "general"          
    PERMISSIONS = "permissions"  
    MEMBERS = "members"                
    STATS = "stats"


class Role(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    @commands.hybrid_command(name="role_add",description="Ajouter un rôle à un ou plusieurs membres")
    @app_commands.describe(membres="Membre(s) à qui ajouter le rôle", role="Rôle à ajouter", etendre="Étendre la recherche aux rôles", temps="Durée avant suppression du message de confirmation (en secondes)")
    async def ajout_role_command(self,ctx,membres:str,role:str,etendre:Ouiounon=Ouiounon.NON,temps:int=None):
        try:
            await ajouter(ctx,membres,role,etendre,temps)
        except Exception :
            logger.exception("Une erreur s'est produite lors de l'ajout du rôle.")
            await send_message(ctx,"❌ Une erreur s'est produite lors de l'ajout du rôle.",temps)




    @commands.hybrid_command(name="role_remove",description="Retirer un rôle à un ou plusieurs membres")
    @app_commands.describe(membres="Membre(s) à qui retirer le rôle", role="Rôle à retirer", etendre="Étendre la recherche aux rôles", temps="Durée avant suppression du message de confirmation (en secondes)")
    async def retirer_role_command(self,ctx,membres:str,role:str,etendre:Ouiounon=Ouiounon.NON,temps:int=None):
        try:
            await retirer(ctx,membres,role,etendre,temps)
        except Exception :
            logger.exception("Une erreur s'est produite lors du retrait du rôle .")
            await send_message(ctx,"❌ Une erreur s'est produite lors du retrait du rôle.",temps)




    @commands.hybrid_command(name = "renommer_role", description="Renommer un rôle")
    @app_commands.describe(role = "Rôle à renommer", nouveau_nom = "Nouveau nom du rôle", temps="Durée avant suppression du message de confirmation (en secondes)")
    async def renommer_role(self,ctx,role:discord.Role,nouveau_nom:str,temps:int=None):
        try:
            await renommer(ctx,role,nouveau_nom,temps)
        except Exception :
            logger.exception("Une erreur s'est produite lors du renommage du rôle.")
            await send_message(ctx,"❌ Une erreur s'est produite lors du renommage du rôle.",temps)




    @commands.hybrid_command(name = "supprimer_role", description="Supprimer un rôle")
    @app_commands.describe(role = "Rôle à supprimer", temps="Durée avant suppression du message de confirmation (en secondes)")
    async def supprimer_role(self,ctx,role:discord.Role,temps:int=None):
        try:
            
            await supprimer(ctx,role,temps)
        except Exception :
            logger.exception("Une erreur s'est produite lors de la suppression du rôle.")




    @commands.hybrid_command(name = "info_role", description="Des informations sur un rôle")
    @app_commands.describe(info_type = "Informations sur le rôle")
    async def info_role(self,ctx,role:discord.Role,info_type:info_type=info_type.GENERAL,*,temps:int=None):
        try:

            await ctx.defer()
            await info_role_embed(ctx,info_type,role,temps)

        except Exception :
            logger.exception("Une erreur s'est produite lors de l'affichage des informations sur le rôle.")
            await send_message(ctx,"❌ Une erreur s'est produite lors de l'affichage des informations sur le rôle.",temps)




async def setup(bot):
    await bot.add_cog(Role(bot))


