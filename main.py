# from enum import Enum
import random
import pygame
import sys
from button import Button

pygame.init()

default_resolution = pygame.display.Info()
current_screen_width = default_resolution.current_w
current_screen_height = default_resolution.current_h

default_resolution_width = 1920
default_resolution_height = 1080

scale_factor_width = current_screen_width / default_resolution_width
scale_factor_height = current_screen_height / default_resolution_height

Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")
BackGround = pygame.image.load("Background.png")


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
    def __init__(self, name, image, strength, craft, life, fate, gold, start):
        self.name = name
        self.strength = strength
        self.craft = craft
        self.life = life
        self.gold = 0
        self.talisman = False
        self.fate = fate
        self.gold = gold
        self.start = start
        self.image = image
        self.position = (0, 0)

    def set_position(self, x, y, scale_x, scale_y):
        scaled_x = int(x * scale_x)
        scaled_y = int(y * scale_y)
        self.position = (int(x * scale_x), int(y * scale_y))

    def display(self, screen, font):
        name_surface = font.render(self.name, True, (255, 0, 0))
        name_rect = name_surface.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(name_surface, name_rect)


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

    def __init__(self, sides=6, width=190, height=190):
        self.sides = sides
        self.value = 1
        self.images = [pygame.image.load(f'die{i}.png') for i in range(1, sides + 1)]
        self.visible = False
        self.width = width
        self.height = height

    def roll(self):
        self.value = random.randint(1, self.sides)

    def display(self, screen, x, y):
        # self.toggle_visibility()
        screen.blit(pygame.transform.scale(self.images[self.value - 1], (self.width, self.height)), (x, y))


class BoardSection:
    def __init__(self, x, y, section):
        self.x = x
        self.y = y
        self.section = section


def get_font(size):
    return pygame.font.Font("Stuff/font.ttf", size)


characters = [
    Character("Assassin", "./Characters/Assassin.png", 3, 3, 4, 3, 1, "City"),
    Character("Druid", "./Characters/Druid.png", 2, 4, 4, 4, 1, "Chapel"),
    Character("Dwarf", "./Characters/Dwarf.png", 3, 3, 5, 5, 1, "Cracks"),
    Character("Elf", "./Characters/Elf.png", 3, 4, 4, 3, 1, "ElvForest"),
    Character("Ghoul", "./Characters/Ghoul.png", 2, 4, 4, 4, 1, "Village"),
    Character("Minstrel", "./Characters/Minstrel.png", 2, 4, 4, 5, 1, "Tavern"),
    Character("Monk", "./Characters/Monk.png", 2, 3, 4, 5, 1, "Village"),
    Character("Priest", "./Characters/Priest.png", 2, 4, 4, 5, 1, "Chapel"),
    Character("Prophetess", "./Characters/Prophetess.png", 2, 4, 4, 2, 1, "Chapel"),
    Character("Sorceress", "./Characters/Sorceress.png", 2, 4, 4, 3, 1, "City"),
    Character("Thief", "./Characters/Thief.png", 3, 3, 4, 2, 1, "City"),
    Character("Troll", "./Characters/Troll.png", 6, 1, 6, 1, 1, "Cracks"),
    Character("Wizard", "./Characters/Wizard.png", 2, 5, 4, 3, 1, "Chapel"),
    Character("Warrior", "./Characters/Warrior.png", 4, 2, 5, 1, 1, "Tavern")
]


