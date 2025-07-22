import discord
from discord.ext import commands
from config import token
from logic import Pokemon
import random
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı.")

@bot.command()
async def start(ctx):
    user_id = ctx.author.id
    if user_id not in Pokemon.pokemons:
        poke = Pokemon("Pikachu", 100, 10)
        Pokemon.pokemons[user_id] = poke
        await ctx.send(f"{ctx.author.mention}, bir Pokémon yakaladın! 🎉")
    else:
        await ctx.send(f"{ctx.author.mention}, zaten bir Pokémon'un var! 🎮")

@bot.command()
async def info(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        await ctx.send(poke.info())
    else:
        await ctx.send("Henüz bir Pokémon yakalamadınız. !start ile başlayın.")

@bot.command()
async def attack(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        damage = random.randint(5, 15)
        poke.hp -= damage
        await ctx.send(f"{ctx.author.mention}, saldırı yapıldı! {damage} hasar aldın. HP: {poke.hp}")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def feed(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        poke.feed()
        await ctx.send(f"{ctx.author.mention}, Pokémon'un beslendi. Enerjisi yerine geldi! 🍎")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def img(ctx):
    await ctx.send("https://media.giphy.com/media/DRfu7BT8ZK1uo/giphy.gif")

@bot.command()
async def release(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        del Pokemon.pokemons[user_id]
        await ctx.send(f"{ctx.author.mention}, Pokémon'unu doğaya saldın. 🕊️ Elveda...")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def heal(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        poke.hp = 100
        await ctx.send(f"🧬 {ctx.author.mention}, Pokémon'unuz tam şarj oldu! HP: 100")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def status(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        last_feed = poke.last_feed_time.strftime('%Y-%m-%d %H:%M:%S')
        await ctx.send(
            f"📊 **Durum Raporu**\nHP: {poke.hp}\nPower: {poke.power}\nSon Beslenme: {last_feed}"
        )
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def evolve(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        chance = random.randint(1, 4)
        if chance == 1:
            poke.power += 5
            await ctx.send(f"✨ {ctx.author.mention}, Pokémon evrim geçirdi! Yeni Power: {poke.power}")
        else:
            await ctx.send("🧬 Evrim başarısız oldu. Daha fazla çalışman gerek...")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

bot.run(token)

