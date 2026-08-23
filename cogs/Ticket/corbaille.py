import discord
import logging
from .utils.send import send_message
from .Data.databasse import update_ticket,get_tiket
from config import Colors,Durations




logger = logging.getLogger(__name__)




async def remove_corbaille(ctx,channel):

    """
    Déplace un ticket dans la corbeille.

    Exécute
    -------
    - Recherche la catégorie « Corbail ».
    - La crée automatiquement si elle n'existe pas.
    - Rend la catégorie invisible pour @everyone.
    - Autorise le propriétaire du serveur à accéder à la catégorie.
    - Déplace le ticket dans la corbeille et synchronise ses permissions.
    - Vérifie que le ticket existe dans la base de données.
    - Vérifie que le ticket n'est pas déjà dans la corbeille.
    - Met à jour le statut du ticket en « corbeille ».
    - Envoie un message de confirmation.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte Discord de la commande.

    channel : discord.TextChannel
        Salon du ticket à déplacer dans la corbeille.

    Retour
    ------
    None
        La fonction ne retourne aucune valeur.
    """

    try:
        categorie = discord.utils.get(
            ctx.guild.categories,
            name="Corbail"
        )

        if categorie is None:
            categorie = await ctx.guild.create_category("Corbail")

        await categorie.set_permissions(
            ctx.guild.default_role,
            view_channel=False
        )

        await categorie.set_permissions(
            ctx.guild.owner,
            view_channel=True
        )
        
        await channel.edit(
            category=categorie,
            sync_permissions=True
        )


        verification =  get_tiket(ctx.guild.id,channel_id=channel.id)
        if verification[1] == "corbeille":
            message =  "🗑️ Le ticket est déjà dans la corbeille."
            await send_message(ctx,message,color=Colors.ERROR,temps=Durations.ERROR)
            return

        update_ticket(ctx.guild.id, channel_id = channel.id, status = "corbeille")

        message = "🗑️ Le ticket a été déplacé dans la corbeille"
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
    




async def restor_corbaille(ctx,channel_id):

    try:
        categorie = discord.utils.get(ctx.guild.categories,name="🎫・TICKETS")

        if categorie is None:
            categorie = await ctx.guild.create_category("🎫・TICKETS")

        channel = ctx.guild.get_channel(channel_id)

        if channel:
              
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

            
            channel = await channel.edit(
            category=categorie,
            overwrites=overwrites
            )

            update_ticket(ctx.guild.id,channel_id=channel_id,status="active")

            message = (
                f"♻️ Ton ticket a été restauré avec succès :\n\n "
                f"👉 {channel.mention}\n\n"
                f"Tu peux de nouveau y accéder."
            )

            await send_message(ctx,message,color=Colors.SUCCESS,temps=Durations.SUCCESS)

            return True
        else:
            return None


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



