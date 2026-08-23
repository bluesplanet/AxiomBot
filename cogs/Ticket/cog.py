import discord
from .utils.send import send_message
from discord import app_commands
from config import Colors,Durations
from discord.ext import commands
from .creat import creat
from .delet import delet_staff , delet_utilisateur





class Ticket(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    @commands.hybrid_command(name="ticket_creat",description="Créer un ticket privé.")
    async def ticket(self, ctx):
        if ctx.author.guild_permissions.administrator:
            message = "Tu est un Admin , tu ne peux (Théoriquement) pas crée de Ticket"
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return
        await creat(ctx)
        


    @commands.hybrid_command(name="ticket_fermer",description="Fermer et supprimer le ticket actuel.")
    async def delet(self, ctx):
        
        await ctx.defer()

        if ctx.author.guild_permissions.administrator:
            await delet_staff(ctx)
            return

        staff_role = discord.utils.get(
            ctx.guild.roles,
            name="Staff"
        )

        if staff_role in ctx.author.roles:
            await delet_staff(ctx)
            return

        await delet_utilisateur(ctx)    


async def setup(bot):
    await bot.add_cog(Ticket(bot))    


    