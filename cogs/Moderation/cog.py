import discord
from discord.ext import commands
from discord import app_commands
from .kick import expulser
from .bannir import bannir
from .debannir import debannir
from .listban import listban
from .mute import mute
from .unmute import unmute
from .muteliste import muteliste


class Moderations(commands.Cog):

    def __init__(self,bot):
        self.bot = bot




    @commands.hybrid_command(name="membre_kick",description="Expulser un membre")
    @app_commands.describe(membre="Le membre à expulser",raison="La raison de l'expultion")
    async def expulser(self, ctx, membre: discord.Member,*,raison: str = "Aucune raison fournie"):
        await expulser(ctx,membre,raison)




    @commands.hybrid_command(name="membre_ban",description="Banir un membre")
    @app_commands.describe(membre="Menbre à banir",raison="Raison du ban")
    async def bannir(self, ctx, membre: discord.Member,*,raison: str = "Aucune raison fournie"):
        await bannir(ctx,membre,raison)       




    @commands.hybrid_command(name="membre_deban", description="Débannir un membre")
    @app_commands.describe(idmenbre="ID du Menbre",raison="Raison")
    async def debannir( self, ctx, idmenbre: str,raison: str = "Aucune raison fournie"):
        await debannir(ctx,idmenbre,raison)
    



    @commands.hybrid_command(name="membre_listban",description="list des membre monbre")
    async def listban(self, ctx):
        await listban(ctx)
       


    @commands.hybrid_command(name="membre_mute",description="Mute un membre")
    @app_commands.describe(membre="Le membre à mute",heure="Durée en heures",minute="Durée en minutes")
    async def mute(self, ctx, membre: discord.Member,raison: str = "Aucune raison fournie", heure: int = 0, minute: int = 0):
        await mute(ctx,membre,raison ,heure, minute)


    @commands.hybrid_command(name="membre_unmute", description="unMute un membre")
    @app_commands.describe(membre="Le membre à unmute")
    async def unmute(self, ctx, membre: discord.Member,raison: str = "Aucune raison fournie"):
        await unmute(ctx,membre,raison)


    @commands.hybrid_command(name="membre_muteliste",description="La liste des persone Mute")
    async def muteliste(self,ctx):
        muteliste(ctx)


async def setup(bot):
    await bot.add_cog(Moderations(bot))