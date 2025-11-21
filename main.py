import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Komut açıklamaları
komutlar = """
$bye: Bot gitmenize tepki olarak bir emoji gönderir.
$yardim: Bot komutları listeler.
$merhaba: Bot tanıtım mesajı gönderir.
$kirlilik: Bot çevre kirliliği hakkında şaşırtıcı bilgiler verir.
$anket: İklim değişikliği anketini başlatır.
"""

# Anket soruları
sorular = [
"""
1. Günlük ulaşımını en çok nasıl sağlıyorsun?
A) Araba
B) Toplu taşıma
C) Yürüyüş / Bisiklet
""",
"""
2. Evinde enerji tasarrufu yapmak için genelde ne yaparsın?
A) Pek bir şey yapmıyorum
B) Işıkları ve cihazları kapatıyorum
C) Enerji tasarruflu cihazlar kullanıyorum
""",
"""
3. Geri dönüşüm konusunda ne kadar aktifsin?
A) Hiç
B) Bazen
C) Düzenli olarak
""",
"""
4. Alışveriş yaparken çevre dostu ürünlere yöneliyor musun?
A) Pek sayılmaz
B) Bazen dikkat ediyorum
C) Özellikle çevreci ürünleri tercih ediyorum
""",
"""
5. Tek kullanımlık plastik ürünler (bardak, poşet, şişe) kullanma sıklığın nasıl?
A) Çok sık
B) Ara sıra
C) Mümkün olduğunca kaçınıyorum
"""
]

# Kullanıcı cevaplarını saklamak için sözlük
kullanici_cevaplari = {}

# Kullanıcı cevaplarına göre öneriler
oneriler = {
    "1": {
        "A": "Daha fazla toplu taşıma veya bisiklet kullanmayı deneyebilirsin.",
        "B": "Harika! Toplu taşımayı tercih ediyorsun.",
        "C": "Mükemmel! Çevreye dost ulaşım yöntemleri kullanıyorsun."
    },
    "2": {
        "A": "Enerji tasarrufu yapmayı düşünebilirsin.",
        "B": "Güzel, basit önlemlerle enerji tasarrufu yapıyorsun.",
        "C": "Harika! Enerji tasarruflu cihaz kullanmak çok etkili."
    },
    "3": {
        "A": "Geri dönüşüm konusunda daha aktif olabilirsin.",
        "B": "Bazen geri dönüşüm yapman iyi bir başlangıç.",
        "C": "Harika! Düzenli geri dönüşüm çevreyi korur."
    },
    "4": {
        "A": "Alışverişlerde çevreci ürünlere yönelmeyi deneyebilirsin.",
        "B": "Bazen dikkat etmen güzel.",
        "C": "Mükemmel! Çevre dostu ürünleri tercih ediyorsun."
    },
    "5": {
        "A": "Tek kullanımlık ürünleri azaltmayı deneyebilirsin.",
        "B": "Ara sıra kullanım fena değil, ama azaltmak iyi olur.",
        "C": "Harika! Tek kullanımlıklardan mümkün olduğunca kaçınıyorsun."
    }
}

# ----------------- BOT EVENTLERİ -----------------

@bot.event
async def on_ready():
    print(f'Bot giriş yaptı: {bot.user}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return

    user_id = message.author.id

    # Mesajı virgülle ayır
    cevaplar = message.content.split(",")
    kaydedilen = False

    for item in cevaplar:
        item = item.strip()  # baştaki/sondaki boşlukları temizle
        if len(item.split(".")) != 2:
            continue

        try:
            soru_no, cevap = item.split(".")
            soru_no = soru_no.strip()
            cevap = cevap.strip().upper()

            if soru_no not in ["1","2","3","4","5"]:
                continue
            if cevap not in ["A","B","C"]:
                continue

            if user_id not in kullanici_cevaplari:
                kullanici_cevaplari[user_id] = {}

            kullanici_cevaplari[user_id][soru_no] = cevap
            kaydedilen = True

        except:
            continue

    if kaydedilen:
        await message.channel.send("Cevapların kaydedildi ✅")
        if len(kullanici_cevaplari[user_id]) == 5:
            await message.channel.send("Tüm soruları tamamladın! 🎉\nİşte önerilerin:")
            for sn, cvp in kullanici_cevaplari[user_id].items():
                await message.channel.send(f"Soru {sn}: {oneriler[sn][cvp]}")

# ----------------- BOT KOMUTLARI -----------------

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

@bot.command("anket")
async def anket(ctx):
    await ctx.send("Anket başlıyor! Cevap vermek için: **1.A, 2.B, 3.C** gibi yaz.\n")
    for soru in sorular:
        await ctx.send(soru)

# ----------------- BOT ÇALIŞTIR -----------------

bot.run("BOT_TOKEN")  # Tokeni kendi bot tokeninle değiştir
