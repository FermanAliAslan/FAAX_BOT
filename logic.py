import aiohttp
import random
import datetime

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(1, 100)
        self.power = random.randint(1, 10)
        self.last_feed_time = datetime.datetime.min

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(hours=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon sağlığı geri yüklendi. Mevcut HP: {self.hp}"
        else:
            next_time = self.last_feed_time + delta_time
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {next_time.strftime('%Y-%m-%d %H:%M:%S')}"

    async def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'e saldırdı!\n@{enemy.pokemon_trainer}'nin kalan canı: {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'i yendi!"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
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

