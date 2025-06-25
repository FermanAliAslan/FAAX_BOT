import discord
from discord.ext import commands
from config import token

# Basit Car sınıfı
class Car:
    def __init__(self, color, brand):
        self.color = color
        self.brand = brand

    def info(self):
        return f"🚗 Marka: {self.brand}, Renk: {self.color}"

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print(f"Giriş yaptı: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(client.command_prefix):
        await client.process_commands(message)
    else:
        await message.channel.send(message.content)

@client.command()
async def about(ctx):
    await ctx.send('Bu discord.py kütüphanesi ile oluşturulmuş echo-bot!')

@client.command()
async def info(ctx):
    await ctx.send(
        "Komutlar:\n"
        "- /about: Bot hakkında bilgi\n"
        "- /info: Komutları gösterir\n"
        "- /ping: Gecikme\n"
        "- /car renk marka: Araç bilgisi gösterir"
    )

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)} ms")

@client.command()
async def car(ctx, color: str, brand: str):
    new_car = Car(color, brand)
    await ctx.send(new_car.info())

client.run(token)
