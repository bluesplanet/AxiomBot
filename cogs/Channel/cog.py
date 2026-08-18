import discord
from config import Colors,Durations
from .utils.send import send_message
from discord import app_commands
from discord.ext import commands
from .creat import creer_salon
from .delete import supprimer_salon
from .verrouiller import salon_verrouiller
from .deverrouiller import salon_deverrouiller
from .config_acces import salon_config_acces_multi

class Channel(commands.Cog):
    def __init__(self,bot):
        self.bot = bot




    @commands.hybrid_command(name="salon_creer", description="Créer un salon")
    @app_commands.describe(nom="Nom du salon à créer",categorie="Catégorie existante dans laquelle créer le salon",new_categorie="Nom d'une nouvelle catégorie à créer")
    async def creer_salon(self, ctx, nom : str ,*, categorie:discord.CategoryChannel = None,new_categorie = None):
        await creer_salon(ctx,nom,categorie,new_categorie)




    @commands.hybrid_command(name="salon_supprimer", description="Supprimer un salon")
    @app_commands.describe(salon="Le salon à supprimer")
    async def supprimer_salon(self, ctx, salon: discord.TextChannel):
        await supprimer_salon(ctx,salon)
        



    @commands.hybrid_command(name="salon_verrouiller", description="Verrouiller un salon")
    async def verrouiller(self, ctx):
        await salon_verrouiller(ctx)

        


    @commands.hybrid_command(name="salon_deverrouiller", description="Déverrouiller un salon")
    async def deverrouiller(self, ctx):
        await salon_deverrouiller(ctx)
        


   
    @commands.hybrid_command(name="salon_config_acces",description="Configure l'accès d'un salon pour plusieurs rôles.")
    @app_commands.describe(channel = "Le salon à configurer.",roles="Les rôles qui auront accès au salon.")
    async def salon_config_acces(self,ctx,channel:discord.TextChannel,roles:str):
        await salon_config_acces_multi(ctx,channel,roles)

async def setup(bot):
    await bot.add_cog(Channel(bot))