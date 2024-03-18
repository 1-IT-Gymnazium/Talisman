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
        self.position = 0

    def set_position(self, x, y, scale_x, scale_y):
        self.position = (int(x * scale_x), int(y * scale_y))

    def display(self, screen, font):
        name_surface = font.render(self.name, True, (0, 0, 255))
        text_position = self.position
        screen.blit(name_surface, text_position)


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
    def __init__(self, x, y, section, up=None, down=None, left=None, right=None):
        self.x = x
        self.y = y
        self.section = section
        self.up_neighbor_index = up
        self.down_neighbor_index = down
        self.left_neighbor_index = left
        self.right_neighbor_index = right


def get_font(size):
    return pygame.font.Font("Stuff/font.ttf", size)


def get_available_directions(position_index, board_sections):
    current_section = board_sections[position_index]
    available_directions = {'up': False, 'down': False, 'left': False, 'right': False}

    if current_section.up_neighbor_index is not None:
        available_directions['up'] = True
    if current_section.down_neighbor_index is not None:
        available_directions['down'] = True
    if current_section.left_neighbor_index is not None:
        available_directions['left'] = True
    if current_section.right_neighbor_index is not None:
        available_directions['right'] = True

    return available_directions


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

current_player_index = 0


def Game(selected_characetrs):
    pygame.display.set_caption("Game")
    Screen.fill("black")
    global BoardSection

    game_board = pygame.image.load("./board.png")

    def load_and_scale_image(image, scale_x, scale_y):
        image = pygame.image.load(image)
        image_width = image.get_width() * scale_x
        image_height = image.get_height() * scale_y
        scaled_image = pygame.transform.scale(image, (int(image_width), int(image_height)))
        return scaled_image

    game_board = load_and_scale_image("./board.png", scale_factor_width, scale_factor_height)

    Board_Section = [
        BoardSection(395, 135, "Village", down=23, right=1),  # 0
        BoardSection(579, 135, "Forest", left=0, right=2),  # 1
        BoardSection(770, 135, "Graveyard", left=1, right=3),  # 2
        BoardSection(956, 135, "Forest", left=2, right=4),  # 3
        BoardSection(1158, 135, "Sentinel", left=3, right=5),  # 4
        BoardSection(1351, 135, "Forest", left=4, right=6),  # 5
        BoardSection(1545, 135, "Chapel", left=5, down=7),  # 6
        BoardSection(1545, 249, "Forest", down=8, up=6),  # 7
        BoardSection(1545, 377, "Cracks", down=9, up=7),  # 8
        BoardSection(1545, 508, "Forest", down=10, up=8),  # 9
        BoardSection(1545, 632, "Forest", down=11, up=9),  # 10
        BoardSection(1545, 753, "Forest", down=12, up=10),  # 11
        BoardSection(1545, 875, "City", left=13, up=11),  # 12
        BoardSection(1339, 875, "Forest", left=14, right=12),  # 13
        BoardSection(1134, 75, "Forest", left=15, right=13),  # 14
        BoardSection(924, 875, "Forest", left=16, right=14),  # 15
        BoardSection(750, 875, "ElvForest", left=17, right=15),  # 16
        BoardSection(579, 875, "Forest", left=18, right=16),  # 17
        BoardSection(396, 875, "Tavern", up=19, left=17),  # 18
        BoardSection(365, 757, "Forest", up=20, down=18),  # 19
        BoardSection(365, 628, "Ruins", up=21, down=19),  # 20
        BoardSection(365, 469, "Forest", up=22, down=20),  # 21
        BoardSection(365, 357, "Forest", up=23, down=21),  # 22
        BoardSection(365, 267, "Forest", up=0, down=22)  # 23
    ]

   # for event in pygame.event.get():
   #     if event.type == pygame.KEYDOWN:
   #         if event.key == pygame.K_LEFT:
   #             current_character.move_character('left', Board_Section)
   #         elif event.key == pygame.K_RIGHT:
   #             current_character.move_character('right', Board_Section)
   #         elif event.key == pygame.K_UP:
   #             current_character.move_character('up', Board_Section)
   #         elif event.key == pygame.K_DOWN:
   #             current_character.move_character('down', Board_Section)

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

    Screen.blit(game_board, (190, 60))

    current_characters = selected_characters[current_player_index]

       #current_player_index += 1 THIS WILL BE ADDED AT THE END OF THE ROUND
       #if current_player_index >= len(selected_characters):  # Check if we've gone past the last player
       #    current_player_index = 0

    # Create a mapping of character names to their Character objects
    character_mapping = {character.name: character for character in characters}

    font = get_font(40)

    # selected_characters is a list of lists, with each sublist containing character names
    for player_characters in selected_characters:
        for character_name in player_characters:
            character = character_mapping.get(character_name)
            if character:
                # Find the BoardSection for the character's starting location
                matching_section = next((section for section in Board_Section if section.section == character.start),
                                        None)
                if matching_section:
                    character.set_position(matching_section.x, matching_section.y, scale_factor_width,
                                           scale_factor_height)
                    character.display(Screen, font)

    run = True
    while run:
        if current_characters:  # Ensure there's at least one character
            current_char_name = current_characters[0]
            player_turn_text = get_font(75).render(f"{current_char_name}'s Turn", True, "#b68f40")
            player_turn_rect = player_turn_text.get_rect(center=(Screen.get_width() // 2, 30))
            Screen.blit(player_turn_text, player_turn_rect)
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
