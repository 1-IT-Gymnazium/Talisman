# from enum import Enum
import pygame, sys
import random
from button import Button


pygame.init()

Screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BackGround = pygame.image.load("Background.png")

num_players = 0
selected_characters = [None] * num_players


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
    def __init__(self, name, image, strength, craft, life, fate, gold):
        self.name = name
        self.strength = strength
        self.craft = craft
        self.life = life
        self.gold = 0
        self.talisman = False
        self.fate = fate
        self.gold = gold
        self.image = image

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


def get_font(size):
    return pygame.font.Font("Stuff/font.ttf", size)


def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        Screen.blit(BackGround, (0, 0))

        MenuMousePos = pygame.mouse.get_pos()

        MenuText = get_font(100).render("Main Menu", True, "#b68f40")
        MenuRect = MenuText.get_rect(center=(640, 100))

        PlayButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(640, 250),
                            text_input="PLAY", font=get_font(75), base_color="#b68f40", hovering_color="Blue")
        QuitButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(640, 550),
                            text_input="QUIT", font=get_font(75), base_color="#b68f40", hovering_color="Blue")

        Screen.blit(MenuText, MenuRect)

        for button in [PlayButton, QuitButton]:
            button.changeColor(MenuMousePos)
            button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PlayButton.checkForInput(MenuMousePos):
                    PlayerNum()
                if QuitButton.checkForInput(MenuMousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()


def PlayerNum():
    pygame.display.set_caption("Player_Selection")
    global num_players
    while True:
        CharMousePos = pygame.mouse.get_pos()

        Screen.fill("black")

        CharText = get_font(100).render("Player Selection", True, "#b68f40")
        CharRect = CharText.get_rect(center=(640, 100))

        TwoPlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(640, 250),
                                  text_input="2 Players", font=get_font(50), base_color="#b68f40",
                                  hovering_color="Blue")
        ThreePlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(640, 400),
                                    text_input="3 Players", font=get_font(50), base_color="#b68f40",
                                    hovering_color="Blue")
        FourPlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(640, 400),
                                   text_input="4 Players", font=get_font(50), base_color="#b68f40",
                                   hovering_color="Blue")

        Screen.blit(CharText, CharRect)

        for button in [TwoPlayersButton, ThreePlayersButton, FourPlayersButton]:
            button.changeColor(CharMousePos)
            button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if TwoPlayersButton.checkForInput(CharMousePos):
                    num_players = 2
                    CharSelection()
                elif ThreePlayersButton.checkForInput(CharMousePos):
                    num_players = 3
                    CharSelection()
                elif FourPlayersButton.checkForInput(CharMousePos):
                    num_players = 4
                    CharSelection()

        pygame.display.update()


