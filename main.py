import discord
from discord.ext import commands
import random
import os
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# ----------------- KOMUT AÇIKLAMALARI -----------------
komutlar = """
$bye: Gitmenize tepki olarak bir emoji gönderir.
$yardim: Komutları listeler.
$merhaba: Tanıtım mesajı gönderir.
$kirlilik: Çevre kirliliği hakkında bilgi verir.
$anket: İklim değişikliği anketini başlatır.
$hava <şehir>: Anlık sıcaklık bilgisini verir.
$co2 <yıl> <ay>: Dünya CO₂ seviyesini verir.
"""

# ----------------- ANKET SORULARI -----------------
sorular = [
"""
1. Günlük ulaşımını en çok nasıl sağlıyorsun?
A) Araba
B) Toplu taşıma
C) Yürüyüş / Bisiklet
D) Diğer / Karışık
""",
"""
2. Evinde enerji tasarrufu yapmak için genelde ne yaparsın?
A) Pek bir şey yapmıyorum
B) Işıkları ve cihazları kapatıyorum
C) Enerji tasarruflu cihazlar kullanıyorum
D) Güneş enerjisi veya yenilenebilir kaynak kullanıyorum
""",
"""
3. Geri dönüşüm konusunda ne kadar aktifsin?
A) Hiç
B) Bazen
C) Düzenli olarak
D) Tüm atıkları ayrıştırıyorum ve topluluk geri dönüşümüne katılıyorum
""",
"""
4. Alışveriş yaparken çevre dostu ürünlere yöneliyor musun?
A) Pek sayılmaz
B) Bazen dikkat ediyorum
C) Özellikle çevreci ürünleri tercih ediyorum
D) Sadece çevreci ürünleri alıyorum
""",
"""
5. Tek kullanımlık plastik ürünler (bardak, poşet, şişe) kullanma sıklığın nasıl?
A) Çok sık
B) Ara sıra
C) Mümkün olduğunca kaçınıyorum
D) Hiç kullanmıyorum
""",
"""
6. Elektrik tüketimini azaltmak için hangi yöntemleri kullanıyorsun?
A) Hiçbir şey yapmıyorum
B) Gereksiz cihazları kapatıyorum
C) Enerji tasarruflu ampul ve cihaz kullanıyorum
D) Güneş enerjisi ve akıllı cihazlar kullanıyorum
""",
"""
7. Su tasarrufu yapmak için ne yapıyorsun?
A) Hiçbir şey yapmıyorum
B) Suyu dikkatli kullanıyorum
C) Duş süresini kısaltıyor ve sızıntıları önlüyorum
D) Yağmur suyu toplama veya akıllı su sistemleri kullanıyorum
""",
"""
8. Geri dönüşüm ve atık ayrıştırma konusunda evinde hangi yöntemleri uyguluyorsun?
A) Hiç uygulamıyorum
B) Bazı geri dönüşümleri yapıyorum
C) Düzenli olarak tüm geri dönüşümleri yapıyorum
D) Topluluk geri dönüşüm programlarına aktif katılıyorum
"""
]

# ----------------- KULLANICI CEVAPLARI -----------------
kullanici_cevaplari = {}

# ----------------- ÖNERİLER -----------------
oneriler = {
    "1": {"A": "Daha fazla toplu taşıma veya bisiklet kullanabilirsin.",
          "B": "Harika! Toplu taşımayı tercih ediyorsun.",
          "C": "Mükemmel! Çevreye dost ulaşım yöntemleri kullanıyorsun.",
          "D": "İyi! Farklı ulaşım yöntemlerini dengeliyorsun."},

    "2": {"A": "Enerji tasarrufu yapmayı düşünebilirsin.",
          "B": "İyi! Basit önlemlerle tasarruf ediyorsun.",
          "C": "Harika! Enerji tasarruflu cihaz kullanıyorsun.",
          "D": "Mükemmel! Yenilenebilir kaynaklar kullanıyorsun."},

    "3": {"A": "Geri dönüşüm konusunda daha aktif olabilirsin.",
          "B": "Bazen geri dönüşüm yapman güzel.",
          "C": "Harika! Düzenli geri dönüşüm yapıyorsun.",
          "D": "Mükemmel! Tüm atıkları ayrıştırıyorsun."},

    "4": {"A": "Alışverişlerde çevreci ürünlere yönelmeyi deneyebilirsin.",
          "B": "Bazen dikkat etmen güzel.",
          "C": "Çevre dostu ürünleri özellikle seçmen harika!",
          "D": "Mükemmel! Sadece çevreci ürünleri tercih ediyorsun."},

    "5": {"A": "Tek kullanımlık ürünleri azaltmayı deneyebilirsin.",
          "B": "Ara sıra kullanman fena değil ama azaltmak iyi olur.",
          "C": "Harika! Tek kullanımlıkları mümkün olduğunca azaltıyorsun.",
          "D": "Mükemmel! Hiç kullanmıyorsun."},

    "6": {"A": "Elektrik tasarrufu yapmayı düşünebilirsin.",
          "B": "İyi! Gereksiz cihazları kapatıyorsun.",
          "C": "Harika! Enerji tasarruflu ampul ve cihaz kullanıyorsun.",
          "D": "Mükemmel! Güneş enerjisi ve akıllı cihazlar kullanıyorsun."},

    "7": {"A": "Su tasarrufu yapmayı düşünebilirsin.",
          "B": "İyi! Dikkatli su kullanıyorsun.",
          "C": "Mükemmel! Su kullanımını etkin şekilde yönetiyorsun.",
          "D": "Harika! Akıllı sistemlerle suyu verimli kullanıyorsun."},

    "8": {"A": "Geri dönüşüme başlamanı öneririm.",
          "B": "Bazı adımlar atman güzel.",
          "C": "Harika! Düzenli olarak geri dönüşüm yapıyorsun.",
          "D": "Mükemmel! Topluluk geri dönüşüm programlarına katılıyorsun."}
}

