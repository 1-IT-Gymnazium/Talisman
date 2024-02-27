# from enum import Enum
import pygame
import random


class DeckShuffle:
    def __init__(self, deck):
        self.cards = []
        self.deck = deck
        self.screen = None
        self.image = None

    def shuffle(self):
        random.shuffle(self.deck)

    def display(self, screen):
        self.screen = screen
        self.image = pygame.image.load("backside.png")
        screen.blit(self.image, (0, 200))


class Character:
    def __init__(self, name, strength, craft, life, fate, gold):
        self.name = name
        self.strength = strength
        self.craft = craft
        self.life = life
        self.gold = 0
        self.talisman = False
        self.fate = fate
        self.gold = gold

    def display(self):
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        # screen.blit(text, (self.x + 10, self.y + 10))


class Card:
    def __init__(self, image, types):
        self.screen = None
        self.image_path = image
        self.types = types
        self.image = pygame.image.load(image)
        
    def display(self, screen):
        self.screen = screen
        screen.blit(self.image, (0, 400))


class ObjectCard(Card):
    def __init__(self, name, image, effect):
        super().__init__(image, "Object")
        self.name = name
        self.effect = effect


class MagicObject(Card):
    def __init__(self, name, image, effect):
        super().__init__(image, "MagicObject")
        self.name = name
        self.effect = effect


class Follower(Card):
    def __init__(self, name, image, effect):
        super().__init__(image, "Follower")
        self.name = name
        self.effect = effect


class Stranger(Card):
    def __init__(self, name, image, effect):
        super().__init__(image, "Stranger")
        self.name = name
        self.effect = effect


class Enemy(Card):
    def __init__(self, name, image, effect, craft, strength):
        super().__init__(image, "Enemy")
        self.name = name
        self.effect = effect
        self.craft = craft
        self.strength = strength


class Place(Card):
    def __init__(self, name, image, effect):
        super().__init__(image, "Place")
        self.name = name
        self.effect = effect


class Spell(Card):
    def __init__(self, name, image, effect):
        super().__init__(image, "Spell")
        self.name = name
        self.effect = effect


class Dice:
    dice_w = 190
    dice_h = 190
    dice_screen = pygame.display.set_mode((dice_h, dice_w))

    def __init__(self, sides=6):
        self.sides = sides
        self.value = 1
        self.images = [pygame.image.load(f'die{i}.png') for i in range(1, sides + 1)]
        self.visible = False

    # def toggle_visibility(self):
    #     self.visible = not self.visible

    def roll(self):
        self.value = random.randint(1, self.sides)

    def display(self, screen, x, y):
        # self.toggle_visibility()
        screen.blit(pygame.transform.scale(self.images[self.value - 1], (self.dice_w, self.dice_h)), (x, y))
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.value), True, (255, 255, 255))


