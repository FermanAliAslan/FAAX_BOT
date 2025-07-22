# README - Discord Pokémon Botu
#
# Bu bot, Discord üzerinde kullanıcıların kendi Pokémonlarını yakalayıp, besleyip,
# savaştırabileceği ve evrimleştirebileceği basit bir oyun sunar.
#
# --- Özellikler ---
# !start     : Kendine yeni bir Pokémon yakala.
# !info      : Pokémon'un temel bilgilerini göster.
# !attack    : Pokémon'una rastgele hasar ver.
# !feed      : Pokémon'unu besleyerek enerjisini yenile.
# !heal      : Pokémon'un canını tamamen doldur.
# !status    : Pokémon'un sağlık, güç ve son beslenme zamanını göster.
# !evolve    : Şansa bağlı olarak Pokémon evrim geçirebilir ve güçlenir.
# !release   : Pokémon'unu serbest bırak.
# !img       : Pokémon animasyonu gönderir.
#
# --- Kurulum ---
# 1. Python 3.8 veya üstü yüklü olmalı.
# 2. discord.py kütüphanesini yükle:
#    pip install discord.py
# 3. config.py dosyasına kendi Discord bot token'ını ekle:
#    token = "YOUR_DISCORD_BOT_TOKEN"
# 4. logic.py dosyasında Pokemon sınıfının tanımlı olduğundan emin ol.
# 5. Botu başlat:
#    python bot.py
#
# --- Kullanım ---
# Komutları Discord sunucunda prefix olarak ! ile kullanabilirsin.
# Örnek: !start, !attack, !feed, vs.
#
# --- Pokemon Sınıfı Basit Örneği ---
# import datetime
#
# class Pokemon:
#     pokemons = {}
#
#     def __init__(self, name, hp, power):
#         self.name = name
#         self.hp = hp
#         self.power = power
#         self.last_feed_time = datetime.datetime.now()
#
#     def feed(self):
#         self.hp = min(100, self.hp + 20)
#         self.last_feed_time = datetime.datetime.now()
#
#     def info(self):
#         return f"{self.name} - HP: {self.hp}, Power: {self.power}"
#
# --- Notlar ---
# - Her kullanıcı sadece bir Pokémon'a sahip olabilir.
# - Hasar ve evrim tamamen rastgele işliyor.
# - Pokémon canı 0'ın altına düşerse bot otomatik işlem yapmaz.
#
# --- Geliştirme Fikirleri ---
# - Farklı Pokémon türleri ve yetenekleri eklemek.
# - PvP modu ve yarışmalar geliştirmek.
# - Daha gelişmiş sağlık yönetimi.
#
# Keyifli oyunlar! ⚡🐾
