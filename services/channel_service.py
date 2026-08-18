import discord
from utils.messages import send_message 
from services.Rechercher.convert_type import convert_type

#La fonction pour cree un seule salon 
async def creer_un_salon(ctx,nom):
    try:
        print(nom)
        salon = await ctx.guild.create_text_channel(nom)

        message = f"Salon créé : {salon.mention}"
        await send_message(ctx,message)
        return salon
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)

    
#La fonction pour supprimer un seule salon
async def supprimer_un_salon(ctx,salon: discord.TextChannel):
    try:
        salon = salon.name

        await salon.delete(salon)

        message = f"Le salon {salon} a été supprimé."

        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)


#La fonction pour verrouiller un seule salon
async def verrouiller_un_salon(ctx):
    try:
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        
        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            overwrite=overwrite
        )
        message = "🔒 Salon verrouillé."
        await send_message(ctx, message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)


#La fonction pour deverrouiller un seule salon
async def deverrouiller_un_salon(ctx):
    try:
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
            
        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            overwrite=overwrite
        )
        message = "🔓 Salon déverrouillé."
        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)


#fonction - configure le salon pour ne plus etre accicible aux role par_default et autorise l'acces a une seule 
async def salon_config_acces(ctx,channel,role):
    try:
        await channel.set_permissions(
            channel.guild.default_role,
            view_channel=False
        )
        
        await channel.set_permissions(
            role,
            view_channel=True,
            send_messages=True
        )
        message = f"Les personnes qui ont le rôle {role.mention} peuvent accéder au salon {channel.mention}"
        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)

# fonction - Creer prend un liste(Mention discord) et les trasmet un a un aux fonction "salon_config_acces"
async def salon_config_acces_multi(ctx,channel,role,temps):
        # "convert_role" et une fonction qui trasforme des ID de Mention(Discorte) en Contexte puis retourne se contexte
        roles_liste = convert_type(ctx,role,temps)
        for roles in roles_liste:
            if roles:
                await salon_config_acces(ctx,channel,roles)