def main():
    pygame.init()

    screen_height = 1080
    screen_width = 1920
    row = 7
    columns = 7
    board_height = 900
    board_width = 1600

    cell_width = board_width // columns
    cell_height = board_height // row

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # screen_width, screen_height = pygame.display.get_surface().get_size()

    image = pygame.image.load("board.png")
    image1 = pygame.transform.scale(image, (board_width, board_height))

    # CardsType = [
    #     Cards("./ObjectCards", "Object"),
    #     Cards("./MagicObjects", "MagicObject"),
    #     Cards("./FollowerCards", "Follower"),
    #     Cards("./StrangerCards", "Stranger"),
    #     Cards("./EnemyCards", "Enemy"),
    #     Cards("./Place", "Place"),
    #     Cards("./Spell", "Spell")
    # ]

    enemycards = [
        Enemy("Ape", "./EnemyCards/Ape.png", "yep", "0", "3"),
        Enemy("Bandit", "./EnemyCards/Bandit.png", "yep", "0", "4"),
        Enemy("Bear", "./EnemyCards/Bear.png", "yep", "0", "3"),
        Enemy("Demon", "./EnemyCards/Demon.png", "yep", "10", "0"),
        Enemy("Dopplergang", "./EnemyCards/Dopplergang.png", "yep", "0", "7"),
        Enemy("Dragon", "./EnemyCards/Dragon.png", "yep", "0", "7"),
        Enemy("Ghost", "./EnemyCards/Ghost.png", "yep", "4", "0"),
        Enemy("Giant", "./EnemyCards/Giant.png", "yep", "0", "6"),
        Enemy("Goblin", "./EnemyCards/Goblin.png", "yep", "0", "2"),
        Enemy("Hobgoblin", "./EnemyCards/Hobgoblin.png", "yep", "0", "3"),
        Enemy("Lemure", "./EnemyCards/Lemure.png", "yep", "1", "0"),
        Enemy("Lion", "./EnemyCards/Lion.png", "yep", "0", "3"),
        Enemy("Orge", "./EnemyCards/Orge.png", "yep", "0", "5"),
        Enemy("Serpent", "./EnemyCards/Serpent.png", "yep", "0", "4"),
        Enemy("Shadow", "./EnemyCards/Shadow.png", "yep", "2", "0"),
        Enemy("Spectre", "./EnemyCards/Spectre.png", "yep", "3", "0"),
        Enemy("WildBoar", "./EnemyCards/WildBoar.png", "yep", "0", "1"),
        Enemy("Wolf", "./EnemyCards/Wolf.png", "yep", "0", "2"),
        Enemy("Wraith", "./EnemyCards/Wraith.png", "yep", "5", "0"),
    ]

    objectcards = [
        ObjectCard("Armour", "./ObjectCards/Armour.png", "yep"),
        ObjectCard("Axe", "./ObjectCards/Axe.png", "yep"),
        ObjectCard("BagOfGold", "./ObjectCards/BagOfGold.png", "yep"),
        ObjectCard("Helmet", "./ObjectCards/Helmet.png", "yep"),
        ObjectCard("Shield", "./ObjectCards/Shield.png", "yep"),
        ObjectCard("Sword", "./ObjectCards/Sword.png", "yep"),
        ObjectCard("TwoBagsOfGold", "./ObjectCards/TwoBagsOfGold.png", "yep"),
        ObjectCard("WaterBottle", "./ObjectCards/WaterBottle.png", "yep"),
    ]

    followercards = [
        Follower("Alchemist", "./FollowerCards/Alchemist.png", "yep"),
        Follower("Gnome", "./FollowerCards/Gnome.png", "yep"),
        Follower("Guide", "./FollowerCards/Guide.png", "yep"),
        Follower("Hag", "./FollowerCards/Hag.png", "yep"),
        Follower("Maiden", "./FollowerCards/Maiden.png", "yep"),
        Follower("Mercenary", "./FollowerCards/Mercenary.png", "yep"),
        Follower("Mule", "./FollowerCards/Mule.png", "yep"),
        Follower("Pixie", "./FollowerCards/Pixie.png", "yep"),
        Follower("Poltergeist", "./FollowerCards/Poltergeist.png", "yep"),
        Follower("Prince", "./FollowerCards/Prince.png", "yep"),
        Follower("Princess", "./FollowerCards/Princess.png", "yep"),
        Follower("Unicorn", "./FollowerCards/Unicorn.png", "yep")
    ]

    magicobjectcards = [
        MagicObject("Amulet", "./MagicObjects/Amulet.png", "yep"),
        MagicObject("Cross", "./MagicObjects/Cross.png", "yep"),
        MagicObject("HolyGrail", "./MagicObjects/HolyGrail.png", "yep"),
        MagicObject("HolyLance", "./MagicObjects/HolyLance.png", "yep"),
        MagicObject("MagicBelt", "./MagicObjects/MagicBelt.png", "yep"),
        MagicObject("OrbOfKnowledge", "./MagicObjects/OrbOfKnowledge.png", "yep"),
        MagicObject("PotionOfStrength", "./MagicObjects/PotionOfStrength.png", "yep"),
        MagicObject("Ring", "./MagicObjects/Ring.png", "yep"),
        MagicObject("RuneSword", "./MagicObjects/RuneSword.png", "yep"),
        MagicObject("SolomonCrown", "./MagicObjects/SolomonCrown.png", "yep"),
        MagicObject("Talisman", "./MagicObjects/Talisman.png", "yep"),
        MagicObject("Wand", "./MagicObjects/Wand.png", "yep"),

    ]
    strangercards = [
        Stranger("Enchanter", "./StrangerCards/Enchanter.png", "yep"),
        Stranger("Fairy", "./StrangerCards/Fairy.png", "yep"),
        Stranger("Healer", "./StrangerCards/Healer.png", "yep"),
        Stranger("Hermit", "./StrangerCards/Hermit.png", "yep"),
        Stranger("Instructor", "./StrangerCards/Instructor.png", "yep"),
        Stranger("Mage", "./StrangerCards/Mage.png", "yep"),
        Stranger("Phantom", "./StrangerCards/Phantom.png", "yep"),
        Stranger("Sorcerer", "./StrangerCards/Sorcerer.png", "yep"),
        Stranger("Witch", "./StrangerCards/Witch.png", "yep")
    ]

    placecards = [
        Place("Cave", "./Place/Cave.png", "Yep"),
        Place("FountainOfW", "./Place/FountainOfW.png", "Yep"),
        Place("MagicPortal", "./Place/MagicPortal.png", "Yep"),
        Place("MagicStream", "./Place/MagicStream.png", "Yep"),
        Place("Market", "./Place/Market.png", "Yep"),
        Place("Marsh", "./Place/Marsh.png", "Yep"),
        Place("Maze", "./Place/Maze.png", "Yep"),
        Place("PoolOfLife", "./Place/PoolOfLife.png", "Yep"),
        Place("Shrine", "./Place/Shrine.png", "Yep"),
    ]

    spellcards = [
        Spell("Acqusition", "./Spell/Acqusition.png", "yep"),
        Spell("Alchemy", "./Spell/Alchemy.png", "yep"),
        Spell("CounterSpell", "./Spell/CounterSpell.png", "yep"),
        Spell("DestroyMagic", "./Spell/DestroyMagic.png", "yep"),
        Spell("Destruction", "./Spell/Destruction.png", "yep"),
        Spell("Divination", "./Spell/Divination.png", "yep"),
        Spell("Healing", "./Spell/Healing.png", "yep"),
        Spell("Hex", "./Spell/Hex.png", "yep"),
        Spell("Immobility", "./Spell/Immobility.png", "yep"),
        Spell("Invisibility", "./Spell/Invisibility.png", "yep"),
        Spell("Mesmerism", "./Spell/Mesmerism.png", "yep"),
        Spell("Nullify", "./Spell/Nullify.png", "yep"),
        Spell("Preservation", "./Spell/Preservation.png", "yep"),
        Spell("PsionicBlast", "./Spell/PsionicBlast.png", "yep"),
        Spell("Random", "./Spell/Random.png", "yep"),
        Spell("Teleport", "./Spell/Teleport.png", "yep"),
        Spell("TemporalWarp", "./Spell/TemporalWarp.png", "yep")

    ]

    characters = [
        Character("Warrior", 4, 2, 5, 1, 1),
        Character("Assassin", 3, 3, 4, 3, 1),
        Character("Druid", 2, 4, 4, 4, 1),
        Character("Dwarf", 3, 3, 5, 5, 1),
        Character("Elf", 3, 4, 4, 3, 1),
        Character("Ghoul", 2, 4, 4, 4, 1),
        Character("Minstrel", 2, 4, 4, 5, 1),
        Character("Monk", 2, 3, 4, 5, 1),
        Character("Priest", 2, 4, 4, 5, 1),
        Character("Prophetess", 2, 4, 4, 2, 1),
        Character("Sorceress", 2, 4, 4, 3, 1),
        Character("Thief", 3, 3, 4, 2, 1),
        Character("Troll", 6, 1, 6, 1, 1),
        Character("Wizard", 2, 5, 4, 3, 1),
        Character("Toad", 1, 0, 0, 0, 1)
    ]
    deck = [enemycards, followercards, magicobjectcards, objectcards, placecards, spellcards, strangercards]
    deck_shuffler = DeckShuffle(deck)
    deck_shuffler.shuffle()
    deck_shuffler.display(screen)

    my_die = Dice()

    screen.blit(image1, (screen_width / 10, screen_height / 10))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not my_die.visible:
                        my_die.roll()
                        my_die.display(screen, 0, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    random_card_type = random.choice(deck)
                    random_card = random.choice(random_card_type)
                    random_card.display(screen)
                    ## todo: MÍCHAT BALÍČEK JEN JEDNOU
                    ## TODO: VYTVOŘIT ODKLÁDACÍ BALÍČEK
                    ## TODO: HRÁČOVI KARTY
                    ## TODO: VYŘEŠIT PROTIVNÍKOVI KARTY
        for row in range(row):
            for col in range(columns):
                x = col * cell_width
                y = row * cell_height
                pygame.draw.rect(screen, (0, 0, 0),
                                 (x + screen_width / 10, y + screen_height / 10, cell_width, cell_height), 1)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
