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
        self.position_index = 0
        self.section_name = start
        self.deck = []

    def move(self, direction, board_sections):
        current_section = board_sections[self.position_index]

        # Determine the new position based on the direction
        if direction == 'up' and current_section.up_neighbor_index is not None:
            self.position_index = current_section.up_neighbor_index
        elif direction == 'down' and current_section.down_neighbor_index is not None:
            self.position_index = current_section.down_neighbor_index
        elif direction == 'left' and current_section.left_neighbor_index is not None:
            self.position_index = current_section.left_neighbor_index
        elif direction == 'right' and current_section.right_neighbor_index is not None:
            self.position_index = current_section.right_neighbor_index

        new_section = board_sections[self.position_index]
        self.set_position(new_section.x, new_section.y, scale_factor_width, scale_factor_height)

    def current_section_name(self):
        return self.section_name

    def set_position(self, x, y, scale_x, scale_y):
        self.position = (int(x * scale_x), int(y * scale_y))

    def display(self, screen, font):
        name_surface = font.render(self.name, True, (0, 0, 255))
        text_position = self.position
        screen.blit(name_surface, text_position)

    def display_attribute(self, screen):
        base_y = (1050 * scale_factor_height) + (current_screen_height - (1080 * scale_factor_height))

        attributes = ["Strength = " + str(self.strength),
                     "Craft = " + str(self.craft),
                     "Fate = " + str(self.fate),
                     "Gold = " + str(self.gold)]
        x_offset = 10
        font = get_font(30)

        total_width = sum(font.size(attr)[0] for attr in attributes) + x_offset * (len(attributes) - 1)

        # Calculate the starting x position to center the attributes block
        base_x = (current_screen_width - total_width) / 2  # Assuming current_screen_width is defined

        current_x = base_x
        for attribute in attributes:
            attribute_surface = font.render(attribute, True, (0, 0, 255))
            screen.blit(attribute_surface, (current_x, base_y))
            current_x += attribute_surface.get_width() + x_offset

    def clear_name(self, screen, font):
        self.display(screen, font)


