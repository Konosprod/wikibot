import discord
from discord.ext import commands
import logging
import atexit
from wikihandler import Wikihandler
import locale
import time

logging.basicConfig(level=logging.DEBUG)

#use fr_FR on linux
locale.setlocale(locale.LC_ALL, "fra")


bot = commands.Bot(command_prefix="/")
wh = Wikihandler()

@bot.event
async def on_ready():
    await bot.edit_profile(username="Le saviez vous ?")
    await bot.change_presence(game=discord.Game(name="/lsvaide"))

@bot.command(no_pm=True)
async def lsvaide():
    help=("Un bot qui permet d'obtenir les informations du jour sur wikipedia\n\n"
          "Commandes:\n"
          "\t/lsvaide       : Affiche l'aide\n"
          "\t/lsvimage   : Obtient l'image du jour\n"
          "\t/lsvlumiere : Obtient l'article du jour\n"
          "\t/lsvtrivia      : Affiche les trivias du jour\n"
          "\t/lsvrand       : Affiche une page au hasard\n")
    await bot.say(help)

@bot.command(pass_context=True, no_pm=True)
async def lsvimage(context):
    src, desc = await wh.getContentImageOfTheDay()

    emb = discord.Embed(title="Image du " + time.strftime("%#d %B %Y"), 
                        description=desc,
                        url="https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Image_du_jour/" + time.strftime("%#d_%B_%Y"), 
                        colour=0xFF005D)
    emb.set_image(url=src)
    emb.set_author(name="Le saviez vous ?", icon_url=bot.user.default_avatar_url)
    await bot.send_message(context.message.channel, embed=emb)

@bot.command(no_pm=True)
async def lsvlumiere():
    await bot.say(await wh.getContentLightOn())

@bot.command(no_pm=True)
async def lsvtrivia():
    await bot.say(await wh.getContentDidYouKnow())

@bot.command(no_pm=True)
async def lsvrand():
    await bot.say(await wh.getContentRandomPage())

async def cleanup():
    await wh.cleanup()


atexit.register(cleanup)

bot.run('token')