# ----------------- EVENTLER -----------------
@bot.event
async def on_ready():
    print(f'Bot giriş yaptı: {bot.user}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot:
        return

    user_id = message.author.id
    cevaplar = message.content.split(",")
    kaydedilen = False

    for item in cevaplar:
        item = item.strip()
        if len(item.split(".")) != 2:
            continue
        try:
            soru_no, cevap = item.split(".")
            soru_no = soru_no.strip()
            cevap = cevap.strip().upper()
            if soru_no not in [str(i) for i in range(1, 9)]:
                continue
            if cevap not in ["A","B","C","D"]:
                continue
            if user_id not in kullanici_cevaplari:
                kullanici_cevaplari[user_id] = {}
            kullanici_cevaplari[user_id][soru_no] = cevap
            kaydedilen = True
        except:
            continue

    if kaydedilen:
        await message.channel.send("Cevapların kaydedildi!")
        if len(kullanici_cevaplari[user_id]) == 8:
            await message.channel.send("Tüm soruları tamamladın! İşte önerilerin:")
            for sn, cvp in kullanici_cevaplari[user_id].items():
                await message.channel.send(f"Soru {sn}: {oneriler[sn][cvp]}")

# ----------------- NORMAL KOMUTLAR -----------------
@bot.command()
async def bye(ctx):
    await ctx.send("Hoşçakal! 🙂")

@bot.command()
async def yardim(ctx):
    await ctx.send(komutlar)

@bot.command()
async def merhaba(ctx):
    await ctx.send(f"Selam! Ben {bot.user}, çevre dostu Discord botuyum!")

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
    await ctx.send("Anket başlıyor! Cevap vermek için: **1.A, 2.B, 3.C … 8.D** gibi yaz.\n")
    for soru in sorular:
        await ctx.send(soru)

# ----------------- API KOMUTLARI -----------------
@bot.command()
async def hava(ctx, *, sehir):
    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={sehir}&count=1").json()
    if "results" not in geo:
        return await ctx.send("Şehir bulunamadı!")
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m").json()
    temp = weather["current"]["temperature_2m"]
    await ctx.send(f"**{sehir.title()}** şu anda: **{temp}°C**")

@bot.command()
async def co2(ctx, yil: int = None, ay: int = None):
    url = "https://v1.datafor.earth/api/co2/monthly"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        await ctx.send("CO₂ verisi alınırken bir hata oluştu.")
        print("CO2 API hata:", e)
        return

    son_veri = data[-1]
    son_yil = son_veri.get("year")
    son_ay = son_veri.get("month")
    son_ppm = float(son_veri.get("measurement", 0))

    if yil is None or ay is None:
        yil = son_yil
        ay = son_ay
        ppm = son_ppm
    else:
        secilen = next((item for item in data if item["year"] == yil and item["month"] == ay), None)
        if secilen is None:
            await ctx.send(
                f"{yil}-{ay:02d} için CO₂ verisi henüz mevcut değil.\n"
                f"En son veri: {son_yil}-{son_ay:02d} — {son_ppm:.2f} ppm"
            )
            return
        ppm = float(secilen.get("measurement", 0))

    await ctx.send(f"Dünya CO₂ seviyesi (Earth API): **{ppm:.2f} ppm** — {yil}-{ay:02d}")

# ----------------- BOT ÇALIŞTIR -----------------
bot.run("BOT_TOKEN")
