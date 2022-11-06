from dataclasses import dataclass


@dataclass
class Badge:
    name: str
    cap: int
    image: str


class BadgeDataMeta(type):
    def __getattr__(self, item):
        if item in self.badge_data:
            return self.badge_data[item]
        raise ValueError(f'no badge data for {item}')

    def __getitem__(self, item):
        if item in self.badge_data:
            return self.badge_data[item]
        raise ValueError(f'no badge data for {item}')


class BadgeData(metaclass=BadgeDataMeta):
    badge_data = {
        'rb': [
            Badge(name='Boulder Badge', cap=14, image='https://www.pokewiki.de/images/8/8b/Felsorden.png'),
            Badge(name='Cascade Badge', cap=21, image='https://www.pokewiki.de/images/5/55/Quellorden.png'),
            Badge(name='Thunder Badge', cap=24, image='https://www.pokewiki.de/images/5/53/Donnerorden.png'),
            Badge(name='Rainbow Badge', cap=29, image='https://www.pokewiki.de/images/8/8b/Farborden.png'),
            Badge(name='Soul Badge', cap=43, image='https://www.pokewiki.de/images/f/fa/Seelenorden.png'),
            Badge(name='Marsh Badge', cap=43, image='https://www.pokewiki.de/images/5/5c/Sumpforden.png'),
            Badge(name='Volcano Badge', cap=47, image='https://www.pokewiki.de/images/c/c0/Vulkanorden.png'),
            Badge(name='Earth Badge', cap=50, image='https://www.pokewiki.de/images/7/70/Erdorden.png'),
            Badge(name='Champion Ribbon', cap=62, image='https://www.pokewiki.de/images/7/7e/Band_des_Champs.png'),
        ],
        'y': [
            Badge(name='Boulder Badge', cap=12, image='https://www.pokewiki.de/images/8/8b/Felsorden.png'),
            Badge(name='Cascade Badge', cap=21, image='https://www.pokewiki.de/images/5/55/Quellorden.png'),
            Badge(name='Thunder Badge', cap=28, image='https://www.pokewiki.de/images/5/53/Donnerorden.png'),
            Badge(name='Rainbow Badge', cap=32, image='https://www.pokewiki.de/images/8/8b/Farborden.png'),
            Badge(name='Soul Badge', cap=50, image='https://www.pokewiki.de/images/f/fa/Seelenorden.png'),
            Badge(name='Marsh Badge', cap=50, image='https://www.pokewiki.de/images/5/5c/Sumpforden.png'),
            Badge(name='Volcano Badge', cap=54, image='https://www.pokewiki.de/images/c/c0/Vulkanorden.png'),
            Badge(name='Earth Badge', cap=55, image='https://www.pokewiki.de/images/7/70/Erdorden.png'),
            Badge(name='Champion Ribbon', cap=62, image='https://www.pokewiki.de/images/7/7e/Band_des_Champs.png'),
        ],
        'frlg': [
            Badge(name='Boulder Badge', cap=14, image='https://www.pokewiki.de/images/8/8b/Felsorden.png'),
            Badge(name='Cascade Badge', cap=21, image='https://www.pokewiki.de/images/5/55/Quellorden.png'),
            Badge(name='Thunder Badge', cap=24, image='https://www.pokewiki.de/images/5/53/Donnerorden.png'),
            Badge(name='Rainbow Badge', cap=29, image='https://www.pokewiki.de/images/8/8b/Farborden.png'),
            Badge(name='Soul Badge', cap=43, image='https://www.pokewiki.de/images/f/fa/Seelenorden.png'),
            Badge(name='Marsh Badge', cap=43, image='https://www.pokewiki.de/images/5/5c/Sumpforden.png'),
            Badge(name='Volcano Badge', cap=47, image='https://www.pokewiki.de/images/c/c0/Vulkanorden.png'),
            Badge(name='Earth Badge', cap=50, image='https://www.pokewiki.de/images/7/70/Erdorden.png'),
            Badge(name='Champion Ribbon', cap=60, image='https://www.pokewiki.de/images/7/7e/Band_des_Champs.png'),
        ],
        'frlg2': [
            Badge(name='Boulder Badge', cap=14, image='https://www.pokewiki.de/images/8/8b/Felsorden.png'),
            Badge(name='Cascade Badge', cap=21, image='https://www.pokewiki.de/images/5/55/Quellorden.png'),
            Badge(name='Thunder Badge', cap=24, image='https://www.pokewiki.de/images/5/53/Donnerorden.png'),
            Badge(name='Rainbow Badge', cap=29, image='https://www.pokewiki.de/images/8/8b/Farborden.png'),
            Badge(name='Soul Badge', cap=43, image='https://www.pokewiki.de/images/f/fa/Seelenorden.png'),
            Badge(name='Marsh Badge', cap=43, image='https://www.pokewiki.de/images/5/5c/Sumpforden.png'),
            Badge(name='Volcano Badge', cap=47, image='https://www.pokewiki.de/images/c/c0/Vulkanorden.png'),
            Badge(name='Earth Badge', cap=50, image='https://www.pokewiki.de/images/7/70/Erdorden.png'),
            Badge(name='Champion Ribbon', cap=60, image='https://www.pokewiki.de/images/7/7e/Band_des_Champs.png'),
            Badge(name='Champion Ribbon', cap=72, image='https://www.pokewiki.de/images/7/7e/Band_des_Champs.png'),
        ],
        'Johto': [
            Badge(name='Zephyr Badge', cap=0, image='https://www.pokewiki.de/images/2/2e/Fl%C3%BCgelorden.png'),
            Badge(name='Hive Badge', cap=0, image='https://www.pokewiki.de/images/5/5c/Insektorden.png'),
            Badge(name='Plain Badge', cap=0, image='https://www.pokewiki.de/images/e/e5/Basisorden.png'),
            Badge(name='Fog Badge', cap=0, image='https://www.pokewiki.de/images/1/17/Phantomorden.png'),
            Badge(name='Storm Badge', cap=0, image='https://www.pokewiki.de/images/2/23/Faustorden.png'),
            Badge(name='Mineral Badge', cap=0, image='https://www.pokewiki.de/images/c/c7/Stahlorden.png'),
            Badge(name='Glacier Badge', cap=0, image='https://www.pokewiki.de/images/3/39/Eisorden.png'),
            Badge(name='Rising Badge', cap=0, image='https://www.pokewiki.de/images/4/4e/Drachenorden.png')
        ],
        'rs': [
            Badge(name='Stone Badge', cap=15, image='https://www.pokewiki.de/images/2/2b/Steinorden.png'),
            Badge(name='Knuckle Badge', cap=18, image='https://www.pokewiki.de/images/d/dc/Kn%C3%B6chelorden.png'),
            Badge(name='Dynamo Badge', cap=23, image='https://www.pokewiki.de/images/f/f5/Dynamo-Orden.png'),
            Badge(name='Heat Badge', cap=28, image='https://www.pokewiki.de/images/5/50/Hitzeorden.png'),
            Badge(name='Balance Badge', cap=31, image='https://www.pokewiki.de/images/b/bf/Balanceorden.png'),
            Badge(name='Feather Badge', cap=33, image='https://www.pokewiki.de/images/c/c7/Federorden.png'),
            Badge(name='Mind Badge', cap=42, image='https://www.pokewiki.de/images/c/cb/Mentalorden.png'),
            Badge(name='Rain Badge', cap=43, image='https://www.pokewiki.de/images/4/45/Schauerorden.png'),
            Badge(name='Champion Ribbon', cap=55,
                  image='https://www.pokewiki.de/images/f/f3/Band_des_Hoenn-Champs.png'),
        ],
        'e': [
            Badge(name='Stone Badge', cap=15, image='https://www.pokewiki.de/images/2/2b/Steinorden.png'),
            Badge(name='Knuckle Badge', cap=19, image='https://www.pokewiki.de/images/d/dc/Kn%C3%B6chelorden.png'),
            Badge(name='Dynamo Badge', cap=24, image='https://www.pokewiki.de/images/f/f5/Dynamo-Orden.png'),
            Badge(name='Heat Badge', cap=29, image='https://www.pokewiki.de/images/5/50/Hitzeorden.png'),
            Badge(name='Balance Badge', cap=31, image='https://www.pokewiki.de/images/b/bf/Balanceorden.png'),
            Badge(name='Feather Badge', cap=33, image='https://www.pokewiki.de/images/c/c7/Federorden.png'),
            Badge(name='Mind Badge', cap=42, image='https://www.pokewiki.de/images/c/cb/Mentalorden.png'),
            Badge(name='Rain Badge', cap=46, image='https://www.pokewiki.de/images/4/45/Schauerorden.png'),
            Badge(name='Champion Ribbon', cap=55,
                  image='https://www.pokewiki.de/images/f/f3/Band_des_Hoenn-Champs.png'),
        ],
        'oras': [
            Badge(name='Stone Badge', cap=14, image='https://www.pokewiki.de/images/2/2b/Steinorden.png'),
            Badge(name='Knuckle Badge', cap=16, image='https://www.pokewiki.de/images/d/dc/Kn%C3%B6chelorden.png'),
            Badge(name='Dynamo Badge', cap=21, image='https://www.pokewiki.de/images/f/f5/Dynamo-Orden.png'),
            Badge(name='Heat Badge', cap=28, image='https://www.pokewiki.de/images/5/50/Hitzeorden.png'),
            Badge(name='Balance Badge', cap=30, image='https://www.pokewiki.de/images/b/bf/Balanceorden.png'),
            Badge(name='Feather Badge', cap=35, image='https://www.pokewiki.de/images/c/c7/Federorden.png'),
            Badge(name='Mind Badge', cap=45, image='https://www.pokewiki.de/images/c/cb/Mentalorden.png'),
            Badge(name='Rain Badge', cap=46, image='https://www.pokewiki.de/images/4/45/Schauerorden.png'),
            Badge(name='Champion Ribbon', cap=55,
                  image='https://www.pokewiki.de/images/f/f3/Band_des_Hoenn-Champs.png'),
        ],
        'Sinnoh': [
            Badge(name='Coal Badge', cap=0, image='https://www.pokewiki.de/images/e/ef/Kohleorden.png'),
            Badge(name='Forest Badge', cap=0, image='https://www.pokewiki.de/images/a/ab/Waldorden.png'),
            Badge(name='Cobble Badge', cap=0, image='https://www.pokewiki.de/images/3/3a/Bergorden.png'),
            Badge(name='Fen Badge', cap=0, image='https://www.pokewiki.de/images/4/41/Fennorden.png'),
            Badge(name='Relic Badge', cap=0, image='https://www.pokewiki.de/images/a/ac/Reliktorden.png'),
            Badge(name='Mine Badge', cap=0, image='https://www.pokewiki.de/images/8/82/Minenorden.png'),
            Badge(name='Icicle Badge', cap=0, image='https://www.pokewiki.de/images/7/71/Firnorden.png'),
            Badge(name='Beacon Badge', cap=0, image='https://www.pokewiki.de/images/f/f9/Lichtorden.png'),
            Badge(name='Champion Ribbon', cap=0,
                  image='https://www.pokewiki.de/images/1/1e/Band_des_Sinnoh-Champs.png'),
        ],
        'Einall': [
            Badge(name='Trio Badge', cap=0, image='https://www.pokewiki.de/images/3/35/Triorden.png'),
            Badge(name='Basic Badge', cap=0, image='https://www.pokewiki.de/images/c/ce/Grundorden.png'),
            Badge(name='Toxic Badge', cap=0, image='https://www.pokewiki.de/images/f/f3/Giftorden.png'),
            Badge(name='Insect Badge', cap=0, image='https://www.pokewiki.de/images/9/9a/K%C3%A4ferorden.png'),
            Badge(name='Bolt Badge', cap=0, image='https://www.pokewiki.de/images/d/de/Voltorden.png'),
            Badge(name='Quake Badge', cap=0, image='https://www.pokewiki.de/images/0/08/Seismo-Orden.png'),
            Badge(name='Jet Badge', cap=0, image='https://www.pokewiki.de/images/4/44/Jetorden.png'),
            Badge(name='Freeze Badge', cap=0, image='https://www.pokewiki.de/images/0/0d/Eiszapforden.png'),
            Badge(name='Legend Badge', cap=0, image='https://www.pokewiki.de/images/a/a2/Legendenorden.png'),
            Badge(name='Wave Badge', cap=0, image='https://www.pokewiki.de/images/9/9b/Wellenorden.png'),
            Badge(name='Champion Ribbon', cap=0, image='https://www.pokewiki.de/images/7/7e/Band_des_Champs.png'),
        ],
        'Kalos': [
            Badge(name='Bug Badge', cap=0, image='https://www.pokewiki.de/images/5/55/Krabbelorden.png'),
            Badge(name='Cliff Badge', cap=0, image='https://www.pokewiki.de/images/9/95/Wallorden.png'),
            Badge(name='Rumble Badge', cap=0, image='https://www.pokewiki.de/images/2/2f/Rauforden.png'),
            Badge(name='Plant Badge', cap=0, image='https://www.pokewiki.de/images/6/6a/Blattorden.png'),
            Badge(name='Voltage Badge', cap=0, image='https://www.pokewiki.de/images/8/80/Ampere-Orden.png'),
            Badge(name='Fairy Badge', cap=0, image='https://www.pokewiki.de/images/5/58/Feenorden.png'),
            Badge(name='Psychic Badge', cap=0, image='https://www.pokewiki.de/images/7/75/Psi-Orden.png'),
            Badge(name='Iceberg Badge', cap=0, image='https://www.pokewiki.de/images/6/66/Eisbergorden.png'),
            Badge(name='Champion Ribbon', cap=0, image='https://www.pokewiki.de/images/f/fe/Band_des_Kalos-Champs.png'),
        ],
        'Galar': [
            Badge(name='Grass Badge', cap=0, image='https://www.pokewiki.de/images/d/d1/Pflanzen-Orden.png'),
            Badge(name='Water Badge', cap=0, image='https://www.pokewiki.de/images/d/d6/Wasser-Orden.png'),
            Badge(name='Fire Badge', cap=0, image='https://www.pokewiki.de/images/1/1f/Feuer-Orden.png'),
            Badge(name='Fighting Badge', cap=0, image='https://www.pokewiki.de/images/5/5e/Kampf-Orden.png'),
            Badge(name='Ghost Badge', cap=0, image='https://www.pokewiki.de/images/6/60/Geister-Orden.png'),
            Badge(name='Fairy Badge', cap=0, image='https://www.pokewiki.de/images/1/1a/Feen-Orden.png'),
            Badge(name='Rock Badge', cap=0, image='https://www.pokewiki.de/images/5/5a/Gesteins-Orden.png'),
            Badge(name='Ice Badge', cap=0, image='https://www.pokewiki.de/images/a/a5/Eis-Orden.png'),
            Badge(name='Dark Badge', cap=0, image='https://www.pokewiki.de/images/4/4a/Unlicht-Orden.png'),
            Badge(name='Dragon Badge', cap=0, image='https://www.pokewiki.de/images/b/b7/Drachen-Orden.png'),
            Badge(name='Champion Ribbon', cap=0, image='https://www.pokewiki.de/images/0/04/Band_des_Galar-Champs.png'),
        ]
    }
