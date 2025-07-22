import aiohttp
import random
import datetime

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        # pokemon_trainer artık discord kullanıcısının ID'si (int)
        self.pokemon_trainer = pokemon_trainer  
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(50, 100)    # biraz daha sağlam başlasın diye
        self.power = random.randint(5, 15)   # biraz daha dengeli güç
        self.last_feed_time = datetime.datetime.min

        # Eğer kullanıcı zaten varsa, mevcut nesneyi döndürme zor, onu dışarda main.py'de kontrol ediyoruz
        # Burada sadece yeni yaratma işlemi yapılır.

    @classmethod
    def get_pokemon(cls, trainer_id):
        # Eğer varsa pokemon döner, yoksa None
        return cls.pokemons.get(trainer_id)

    @classmethod
    def create_pokemon(cls, trainer_id, pkmn_type="normal"):
        # Farklı tipte pokemon yaratma
        if trainer_id in cls.pokemons:
            return cls.pokemons[trainer_id]

        if pkmn_type.lower() == "wizard":
            poke = Wizard(trainer_id)
        elif pkmn_type.lower() == "fighter":
            poke = Fighter(trainer_id)
        else:
            poke = Pokemon(trainer_id)

        cls.pokemons[trainer_id] = poke
        return poke

    async def get_name(self):
        if self.name:
            return self.name

        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name']
                else:
                    self.name = "Pikachu"
        return self.name

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(hours=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            if self.hp > 100:
                self.hp = 100
            self.last_feed_time = current_time
            return f"Pokémon sağlığı geri yüklendi. Mevcut HP: {self.hp}"
        else:
            next_time = self.last_feed_time + delta_time
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {next_time.strftime('%Y-%m-%d %H:%M:%S')}"

    async def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            if enemy.hp < 0:
                enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'e saldırdı!\nKalan can: {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'i yendi!"

    async def info(self):
        if not self.name:
            await self.get_name()
        return f"🔍 Pokémonunuzun ismi: {self.name} \n❤️ HP: {self.hp} \n⚔️ Power: {self.power}"

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url
                else:
                    return None

class Wizard(Pokemon):
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            sans = random.randint(1, 5)
            if sans == 1:
                return "✨ Sihirbaz Pokémon savaşta bir kalkan kullandı, saldırı etkisiz!"
        return await super().attack(enemy)

    async def feed(self, feed_interval=20, hp_increase=10):
        hp_increase = int(hp_increase * 1.5)
        return await super().feed(feed_interval, hp_increase)

class Fighter(Pokemon):
    async def attack(self, enemy):
        extra_power = random.randint(5, 15)
        self.power += extra_power
        result = await super().attack(enemy)
        self.power -= extra_power
        return result + f"\n💥 Dövüşçü Pokémon süper saldırı kullandı! +{extra_power} güç"

    async def feed(self, feed_interval=20, hp_increase=10):
        hp_increase = int(hp_increase / 1.5)
        return await super().feed(feed_interval, hp_increase)


