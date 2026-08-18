import discord
from datetime import timedelta
from utils.messages import send_message

async def expulser_un_membre(ctx,membre,raison):
    try:
        await ctx.defer()
        await membre.kick(reason=raison)
        message = f"{membre.mention} a été expulsé. Raison: {raison}"
        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message) 
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)



async def bannir_un_membre(ctx,membre,raison):
    try:
        await ctx.defer()
        await membre.ban(reason=raison)
        message = f"{membre.mention} a été banni. Raison: {raison}"
        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message) 
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)



async def debannir_un_membre(ctx,idmenbre,raison):
    try:
        await ctx.defer()
        user = await ctx.bot.fetch_user(int(idmenbre))
        await ctx.guild.unban(user, reason=raison)
        message = f"{user} a été débanni. Raison : {raison}"
        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message) 
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)



async def listban_des_membres_banis(ctx):
    try:
        await ctx.defer()
        bans = [entry async for entry in ctx.guild.bans()]
        if len(bans) == 0:
            message = "Liste vide"
            await ctx.send(message)
            return
        for entr in bans:
            message = f"Nom : {entr.user.name} | ID : {entr.user.id}"
            await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)



async def mute_un_membre(ctx,membre,raison ,heure, minute):
    try:
        await ctx.defer()
        if heure == 0 and minute == 0:
            message = "❌ Tu dois mettre une durée supérieure à 0."
            await send_message(ctx,message)
            return
        duree = timedelta(
            hours=heure,
            minutes=minute
        )

        if duree.total_seconds() > 28 * 24 * 60 * 60:
            message = f"❌ La durée maximale est de 28 jours."
            await send_message(ctx,message)
            return
        await membre.timeout(
            duree,
            reason=raison
        )
        message = f"{membre.mention} a été mute pendant {heure}h {minute}min."
        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)



async def unmute_un_membre(ctx,membre,raison):
    try:
        await ctx.defer()
        await membre.timeout(
        None,
        reason=raison
        )

        message = f"🔊 Le timeout de {membre.mention} a été retiré. Raison: {raison}"
        await send_message(ctx,message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)   
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)



async def liste_des_membre_mute(ctx):
    try:
        await ctx.defer()
        message = f"📋 Membres actuellement en timeout\n\n"
        nombre = 0
        for membre in ctx.guild.members:

            if membre.timed_out_until is None:
                continue
            if membre.timed_out_until <= discord.utils.utcnow():
                continue
            nombre += 1

            message += (
                f"👤 Membre : {membre.mention}\n"
                f"🆔 ID : {membre.id}\n"
                f"⏰ Fin : {membre.timed_out_until.strftime('%d/%m/%Y à %H:%M UTC')}\n\n"
            )

        if nombre == 0:
            await send_message(
                ctx,
                "➡️✅ Aucun membre n'est actuellement en timeout."
            )
            return

        message += f"📊 Total : {nombre} membre(s)."
        await send_message(ctx, message)
    except discord.Forbidden:
        message = "❌ erreur ,verifier les permission du Bot" 
        await send_message(ctx,message)       
    except discord.HTTPException:
        message = "❌ Discord a rencontré une erreur."
        await send_message(ctx,message)