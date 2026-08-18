import discord
import logging
import enum
from textwrap import dedent
from ..utils.send import send_message
from .view.create_embed_all import Pagination_permissions


logger = logging.getLogger(__name__)
AXIOM_BLUE = discord.Color.from_rgb(0, 170, 255)


# Fourmier des info generale concernent le role
async def role_general_embed(ctx,role: discord.Role,temps = None):

    logger.warning(
    f"Demande d'informations general du rôle | "
    f"Utilisateur:{ctx.author} | "
    f"Serveur:{ctx.guild.name} | "
    f"Rôle:{role.name} | "
    f"Expiration:{temps}"
    )

    embed = discord.Embed(
        title=f"Informations du rôle : {role.name}",
        colour=AXIOM_BLUE
    )

    embed.add_field(
        name=f"🔹Nom : {role.name}",
        value="",
        inline=False
    )

    embed.add_field(
        name=f"🔹ID : {role.id}",
        value="",
        inline=False
    )

    embed.add_field(
        name=f"🔹Couleur : {role.colour}",
        value="",
        inline=False
    )

    embed.add_field(
        name=f"🔹Position : {role.position}",
        value="",
        inline=False
    )

    embed.add_field(
        name=f"🔹Membres : {len(role.members)}/{len(ctx.guild.members)}",
        value="",
        inline=False
    )

    Mentionnable = "● Activé" if role.mentionable else "○ Désactivé"
    embed.add_field(
        name=f"🔹Mentionnable : {Mentionnable}",
        value="",
        inline=False
    )
    Affiché_séparément = "● Activé" if role.hoist else "○ Désactivé"
    embed.add_field(
        name=f"🔹Affiché séparément : {Affiché_séparément}",
        value="",
        inline=False
    )
    Role_gere_par_un_Bot = "● Activé" if role.managed else "○ Désactivé"
    embed.add_field(
        name=f"🔹Rôle géré par un Bot : {Role_gere_par_un_Bot}",
        value="",
        inline=False
    )
    Creation = discord.utils.format_dt(role.created_at, style="F")
    embed.add_field(
        name=f"🔹Création : {Creation}",
        value="",
        inline=False
    )


    embed.set_footer(
    text="AxiomBot • Powered by Blues Planet"
    )

    await ctx.send(
        embed = embed,
        delete_after = temps
        )



# Fourmier des info permission concernent le role 
async def role_permissions_embed(ctx, role: discord.Role, temps=60*7):


    logger.info(
    f"Demande d'informations sur les permissions du rôle | "
    f"Utilisateur:{ctx.author} | "
    f"Serveur:{ctx.guild.name} | "
    f"Rôle:{role.name} | "
    f"Expiration:{temps}"
    )


    permissions = []
    permission_all = []
   

    for num, (permission, valeur) in enumerate(role.permissions , start = 1):

        texte = permission.replace("_", " ").title()

        if valeur:
            permissions.append(f"● {texte}")
            permission_all.append(f"N°{num} {texte} (● Activée)")
        else:
            permission_all.append(f"N°{num} {texte} (○ Désactivée)")

    pags = [
        permissions[i:i + 10]
        for i in range(0,len(permissions),10)
    ]

    
    titre = "════════〔 PERMISSIONS "
    titre_all = dedent("""
    ╭─ Légende
    │ ● Permission activée
    │ ○ Permission désactivée
    ╰────────────>
    """

                       
    )

    pages = {
        "type" : "permissions",
        "pages" : pags,
        "pages_all" : permission_all
    }
    
    view = Pagination_permissions(
        pages,
        titre,
        titre_all,
        
    )
                 

    await ctx.send(
        embed = view.create_embed(),
        view = view,
        delete_after = temps
    )



async def role_membre_embed(ctx, role:discord.Role , temps=60*7):

    logger.info(
        f"Demande la liste des membre du role | "
        f"Utilisateur:{ctx.author} | "
        f"Serveur:{ctx.guild.name} | "
        f"Rôle:{role.name} | "
        f"Expiration:{temps}"
        )

    liste_membre = []
    liste = sorted([
        (membre,membre.joined_at)
        for membre in role.members
        ],
        key=lambda x: x[1] or discord.utils.utcnow(),
        reverse=True
    )   

    for membre,date in liste:
        date_at = discord.utils.format_dt(date, style="R")
        liste_membre.append(f"{membre} {date_at}")

    pags = [
        liste_membre[i:i + 20]
        for i in range(0,len(liste_membre),20)
    ]
    titre = f"◆ Membres — {role.name}"
    titre_all = f"◆ Liste complète — {role.name}"

    pages = {
        "type" : "membre",
        "pages" : pags,
        "pages_all" : liste_membre
    }

    view = Pagination_permissions(
        pages=pages,
        titre=titre,
        titre_all=titre_all
    )

    await ctx.send(
        embed = view.create_embed(),
        view = view,
        delete_after = temps
    )





async def role_stats_embed(role: discord.Role):

    humains = sum(
        1 for membre in role.members
        if not membre.bot
    )

    bots = sum(
        1 for membre in role.members
        if membre.bot
    )

    permissions = sum(
        1 for _, value in role.permissions
        if value
    )

    salons = sum(
        1 for channel in role.guild.channels
        if role in channel.overwrites
    )

    embed = discord.Embed(
        title=f"📈 Statistiques • {role.name}",
        colour=role.colour
    )

    embed.add_field(
        name="👥 Membres",
        value=f"`{len(role.members)}`",
        inline=True
    )

    embed.add_field(
        name="👤 Humains",
        value=f"`{humains}`",
        inline=True
    )

    embed.add_field(
        name="🤖 Bots",
        value=f"`{bots}`",
        inline=True
    )

    embed.add_field(
        name="🔐 Permissions",
        value=f"`{permissions}`",
        inline=True
    )

    embed.add_field(
        name="📁 Salons",
        value=f"`{salons}`",
        inline=True
    )

    embed.add_field(
        name="📅 Création",
        value=discord.utils.format_dt(
            role.created_at,
            style="D"
        ),
        inline=True
    )


    return embed




async def info_role_embed(ctx,info_type,role,temps):
    if role is None:
        message = "❌ Aucun rôle spécifié."
        await send_message(ctx,message,temps)
        return
    if  info_type== info_type.GENERAL:
        await role_general_embed(ctx,role,temps)
    elif info_type == info_type.MEMBERS:
        await role_membre_embed(ctx,role,temps)
    elif info_type == info_type.PERMISSIONS:
        await role_permissions_embed(ctx,role,temps)
    elif info_type == info_type.STATS:
        await ctx.send(embed=role_stats_embed(role))
    elif info_type == info_type.ALL:
        await role_general_embed(ctx,role,temps)
        await role_permissions_embed(ctx,role,temps)
        await ctx.send(embed=role_stats_embed(ctx,role,temps))