def Game(selected_characetrs):
    pygame.display.set_caption("Game")
    Screen.fill("black")

    game_board = pygame.image.load("./board.png")
    # Get the dimensions of the game board
    board_width = 1600
    board_height = 900

    def load_and_scale_image(image, scale_x, scale_y):
        image = pygame.image.load(image)
        image_width = image.get_width() * scale_x
        image_height = image.get_height() * scale_y
        scaled_image = pygame.transform.scale(image, (int(image_width), int(image_height)))
        return scaled_image

    game_board = load_and_scale_image("./board.png", scale_factor_width, scale_factor_height)

    def scale_positionx(x, scale_x):
        return int(x * scale_x)

    def scale_positiony(y, scale_y):
        return int(y * scale_y)

    Board_Section = [
        BoardSection(scale_positionx(235, scale_factor_width), scale_positiony(75, scale_factor_height), "Village"),
        BoardSection(scale_positionx(419, scale_factor_width), scale_positiony(75, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(610, scale_factor_width), scale_positiony(75, scale_factor_height), "Graveyard"),
        BoardSection(scale_positionx(796, scale_factor_width), scale_positiony(75, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(998, scale_factor_width), scale_positiony(75, scale_factor_height), "Sentinel"),
        BoardSection(scale_positionx(1191, scale_factor_width), scale_positiony(75, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(1385, scale_factor_width), scale_positiony(75, scale_factor_height), "Chapel"),
        BoardSection(scale_positionx(1385, scale_factor_width), scale_positiony(189, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(1385, scale_factor_width), scale_positiony(317, scale_factor_height), "Cracks"),
        BoardSection(scale_positionx(1385, scale_factor_width), scale_positiony(448, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(1385, scale_factor_width), scale_positiony(572, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(1385, scale_factor_width), scale_positiony(693, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(1385, scale_factor_width), scale_positiony(815, scale_factor_height), "City"),
        BoardSection(scale_positionx(1179, scale_factor_width), scale_positiony(815, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(974, scale_factor_width), scale_positiony(815, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(764, scale_factor_width), scale_positiony(815, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(590, scale_factor_width), scale_positiony(815, scale_factor_height), "ElvForest"),
        BoardSection(scale_positionx(419, scale_factor_width), scale_positiony(815, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(236, scale_factor_width), scale_positiony(815, scale_factor_height), "Tavern"),
        BoardSection(scale_positionx(205, scale_factor_width), scale_positiony(697, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(205, scale_factor_width), scale_positiony(568, scale_factor_height), "Ruins"),
        BoardSection(scale_positionx(205, scale_factor_width), scale_positiony(409, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(205, scale_factor_width), scale_positiony(297, scale_factor_height), "Forest"),
        BoardSection(scale_positionx(205, scale_factor_width), scale_positiony(207, scale_factor_height), "Forest")
    ]

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

    deck = [enemycards, followercards, magicobjectcards, objectcards, placecards, spellcards, strangercards]
    deck_shuffler = DeckShuffle(deck)
    deck_shuffler.shuffle()
    deck_shuffler.display(Screen)

    my_die = Dice()

    Screen.blit(game_board, (160, 90))
    # Create a mapping of character names to their Character objects
    character_mapping = {character.name: character for character in characters}

    font = get_font(40)

    # selected_characters is a list of lists, with each sublist containing character names
    for player_characters in selected_characters:
        for character_name in player_characters:
            character = character_mapping.get(character_name)
            if character:
                # Find the BoardSection for the character's starting location
                matching_section = next((section for section in Board_Section if section.section == character.start), None)
                if matching_section:
                    character.set_position(matching_section.x, matching_section.y, scale_factor_width,
                                           scale_factor_height)
                    character.display(Screen, font)

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
                    ## TODO: VYTVOŘIT ODKLÁDACÍ BALÍČEK
                    ## TODO: HRÁČOVI KARTY
                    ## TODO: VYŘEŠIT PROTIVNÍKOVI KARTY
        pygame.display.update()
    pygame.quit()


def CharSelection(num_players):
    global selected_characters
    pygame.display.set_caption("Character_Selection")
    selected_characters = [[] for _ in range(num_players)]

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
        pygame.image.load("Characters/Troll.png"),
        pygame.image.load("Characters/Warrior.png"),
        pygame.image.load("Characters/Wizard.png")
    ]

    stuff = [pygame.image.load("Stuff/Brick.png")] * 14
    current_player = 1  # Initialize the current player index

    while current_player <= num_players:
        Screen.fill("black")

        CharText = get_font(75).render(f"Player {current_player} Character Selection", True, "#b68f40")
        CharRect = CharText.get_rect(center=(960, 100))
        Screen.blit(CharText, CharRect)  # Blit the CharText

        character_buttons = []

        for i, character in enumerate(characters):
            x_offset = (i % 5) * 200
            y_offset = (i // 5) * 200 + (i // 5) * 75
            button = Button(image=pygame.image.load("Stuff/Brick.png"), pos=(520 + x_offset, 300 + y_offset),
                            text_input=character.name, font=get_font(25), base_color="#b68f40",
                            hovering_color="Blue", char_name=character.name)
            character_buttons.append(button)

        for button in character_buttons:
            button.update(Screen)

        for i, image in enumerate(character_images):
            x_offset = (i % 5) * 200
            y_offset = (i // 5) * 200 + (i // 5) * 75 - 20
            Screen.blit(image, (445 + x_offset, 200 + y_offset))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in character_buttons:
                    if button.checkForInput(mouse_pos):
                        selected_characters[current_player - 1].append(button.char_name)
                        current_player += 1
                        break
        if current_player > num_players:
            # Proceed to game or next step after the last selection
            Game(selected_characters)

        pygame.display.update()


def PlayerNum():
    pygame.display.set_caption("Player_Selection")
    while True:
        CharMousePos = pygame.mouse.get_pos()

        Screen.fill("black")

        CharText = get_font(75).render("Player Selection", True, "#b68f40")
        CharRect = CharText.get_rect(center=(Screen.get_width() // 2, 200))

        TwoPlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 400),
                                  text_input="2 Players", font=get_font(50), base_color="#b68f40",
                                  hovering_color="Blue")
        ThreePlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 600),
                                    text_input="3 Players", font=get_font(50), base_color="#b68f40",
                                    hovering_color="Blue")
        FourPlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 800),
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
                    CharSelection(num_players)
                elif ThreePlayersButton.checkForInput(CharMousePos):
                    num_players = 3
                    CharSelection(num_players)
                elif FourPlayersButton.checkForInput(CharMousePos):
                    num_players = 4
                    CharSelection(num_players)

        pygame.display.update()


def main_menu():
    pygame.display.set_caption("Menu")
    while True:
        Screen.blit(BackGround, (0, 0))

        MenuMousePos = pygame.mouse.get_pos()

        MenuText = get_font(100).render("Main Menu", True, "#b68f40")
        MenuRect = MenuText.get_rect(center=(Screen.get_width() // 2, 200))

        PlayButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 450),
                            text_input="PLAY", font=get_font(75), base_color="#b68f40", hovering_color="Blue")
        QuitButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 750),
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