def CharSelection():
    pygame.display.set_caption("Character_Selection")
    global num_players
    global selected_characters

    character_images = [
        pygame.image.load("Characters/Assassin.png"),
        pygame.image.load("Characters/Druid.png"),
        pygame.image.load("Characters/Dwarf.png"),
        pygame.image.load("Characters/Elf.png"),
        pygame.image.load("Characters/Ghoul.png"),
        pygame.image.load("Characters/Minstrel.png"),
        pygame.image.load("Characters/Monk.png"),
        pygame.image.load("Characters/Priest.png"),
        pygame.image.load("Characters/Prophetess.png"),
        pygame.image.load("Characters/Sorceress.png"),
        pygame.image.load("Characters/Thief.png"),
        pygame.image.load("Characters/Toad.png"),
        pygame.image.load("Characters/Troll.png"),
        pygame.image.load("Characters/Warrior.png"),
        pygame.image.load("Characters/Wizard.png")
    ]
    buttons = []

    for i, image in enumerate(character_images):
        x = 150 + (i % 5) * 200
        y = 150 + (i // 5) * 200
        button = Button(image, (x, y), i, None, None)
        buttons.append(button)

    while True:
        CharMousePos = pygame.mouse.get_pos()

        Screen.fill("black")

        CharText = get_font(100).render("Character Selection", True, "#b68f40")
        CharRect = CharText.get_rect(center=(640, 100))

        ##AssassinButton = Button(image=pygame.image.load("Characters/Assassin.png"), pos=(640, 250),
        ##                        text_input=None, font=None, base_color=None,
        ##                        hovering_color=None)
        ##DruidButton = Button(image=pygame.image.load("Characters/Druid.png"), pos=(640, 250),
        ##                     text_input=None, font=None, base_color=None,
        ##                     hovering_color=None)
        ##DwarfButton = Button(image=pygame.image.load("Characters/Dwarf.png"), pos=(640, 250),
        ##                     text_input=None, font=None, base_color=None,
        ##                     hovering_color=None)
        ##ElfButton = Button(image=pygame.image.load("Characters/Elf.png"), pos=(640, 250),
        ##                   text_input=None, font=None, base_color=None,
        ##                   hovering_color=None)
        ##GhoulButton = Button(image=pygame.image.load("Characters/Ghoul.png"), pos=(640, 250),
        ##                     text_input=None, font=None, base_color=None,
        ##                     hovering_color=None)
        ##MinstrelButton = Button(image=pygame.image.load("Characters/Minstrel.png"), pos=(640, 250),
        ##                        text_input=None, font=None, base_color=None,
        ##                        hovering_color=None)
        ##MonkButton = Button(image=pygame.image.load("Characters/Monk.png"), pos=(640, 250),
        ##                    text_input=None, font=None, base_color=None,
        ##                    hovering_color=None)
        ##PriestButton = Button(image=pygame.image.load("Characters/Priest.png"), pos=(640, 250),
        ##                      text_input=None, font=None, base_color=None,
        ##                      hovering_color=None)
        ##ProphetessButton = Button(image=pygame.image.load("Characters/Prophetess.png"), pos=(640, 250),
        ##                          text_input=None, font=None, base_color=None,
        ##                          hovering_color=None)
        ##SorceressButton = Button(image=pygame.image.load("Characters/Sorceress.png"), pos=(640, 250),
        ##                         text_input=None, font=None, base_color=None,
        ##                         hovering_color=None)
        ##ThiefButton = Button(image=pygame.image.load("Characters/Thief.png"), pos=(640, 250),
        ##                     text_input=None, font=None, base_color=None,
        ##                     hovering_color=None)
        ##ToadButton = Button(image=pygame.image.load("Characters/Toad.png"), pos=(640, 250),
        ##                    text_input=None, font=None, base_color=None,
        ##                    hovering_color=None)
        ##TrollButton = Button(image=pygame.image.load("Characters/Troll.png"), pos=(640, 250),
        ##                     text_input=None, font=None, base_color=None,
        ##                     hovering_color=None)
        ##WarriorButton = Button(image=pygame.image.load("Characters/Warrior.png"), pos=(640, 250),
        ##                       text_input=None, font=None, base_color=None,
        ##                       hovering_color=None)
        ##WizardButton = Button(image=pygame.image.load("Characters/Wizard.png"), pos=(640, 250),
        ##                      text_input=None, font=None, base_color=None,
        ##                      hovering_color=None)
        Screen.blit(CharText, CharRect)

        for button in buttons:
            button.changeColor(CharMousePos)
            button.update(Screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        if button.checkForInput(CharMousePos):
                            selected_characters[i % num_players] = button.character

            if all(character is not None for character in selected_characters):
                Game()
        pygame.display.flip()


def Game():
    pygame.display.set_caption("Game")

    screen_height = 1080
    screen_width = 1920
    row = 7
    columns = 7
    board_height = 900
    board_width = 1600

    cell_width = board_width // columns
    cell_height = board_height // row

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
        Character("Warrior", "./Characters/Warrior.png", 4, 2, 5, 1, 1),
        Character("Assassin", "./Characters/Assassin.png", 3, 3, 4, 3, 1),
        Character("Druid", "./Characters/Druid.png", 2, 4, 4, 4, 1),
        Character("Dwarf", "./Characters/Dwarf.png", 3, 3, 5, 5, 1),
        Character("Elf", "./Characters/Elf.png", 3, 4, 4, 3, 1),
        Character("Ghoul", "./Characters/Ghoul.png", 2, 4, 4, 4, 1),
        Character("Minstrel", "./Characters/Minstrel.png", 2, 4, 4, 5, 1),
        Character("Monk", "./Characters/Monk.png", 2, 3, 4, 5, 1),
        Character("Priest", "./Characters/Priest.png", 2, 4, 4, 5, 1),
        Character("Prophetess", "./Characters/Prophetess.png", 2, 4, 4, 2, 1),
        Character("Sorceress", "./Characters/Sorceress.png", 2, 4, 4, 3, 1),
        Character("Thief", "./Characters/Thief.png", 3, 3, 4, 2, 1),
        Character("Troll", "./Characters/Troll.png", 6, 1, 6, 1, 1),
        Character("Wizard", "./Characters/Wizard.png", 2, 5, 4, 3, 1),
        Character("Toad", "./Characters/Toad.png", 1, 0, 0, 0, 1)
    ]
    deck = [enemycards, followercards, magicobjectcards, objectcards, placecards, spellcards, strangercards]
    deck_shuffler = DeckShuffle(deck)
    deck_shuffler.shuffle()
    deck_shuffler.display(Screen)

    my_die = Dice()

    Screen.blit(image1, (screen_width / 10, screen_height / 10))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not my_die.visible:
                        my_die.roll()
                        my_die.display(Screen, 0, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    random_card_type = random.choice(deck)
                    random_card = random.choice(random_card_type)
                    random_card.display(Screen)
                    ## todo: MÍCHAT BALÍČEK JEN JEDNOU
                    ## TODO: VYTVOŘIT ODKLÁDACÍ BALÍČEK
                    ## TODO: HRÁČOVI KARTY
                    ## TODO: VYŘEŠIT PROTIVNÍKOVI KARTY
        for row in range(row):
            for col in range(columns):
                x = col * cell_width
                y = row * cell_height
                pygame.draw.rect(Screen, (0, 0, 0),
                                 (x + screen_width / 10, y + screen_height / 10, cell_width, cell_height), 1)

        pygame.display.update()
    pygame.quit()

