import discord
from discord.ext import commands
from discord import ui, Interaction, ButtonStyle
from logic import Pokemon, quiz_questions
from db_manager import DB_Manager
from config import token, DATABASE
import random
from collections import defaultdict

# ====== VERITABANI ======
db = DB_Manager(DATABASE)
db.create_tables()
db.default_insert()

# ====== DISCORD BOT ======
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== QUIZ ======
user_responses = defaultdict(lambda: {"index": 0, "points": 0})

async def send_question(ctx_or_interaction, user_id):
    idx = user_responses[user_id]["index"]
    question = quiz_questions[idx]
    buttons = question.gen_buttons()

    class QuizView(ui.View):
        def __init__(self):
            super().__init__(timeout=60)
            for b in buttons:
                self.add_item(b)

        async def interaction_check(self, interaction: Interaction) -> bool:
            if interaction.user.id != user_id:
                await interaction.response.send_message("Bu quiz senin için, başka cevap veremezsin.", ephemeral=True)
                return False
            return True

        async def on_timeout(self):
            user_responses.pop(user_id, None)
            self.stop()

    view = QuizView()

    for item in view.children:
        async def callback(interaction: Interaction, item=item):
            custom_id = interaction.data["custom_id"]
            if custom_id.startswith("correct"):
                user_responses[user_id]["points"] += 1
                await interaction.response.send_message("✅ Doğru cevap!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Yanlış cevap!", ephemeral=True)

            user_responses[user_id]["index"] += 1
            idx = user_responses[user_id]["index"]

            if idx >= len(quiz_questions):
                total = user_responses[user_id]["points"]
                await interaction.followup.send(f"🎉 Quiz bitti! Toplam puanın: {total}", ephemeral=True)
                user_responses.pop(user_id, None)
                view.stop()
            else:
                await send_question(interaction, user_id)

        item.callback = callback

    if isinstance(ctx_or_interaction, commands.Context):
        await ctx_or_interaction.send(question.text, view=view)
    else:
        await ctx_or_interaction.followup.send(question.text, view=view, ephemeral=True)

@bot.command()
async def startquiz(ctx):
    user_id = ctx.author.id
    user_responses[user_id] = {"index": 0, "points": 0}
    await send_question(ctx, user_id)

# ====== POKEMON KOMUTLARI ======
@bot.command()
async def start(ctx):
    user_id = ctx.author.id
    if user_id not in Pokemon.pokemons:
        poke = Pokemon.create_pokemon(user_id)
        Pokemon.pokemons[user_id] = poke
        await ctx.send(f"{ctx.author.mention}, bir Pokémon yakaladın! 🎉")
    else:
        await ctx.send(f"{ctx.author.mention}, zaten bir Pokémon'un var! 🎮")

@bot.command()
async def info(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        info_text = await poke.info()
        await ctx.send(info_text)
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
        result = await poke.feed()
        await ctx.send(f"{ctx.author.mention}, {result}")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def status(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        last_feed = poke.last_feed_time.strftime('%Y-%m-%d %H:%M:%S') if poke.last_feed_time else "Bilinmiyor"
        await ctx.send(f"📊 **Durum Raporu**\nHP: {poke.hp}\nPower: {poke.power}\nSon Beslenme: {last_feed}")
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
async def evolve(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        poke = Pokemon.pokemons[user_id]
        chance = random.randint(1, 4)
        if chance == 1:
            poke.power += 5
            await ctx.send(f"✨ {ctx.author.mention}, Pokémon evrim geçirdi! Yeni Power: {poke.power}")
        else:
            await ctx.send(f"{ctx.author.mention}, maalesef Pokémon evrim geçiremedi.")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def release(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        del Pokemon.pokemons[user_id]
        await ctx.send(f"{ctx.author.mention}, Pokémon'unu doğaya saldın. 🕊️ Elveda...")
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok.")

@bot.command()
async def img(ctx):
    await ctx.send("https://media.giphy.com/media/DRfu7BT8ZK1uo/giphy.gif")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı.")

bot.run(token)
