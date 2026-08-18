import discord


async def membre_plusieurs(ctx,texte,objet,temps):

    embed = discord.Embed(
        title="👥 Plusieurs membres trouvés",
        description=f"Plusieurs membres correspondent à **{texte}**.",
        color=discord.Color.orange()
    )

    for candidat, score in objet["resultat"][:20]:
        embed.add_field(
            name=candidat.display_name,
            value=f"ID : `{candidat.id}`\nConfiance : **{score*100:.2f}%**",
            inline=False
        )

    embed.set_footer(
        text="Utilisez une mention ou un ID pour sélectionner le bon membre."
    )

    await ctx.send(
        embed=embed,
        delete_after = temps
    )


async def membre_propositions(ctx,texte,objet,temps):
    embed = discord.Embed(
        title="🔎 Membres similaires",
        description=f"Aucun membre exact trouvé pour **{texte}**.",
        color=discord.Color.gold()
    )

    for candidat, score in objet["resultat"][:20]:
        embed.add_field(
            name=candidat.display_name,
            value=f"ID : `{candidat.id}`\nConfiance : **{score*100:.2f}%**",
            inline=False
        )

    embed.set_footer(
        text="Vous pouvez réutiliser ces informations pour relancer la commande."
    )

    await ctx.send(
        embed=embed,
        delete_after = temps
    )


async def membre_introuvable(ctx,texte,temps):
    embed = discord.Embed(
        title="❌ Aucun membre trouvé",
        description=f"Aucun membre ne correspond à **{texte}**.",
        color=discord.Color.red()
    )

    embed.set_footer(
        text="Essayez une mention, un ID Discord ou un nom plus précis."
    )

    await ctx.send(
        embed=embed,
        delete_after = temps
    )


async def role_plusieurs(ctx,texte,objet,temps):

    embed = discord.Embed(
        title="🎭 Plusieurs rôles trouvés",
        description=f"Plusieurs rôles correspondent à **{texte}**.",
        color=discord.Color.orange()
    )

    for candidat, score in objet["resultat"][:20]:
        embed.add_field(
            name=candidat.name,
            value=f"ID : `{candidat.id}`\nConfiance : **{score*100:.2f}%**",
            inline=False
        )

    embed.set_footer(
        text="Utilisez un ID ou une mention du rôle."
    )

    await ctx.send(
        embed=embed,
        delete_after = temps
        )


async def role_propositions(ctx,texte,objet,temps):

    embed = discord.Embed(
        title="🔎 Rôles similaires",
        description=f"Aucun rôle exact trouvé pour **{texte}**.",
        color=discord.Color.gold()
    )

    for candidat, score in objet["resultat"][:20]:
        embed.add_field(
            name=candidat.name,
            value=f"ID : `{candidat.id}`\nConfiance : **{score*100:.2f}%**",
            inline=False
        )

    embed.set_footer(
        text="Vous pouvez réutiliser ces informations pour relancer la commande."
    )

    await ctx.send(
            embed=embed,
            delete_after = temps
        )


async def role_introuvable(ctx,texte,temps):
    embed = discord.Embed(
        title="❌ Aucun rôle trouvé",
        description=f"Aucun rôle ne correspond à **{texte}**.",
        color=discord.Color.red()
    )

    embed.set_footer(
        text="Essayez une mention, un ID Discord ou un nom plus précis."
    )

    await ctx.send(
            embed=embed,
            delete_after = temps
            )