class Card:
    def __init__(self, image, types):
        self.screen = None
        self.image_path = image
        self.types = types
        self.image = pygame.image.load(image)

    def display(self, screen):
        self.screen = screen
        screen.blit(self.image, (0, 500))


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
        self.screen = None
        self.sides = sides
        self.value = 1
        self.images = [pygame.image.load(f'die{i}.png') for i in range(1, sides + 1)]
        self.width = width
        self.height = height

    def roll(self):
        self.value = random.randint(1, self.sides)

    def display(self, screen):
        self.screen = screen
        image = self.images[self.value - 1]
        screen.blit(image, (0, 0))


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
    global BoardSection, current_player_index, event, drawn_card, current_character
    last_button_press_time = 0
    button_cooldown = 500

    game_board = pygame.image.load("./board.png")

    def load_and_scale_image(image, scale_x, scale_y):
        image = pygame.image.load(image)
        image_width = image.get_width() * scale_x
        image_height = image.get_height() * scale_y
        scaled_image = pygame.transform.scale(image, (int(image_width), int(image_height)))
        return scaled_image

    game_board = load_and_scale_image("./board.png", scale_factor_width, scale_factor_height)

    def handle_movement(event, characters, current_player_index, board_sections, screen, game_board, scale_x, scale_y):
        current_character = characters[current_player_index]
        direction = None
        if event.key == pygame.K_LEFT:
            direction = 'left'
        elif event.key == pygame.K_RIGHT:
            direction = 'right'
        elif event.key == pygame.K_UP:
            direction = 'up'
        elif event.key == pygame.K_DOWN:
            direction = 'down'

        if direction:
            current_character.move(direction, board_sections)
            # Redraw the character at the new position
            screen.blit(game_board, (190, 80))  # Reset the background
            for character in characters:
                character.display(screen, get_font(40))

    def display_current_state(screen, game_board, characters, current_player_index):
        screen.blit(game_board, (190, 80))
        for character in characters:
            character.display(screen, get_font(40))

    def get_current_section_name(character, board_sections):
        return board_sections[character.position_index].section

    def update_player_turn_text(screen, current_player_name):
        background_color = (0, 0, 0)
        clear_rect = pygame.Rect(screen.get_width() // 2 - 200, 20 - 35, 400, 70)  # Adjust the size as needed
        screen.fill(background_color, clear_rect)

        player_turn_text = get_font(70).render(f"{current_player_name}'s Turn", True, "#b68f40")
        player_turn_rect = player_turn_text.get_rect(center=(screen.get_width() // 2, 25))
        screen.blit(player_turn_text, player_turn_rect)

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
        BoardSection(1134, 875, "Forest", left=15, right=13),  # 14
        BoardSection(924, 875, "Forest", left=16, right=14),  # 15
        BoardSection(750, 875, "ElvForest", left=17, right=15),  # 16
        BoardSection(579, 875, "Forest", left=18, right=16),  # 17
        BoardSection(396, 875, "Tavern", up=19, right=17),  # 18
        BoardSection(365, 757, "Forest", up=20, down=18),  # 19
        BoardSection(365, 628, "Ruins", up=21, down=19),  # 20
        BoardSection(365, 469, "Forest", up=22, down=20),  # 21
        BoardSection(365, 357, "Forest", up=23, down=21),  # 22
        BoardSection(365, 267, "Forest", up=0, down=22)  # 23
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

    Screen.blit(game_board, (190, 80))

    # Create a mapping of character names to their Character objects
    character_mapping = {character.name: character for character in characters}

    font = get_font(40)

    selected_character_objects = []
    for player_characters in selected_characters:
        for character_name in player_characters:
            character = character_mapping.get(character_name)
            if character:
                # Find the matching section for the character's start location
                matching_section = next((index for index, section in enumerate(Board_Section) if
                                         section.section.lower() == character.start.lower()), None)
                if matching_section is not None:
                    character.position_index = matching_section  # Set the character's position index to the matching section index
                    character.set_position(Board_Section[matching_section].x, Board_Section[matching_section].y,
                                           scale_factor_width, scale_factor_height)
                    selected_character_objects.append(character)
                    character.display(Screen, font)

    run = True
    show_deck = False
    current_player_index = 0
    current_characters = selected_characters[current_player_index][0]
    update_player_turn_text(Screen, current_characters)
    current_char = character_mapping.get(current_characters)
    if current_char:
        current_char.display_attribute(Screen)

    while run:
        MousePos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        EndTurnButton = Button(image=pygame.image.load("Stuff/SmallRect.png"), pos=(1800 * scale_factor_width,100 * scale_factor_height),
                               text_input="End Turn", font=get_font(40), base_color="#b68f40",
                               hovering_color="Blue")

        EndTurnButton.changeColor(MousePos)
        EndTurnButton.update(Screen)

        TakeCardButton = Button(image=pygame.image.load("Stuff/SmallRect.png"), pos=(110 * scale_factor_width, 1000 * scale_factor_height),
                               text_input="Take Card", font=get_font(40), base_color="#b68f40",
                               hovering_color="Blue")
        TakeCardButton.changeColor(MousePos)
        TakeCardButton.update(Screen)

        ShowDeckButton = Button(image=pygame.image.load("Stuff/SmallRect.png"), pos=(110 * scale_factor_width, 1050 * scale_factor_height),
                               text_input="Show Deck", font=get_font(40), base_color="#b68f40",
                               hovering_color="Blue")
        ShowDeckButton.changeColor(MousePos)
        ShowDeckButton.update(Screen)

        rect_height = 50
        rect_y_start = current_screen_height - rect_height
        attributes_display_area = pygame.Rect(0, rect_y_start, current_screen_width, rect_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                handle_movement(event, selected_character_objects, current_player_index, Board_Section, Screen,
                                game_board, scale_factor_width, scale_factor_height)

                display_current_state(Screen, game_board, selected_character_objects, current_player_index)

                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        my_die.roll()
                        Screen.fill((0, 0, 0), (0, 0, my_die.width, my_die.height))
                        my_die.display(Screen)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        random_card_type = random.choice(deck)
                        random_card = random.choice(random_card_type)
                        random_card.display(Screen)
                        drawn_card = random_card

        if event.type == pygame.MOUSEBUTTONDOWN:
            if EndTurnButton.checkForInput(MousePos) and (current_time - last_button_press_time > button_cooldown):
                last_button_press_time = current_time
                Screen.fill((0, 0, 0), attributes_display_area)
                current_player_index += 1
                if current_player_index >= len(selected_characters):
                    current_player_index = 0
                # Ensure you update the text to reflect the new current player
                current_characters = selected_characters[current_player_index][0]
                update_player_turn_text(Screen, current_characters)
                current_char = character_mapping.get(current_characters)
                if current_char:
                    current_char.display_attribute(Screen)
            if TakeCardButton.checkForInput(MousePos):
                if isinstance(drawn_card, (ObjectCard, MagicObject, Spell)):
                    current_character.deck.append(drawn_card)
                    drawn_card = None
            if ShowDeckButton.checkForInput(MousePos):
                show_deck = not show_deck
    if show_deck:
        pass

        current_character = selected_character_objects[current_player_index]

        background_color = (0, 0, 0)

        # Define the area where the text is displayed
        text_area_rect = pygame.Rect(1200, current_screen_height - 40, 400, 40)

        Screen.fill(background_color, text_area_rect)

        # Now draw the new text as before
        font = get_font(30)
        current_section_name = get_current_section_name(current_character, Board_Section)
        section_text = font.render(f"Current Section: {current_section_name}", True, (255, 255, 255))
        Screen.blit(section_text, (1200, current_screen_height - 40))

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
