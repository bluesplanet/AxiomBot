import discord
from utils.send import  send_message
from config import Type
import logging



logger = logging.getLogger(__name__)



async def creer_salon(ctx,nom,categorie,new_categorie):
    
    """
    Crée un salon textuel sur le serveur.

    Paramètres
    ----------
    ctx : commands.Context
        Contexte de la commande.

    nom : str
        Nom du salon à créer.

    categorie : discord.CategoryChannel | None
        Catégorie existante dans laquelle créer le salon.

    new_categorie : str | None
        Nom d'une nouvelle catégorie à créer.
        Utilisée seulement si aucune catégorie existante n'est fournie.

    Fonctionnement
    --------------
    - `categorie` → crée le salon dans cette catégorie.
    - `new_categorie` → crée une catégorie puis le salon dedans.
    - Aucun des deux → crée le salon sans catégorie.

    Retour
    ------
    None
        La fonction envoie directement un message de résultat.
    """

    try:
        
        logger.warning("✅ Entrée ")
        
        if nom is None:
            message = "Roles = None"
            await send_message(ctx,message,type=Type.ERROR)
            return
        

        if categorie:

            salon = await ctx.guild.create_text_channel(name = nom , category = categorie)
            message = f"**Salon créé : {salon.mention} | categorie : {categorie.name}**" 
            
        elif new_categorie:

            nom_categorie = await ctx.guild.create_category(name=new_categorie)
            salon = await ctx.guild.create_text_channel(name = nom , category = nom_categorie)
            message = f"**Salon créé : {salon.mention} | categorie créé : {nom_categorie.name}**"

        else:

            salon = await ctx.guild.create_text_channel(nom)
            message = f"**Salon créé : {salon.mention}**" 
        
        await send_message(ctx,message,type=Type.SUCCESS)

    except discord.Forbidden:
                   
        message = "Désolé, je n'ai pas les permissions nécessaires pour effectuer cette action."
        await send_message(ctx,message,type=Type.ERROR)
        logger.error(message)

    except discord.HTTPException:

        message = "Discord a rencontré une erreur."
        await send_message(ctx,message,type=Type.ERROR)
        logger.error(message)

    except discord.NotFound:

        message = "Désolé, le membre, le rôle ou la ressource demandée est introuvable."
        await send_message(ctx, message, type=Type.ERROR)
        logger.error(message)

    except Exception:

        message = "Erreur inattendue"
        await send_message(ctx,message,type=Type.WARNING)
        logger.exception(message)