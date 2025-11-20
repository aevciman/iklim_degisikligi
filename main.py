import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

komutlar = """
$bye: Bot gitmenize tepki olarak bir emoji gönderir.
$yardim: Bot komutları listeler.
$merhaba: Bot tanıtım mesajı gönderir.
$kirlilik: Bot çevre kirliliği hakkında şaşırtıcı bilgiler verir.
"""

@bot.event
async def on_ready():
    print(f'Bot giriş yaptı: {bot.user}')

@bot.command()
async def bye(ctx):
    await ctx.send("Hoşçakal!\U0001f642")  # 🙂

@bot.command()
async def yardim(ctx):
    await ctx.send(komutlar)

@bot.command()
async def merhaba(ctx):
    await ctx.send(f'Selam! Ben {bot.user}, bir Discord sohbet botuyum!')

@bot.command("kirlilik")
async def kirlilik(ctx):
    klasor = "kirlilik_bilgileri"
    secilen = random.choice(os.listdir(klasor))
    tam_yol = os.path.join(klasor, secilen)

    with open(tam_yol, "r", encoding="utf-8") as dosya:
        icerik = dosya.read()
        await ctx.send(icerik)


bot.run("BOT_TOKEN")
