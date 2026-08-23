import discord
from .Data.databasse import set_tiket
from .utils.send import send_message
from config import Durations,Colors
from .Data.databasse import get_tiket,update_ticket
from.corbaille import restor_corbaille
import logging



logger = logging.getLogger(__name__)




async def creat(ctx):

    """
    Crée un ticket privé pour l'utilisateur.

    Exécute
    -------
    - Crée la catégorie si nécessaire.
    - Crée le salon privé.
    - Enregistre le ticket dans la base de données.
    - Supprime le salon si l'enregistrement échoue.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    Retour
    ------
    None
        Aucun retour.
        
    """

    try:
        ancien_channel = True
        logger.warning("✅ Entrée ")
        liste = get_tiket(ctx.guild.id,ctx.author.id)
        if liste:
            if liste[1] == "corbeille":
                ancien_channel = await restor_corbaille(ctx,liste[0])

        categorie = discord.utils.get(ctx.guild.categories,name="🎫・TICKETS")
        
        if categorie is None:
            categorie = await ctx.guild.create_category("🎫・TICKETS")



        async def creatx(ctx):

            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            ctx.author: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            
            }

            salon = await ctx.guild.create_text_channel(
                name=f"ticket-{ctx.author.name}",
                category=categorie,
                overwrites=overwrites,
                topic=(
                    f"🎫 Ticket de {ctx.author} | "
                    f"Créé par AxiomBot"
                )
            )

            return salon



        if ancien_channel is None:
            salon  = await creatx(ctx)
            update_ticket(ctx.guild.id, author_id = ctx.author.id, channel_id = salon.id)

            message = (
                f"♻️ Ton ancien ticket n'était plus disponible.\n\n"
                f"Un nouveau ticket a été créé automatiquement ici "
                f"👉 {salon.mention}"
            )
            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)
            return


        salon = await creatx(ctx)

        statu = set_tiket(ctx.guild.id,ctx.author.id,salon.id)
        if statu is False :
            await salon.delete()
    
            message = (
                "**Ticket déjà existant.**\n"
                "Cette action a déjà été enregistrée pour votre compte.\n\n"
                "**Avis AxiomBot :** la répétition excessive de cette action "
                "peut être détectée comme un comportement abusif et entraîner "
                "une limitation temporaire de certaines commandes du bot."
            )

            await send_message(ctx,message,color=Colors.WARNING,temps=Durations.WARNING)
            return
        
        message = f"🎫 Ton ticket a bien été créé ici :\n\n👉 {salon.mention}"
        await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)

    except discord.Forbidden:
                    
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        await send_message(ctx,message,color=Colors.ERROR , temps = Durations.ERROR)
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        await send_message(ctx,message,color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except discord.NotFound:

        messages = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        await send_message(ctx, messages, color=Colors.ERROR ,temps = Durations.ERROR)
        logger.error(message)

    except Exception:
            message = "Erreur inattendue"
            await send_message(ctx,message,color=Colors.WARNING,temps = Durations.WARNING)
            logger.exception(message)


