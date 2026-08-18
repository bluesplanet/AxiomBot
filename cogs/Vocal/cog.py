import discord
from discord.ext import commands
from discord import app_commands
from .creat import creer_vocal
from .delet import supprimer_vocal
from .renommer import renommer_vocal
from .limite import limite_vocal
from .deconnecter import deconnecter_vocal
from .deplacer import deplacer_vocal




class Vocal(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    


    @commands.hybrid_command(name="voice_creat", description="Créer un salon")
    @app_commands.describe(nom="Nom du salon vocal à créer",categorie="Catégorie existante dans laquelle créer le salon",new_categorie="Nom d'une nouvelle catégorie à créer")
    async def creer_salon(self, ctx, nom : str ,*, categorie:discord.CategoryChannel = None,new_categorie = None):
        await creer_vocal(ctx,nom,categorie,new_categorie)




    @commands.hybrid_command(name="voice_delet", description="Supprimer un salon vocal")
    @app_commands.describe(salon="Le salon vocal à supprimer")
    async def supprimer_vocal(self,ctx,salon: discord.VoiceChannel):
        await supprimer_vocal(ctx,salon)




    @commands.hybrid_command(name="voice_renommer", description="Renommer un vocal")
    @app_commands.describe(salon="Le salon vocal à renommer",nouveau_nom="Le nouveau nom du salon vocal")
    async def renommer_vocal(self,ctx,salon: discord.VoiceChannel,nouveau_nom: str = "Nouveaux salon"):
        await renommer_vocal(ctx,salon,nouveau_nom)
        



    @commands.hybrid_command(name="voice_limite", description="Limiter les places")
    @app_commands.describe(salon="Le salon vocal à modifier",limite="Nombre maximum de membres autorisés")
    async def limite_vocal(self,ctx,salon: discord.VoiceChannel,limite: int):
        await limite_vocal(ctx,salon,limite)




    @commands.hybrid_command(name="voice_deconnecter", description="Déconnecte un membre du vocal")
    @app_commands.describe(membre="Le membre à déconnecter du salon vocal")
    async def deconnecter_vocal(self, ctx, membre: discord.Member):
        await deconnecter_vocal(ctx,membre)




    @commands.hybrid_command(name="voice_deplacer" , description="Déplacer un membre dans un salon vocal")
    @app_commands.describe(membre="Le membre à déplacer",salon="Le salon vocal de destination")
    async def deplacer_vocal(self,ctx,membre: discord.Member,salon: discord.VoiceChannel):
        await deplacer_vocal(ctx,membre,salon)




async def setup(bot):
    await bot.add_cog(Vocal(bot))