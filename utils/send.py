import discord
from textwrap import dedent
from config import Durations,Colors


AXIOM_BLUE = discord.Colour.blue()


async def send_message(ctx, message,color = Colors.BOT, temps=None,destinataire=None):

    """
    Envoie un message sous forme d'Embed.

    La fonction gère automatiquement les deux types de commandes :
    - commandes Slash / Hybrid via une Interaction ;
    - commandes préfixées classiques.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    message : str
        Contenu du message à afficher dans la description de l'Embed.

        `dedent()` est utilisé pour supprimer les indentations
        inutiles dans les messages écrits sur plusieurs lignes.

    temps : int | None, optional
        Durée en secondes avant la suppression du message.

        Exemple :
            temps=10
            → le message est supprimé après 10 secondes.

        Si `None`, le message n'est pas automatiquement supprimé.

    Fonctionnement
    --------------
    Si la commande provient d'une Interaction :
        - le message est envoyé en réponse éphémère ;
        - seul l'utilisateur ayant effectué la commande peut le voir.

    Si la commande est une commande préfixée :
        - le message est envoyé normalement dans le salon ;
        - un avertissement concernant les commandes Slash est ajouté.

    Retour
    ------
    None
        La fonction envoie directement le message et ne retourne rien.

    Exemple
    -------
    ```python
    await send_message(
        ctx,
        "❌ Désolé, je n'ai pas les permissions nécessaires.",
        temps=10
    )
    ```

    Le message sera automatiquement transformé en Embed.

    Notes
    -----
    Tous les anciens appels à `send_message()` restent compatibles.
    Il n'est donc pas nécessaire de modifier chaque endroit du bot
    où cette fonction est déjà utilisée.
    """

    # Supprime les indentations inutiles du texte.
    message = dedent(message)

    # Création de l'Embed.
    embed = discord.Embed(
        description=message,
        colour=color
    )

    # ---------------------------------------------------------
    # Commande Slash / Hybrid
    # ---------------------------------------------------------
    if destinataire:
        await destinataire.send(
            embed=embed,
            silent=True,
            delete_after=temps
        )
    else:
        if ctx.interaction:

            await ctx.send(
                embed=embed,
                ephemeral=True,
                silent=True,
                delete_after=temps
            )

    # ---------------------------------------------------------
    # Commande préfixée
    # ---------------------------------------------------------

        else:
            embed.description += (
                "\n\n"
                "⚠️ Privilégie les commandes slash (/), "
                "elles sont recommandées."
            )

            await ctx.send(
                embed=embed,
                delete_after=temps
            )