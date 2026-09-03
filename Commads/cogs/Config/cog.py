from discord.ext import commands
from discord import app_commands
import discord
from utils.send import send_message
from Event.Data.Databasse import set
from config import Type
from data.config import set_config
from .utils.util_config_set import configtype, configtype_staff
from .Embed.language_embed import language_embed,LanguageView
from .Embed.Prefix_embed import PrefixModal
from data.role import set_role



class Config(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    @commands.hybrid_command(name="config_welcome",description="Configure le salon utilisé pour les messages de bienvenue.")
    @app_commands.describe(channel="Le salon où les messages de bienvenue seront envoyés.")
    async def config_welcom(self,ctx,channel : discord.TextChannel ):
        resultat = set(ctx.guild.id,welcome_channel_id=channel.id)

        if resultat:
            message = (
                f"✅ Le salon de bienvenue a été configuré sur {channel.mention}."
            )
            await send_message(ctx,message,type=Type.SUCCESS)

        else:
            message = "❌ Impossible de configurer le salon de bienvenue."
            await send_message(ctx,message,type=Type.ERROR)



    @commands.hybrid_command(name="config_bey",description="Configure le salon utilisé pour les messages de bienvenue.")
    @app_commands.describe(channel = "Configure le salon utilisé pour les messages de départ.")
    async def config_bey(self,ctx,channel : discord.TextChannel ):

        resultat = set(ctx.guild.id,bey_channel_id=channel.id)

        if resultat:
            message = (f"✅ Le salon de départ a été configuré sur {channel.mention}.")
            await send_message(ctx,message,type=Type.SUCCESS)

        else:
            message = "❌ Impossible de configurer le salon de départ."
            await send_message(ctx,message,type=Type.ERROR)


        
    @commands.hybrid_command(name="config_auto",description="Configure automatiquement la configuration du serveur.")
    async def config_auto(self,ctx):

        config = {
            "guild_id": ctx.guild.id,

            "language": "fr",
            "prefix": "?",

            "error_time": 10,
            "success_time": 10,
            "warning_time": 12,
            "info_time": 15,

            "error_color": "#ED4245",
            "success_color": "#57F287",
            "warning_color": "#FEE75C",
            "info_color": "#3498DB"
        }

        resultat = set_config(config)
        if resultat is True:
            message = "Configuration du serveur effectuée avec succès."
            await send_message(
                ctx,
                message,
                type=Type.SUCCESS
            )
        else:
            message = "Une erreur est survenue lors de la configuration du serveur."
            await send_message(
                ctx,
                message,
                type=Type.ERROR
            )



    @commands.hybrid_command(name="config_set" , description="Configure Manuelle la configuration du serveur.")
    async def config_set(self,ctx,type_config:configtype,):

        if type_config == configtype.Language:

            embed = language_embed(ctx)

            await ctx.send(
                embed=embed,
                view=LanguageView(),
                delete_after = 60,
                silent=True,
                ephemeral=True,
            )
            
        if type_config == configtype.Prefix:

            await ctx.interaction.response.send_modal(PrefixModal())



    @commands.hybrid_command(name="config_staff" , description="Configure le rôle du staff du serveur.")
    async def config_staff(self,ctx,role:discord.Role,type_config:configtype_staff):
        
        if type_config == configtype_staff.Staff:
            resultat = set_role(ctx.guild.id, staff_role_id=role.id)

            if resultat is True:
                message = f"**Le rôle du staff a été configuré ** {role.mention}."
                await send_message(ctx,message,type=Type.SUCCESS)

        elif type_config == configtype_staff.moderator:
            resultat = set_role(ctx.guild.id, moderator_role_id=role.id)

            if resultat is True:
                message = f"**Le rôle du modérateur a été configuré sur** {role.mention}."
                await send_message(ctx,message,type=Type.SUCCESS)

        elif type_config == configtype_staff.admin:
            resultat = set_role(ctx.guild.id, admin_role_id=role.id)

            if resultat is True:
                message = f"**Le rôle de l'administrateur a été configuré sur** {role.mention}."
                await send_message(ctx,message,type=Type.SUCCESS)

        else:
            message = "**Impossible de configurer le rôle du staff.**"
            await send_message(ctx,message,type=Type.ERROR)




async def setup(bot):
    await bot.add_cog(Config(bot))