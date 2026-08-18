import os
import discord
import logging
import utils.logger_config
from dotenv import load_dotenv
from discord.ext import commands


logger = logging.getLogger(__name__)




load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")



class MonBot(commands.Bot):
    async def setup_hook(self):
        cogs = [
            "cogs.Teste",
            "cogs.Roles.cog",
            "cogs.Channel.cog",
            "cogs.Moderation.cog",
            "cogs.Vocal.cog"

        ]

        logger.info("Nombre de cogs détecter = %s ",len(cogs))


    
        try:
            for index , cog in enumerate(cogs , start=1):

                await self.load_extension(cog)
                logging.info("Cog N° = %s/%s charger",index,len(cogs))


            logger.info("Chargement cogs terminer | %s/%s",index,len(cogs))

        except Exception:

            logger.exception("Erreur sur le chargement du %s",cog)

        try:

            synced = await self.tree.sync()


            logger.info("Mombre de Commades détecter  = %s",len(synced))


            for index ,cogs in enumerate(synced , start= 1):
                logger.info("Commande synchronisée : %s N° :%s",cogs,index)
                
        except discord.HTTPException:
            logger.error("Discord a refusé la synchronisation")

        except Exception:
            logger.exception("Erreur inconnue pendant la synchronisation")

bot = MonBot(
    command_prefix="?",
    intents=discord.Intents.all()
)

@bot.event
async def on_interaction(interaction):
    print("INTERACTION REÇUE :", interaction.type)
    
@bot.event
async def on_ready():
    logger.info("Bot connécter | bot name = %s",bot.user)
    

        
    
bot.run(TOKEN)