import discord
from discord.ext import commands
from discord import ui, ButtonStyle
from config import token

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Pokemon sınıfı ---
import random
import datetime

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(1, 100)
        self.level = 1
        self.last_fed = None
        self.status = "Healthy"

    def feed(self):
        self.last_fed = datetime.datetime.now()
        self.hp += 10
        self.status = "Happy"

    def evolve(self):
        self.level += 1
        self.hp += 20
        self.status = "Evolved"

    def heal(self):
        self.hp = 100
        self.status = "Healed"

    def release(self):
        Pokemon.pokemons.pop(self.pokemon_trainer, None)

    def get_info(self):
        return f"🎮 Trainer: {self.pokemon_trainer}\n🆔 No: {self.pokemon_number}\n💖 HP: {self.hp}\n⭐ Level: {self.level}\n📅 Last Fed: {self.last_fed}\n📊 Status: {self.status}"

# --- Quiz Sınıfı ---
class Question:
    def __init__(self, text, answer_id, *options):
        self.__text = text
        self.__answer_id = answer_id
        self.options = options

    @property
    def text(self):
        return self.__text

    def gen_buttons(self):
        buttons = []
        for i, option in enumerate(self.options):
            if i == self.__answer_id:
                buttons.append(ui.Button(label=option, style=ButtonStyle.success, custom_id=f'correct_{i}'))
            else:
                buttons.append(ui.Button(label=option, style=ButtonStyle.danger, custom_id=f'wrong_{i}'))
        return buttons

quiz_questions = [
    Question("Kediler neden miyavlar?", 0, "İletişim için", "Saldırmak için", "Kaçmak için", "Oynamak için"),
    Question("Dünya'nın uydusu hangisidir?", 2, "Venüs", "Güneş", "Ay", "Mars"),
]

class QuizView(ui.View):
    def __init__(self, question: Question):
        super().__init__()
        self.question = question
        for button in question.gen_buttons():
            self.add_item(button)

    @ui.button(label="Soru Göster", style=ButtonStyle.primary, custom_id="show_question")
    async def show_question(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.question.text, view=self, ephemeral=True)


# --- Olaylar ve Komutlar ---
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanıcı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

# --- Quiz Komutu ---
@bot.command()
async def quiz(ctx):
    question = random.choice(quiz_questions)
    view = QuizView(question)
    await ctx.send(question.text, view=view)

bot.run(token)


