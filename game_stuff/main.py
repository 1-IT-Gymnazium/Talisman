# from enum import Enum
import random

import pygame
import sys
from button import Button
import game_events
import Cards
import Classes

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


def Game(selected_characetrs):
    """
    Runs the main game loop, handling all game logic, player actions, and rendering updates for the game.

    Args:
        selected_characters (list of list): Nested list of character names selected by each player, used to initiate character states.

    This function sets up the game environment, initializes game objects, and enters a loop that continuously checks for and responds to events such as player movements, actions, and system commands.
    """
    pygame.display.set_caption("Game")
    Screen.fill("black")
    global BoardSection, current_player_index, event, drawn_card, current_section
    last_button_press_time = 0
    button_cooldown = 500

    def load_and_scale_image(image, scale_x, scale_y):
        """
                Loads an image, scales it according to the given factors, and returns the scaled image.

                Args:
                    image (str): Path to the image file.
                    scale_x (float): Factor to scale the image width.
                    scale_y (float): Factor to scale the image height.

                Returns:
                    pygame.Surface: Scaled image.
                """
        image = pygame.image.load(image)
        image_width = image.get_width() * scale_x
        image_height = image.get_height() * scale_y
        scaled_image = pygame.transform.scale(image, (int(image_width), int(image_height)))
        return scaled_image

    game_board = load_and_scale_image("./board.png", scale_factor_width, scale_factor_height)

    def handle_movement(event, characters, current_player_index, board_sections, screen, game_board):
        """
                Processes player movement based on key inputs and updates the game board accordingly.

                Args:
                    event (pygame.Event): Event object capturing the keyboard input.
                    characters (list): List of character objects participating in the game.
                    current_player_index (int): Index of the current player controlling the turn.
                    board_sections (list): List of all game board sections.
                    screen (pygame.Surface): Main display surface where the game is rendered.
                    game_board (pygame.Surface): Surface representing the game board.
                """
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
            screen.blit(game_board, (190, 80))
            for character in characters:
                character.display(screen, game_events.get_font(40))

    def display_current_state(screen, game_board, characters, current_player_index):
        """
                Displays the current state of the game board, including character positions and any relevant game info.

                Args:
                    screen (pygame.Surface): Main display surface where the game is rendered.
                    game_board (pygame.Surface): Surface representing the game board.
                    characters (list): List of character objects participating in the game.
                    current_player_index (int): Index of the current player controlling the turn.
                """
        screen.blit(game_board, (190, 80))
        for character in characters:
            character.display(screen, game_events.get_font(40))

    def get_current_section_name(character, board_sections):
        """
                Retrieves the name of the current board section where the character is located.

                Args:
                    character (Character): The character whose position is being queried.
                    board_sections (list): List of all game board sections.

                Returns:
                    str: Name of the current section.
                """
        return board_sections[character.position_index].section

    def update_player_turn_text(screen, current_player_name):
        """
                Updates the display to show which player's turn it is.

                Args:
                    screen (pygame.Surface): Main display surface where the game is rendered.
                    current_player_name (str): Name of the player whose turn is current.
                """
        background_color = (0, 0, 0)
        clear_rect = pygame.Rect(screen.get_width() // 2 - 200, 20 - 35, 400, 70)  # Adjust the size as needed
        screen.fill(background_color, clear_rect)

        player_turn_text = game_events.get_font(70).render(f"{current_player_name}'s Turn", True, "#b68f40")
        player_turn_rect = player_turn_text.get_rect(center=(screen.get_width() // 2, 25))
        screen.blit(player_turn_text, player_turn_rect)

    Board_Section = [
        # List of board sections, initializing BoardSection objects from Classes module.
        Classes.BoardSection(395, 135, "Village", down=23, right=1),  # 0
        Classes.BoardSection(579, 135, "Forest", left=0, right=2),  # 1
        Classes.BoardSection(770, 135, "Graveyard", left=1, right=3),  # 2
        Classes.BoardSection(956, 135, "Forest", left=2, right=4),  # 3
        Classes.BoardSection(1158, 135, "Sentinel", left=3, right=5),  # 4
        Classes.BoardSection(1351, 135, "Forest", left=4, right=6),  # 5
        Classes.BoardSection(1595, 135, "Chapel", left=5, down=7),  # 6
        Classes.BoardSection(1595, 249, "Forest", down=8, up=6),  # 7
        Classes.BoardSection(1595, 377, "Cracks", down=9, up=7),  # 8
        Classes.BoardSection(1595, 508, "Forest", down=10, up=8),  # 9
        Classes.BoardSection(1595, 632, "Forest", down=11, up=9),  # 10
        Classes.BoardSection(1595, 753, "Forest", down=12, up=10),  # 11
        Classes.BoardSection(1595, 900, "City", left=13, up=11),  # 12
        Classes.BoardSection(1395, 900, "Forest", left=14, right=12),  # 13
        Classes.BoardSection(1190, 900, "Forest", left=15, right=13),  # 14
        Classes.BoardSection(980, 900, "Forest", left=16, right=14),  # 15
        Classes.BoardSection(800, 900, "ElvForest", left=17, right=15),  # 16
        Classes.BoardSection(630, 900, "Forest", left=18, right=16),  # 17
        Classes.BoardSection(450, 900, "Tavern", up=19, right=17),  # 18
        Classes.BoardSection(365, 757, "Forest", up=20, down=18),  # 19
        Classes.BoardSection(365, 628, "Ruins", up=21, down=19),  # 20
        Classes.BoardSection(365, 469, "Forest", up=22, down=20),  # 21
        Classes.BoardSection(365, 357, "Forest", up=23, down=21),  # 22
        Classes.BoardSection(365, 267, "Forest", up=0, down=22)  # 23
    ]

    deck = [Cards.enemycards, Cards.followercards, Cards.magicobjectcards, Cards.objectcards, Cards.placecards,
            Cards.spellcards, Cards.strangercards]
    deck_shuffler = Classes.DeckShuffle(deck)
    deck_shuffler.shuffle()
    deck_shuffler.display(Screen)

    my_die = Classes.Dice()

    Screen.blit(game_board, (190, 80))

    # Create a mapping of character names to their Character objects
    character_mapping = {character.name: character for character in Cards.characters}

    font = game_events.get_font(40)

    selected_character_objects = []
    for player_characters in selected_characters:
        for character_name in player_characters:
            # Retrieve the character object from the mapping using its name.
            character = character_mapping.get(character_name)
            if character:
                # Locate the starting section of the board that matches the character's start location.
                matching_section = next((index for index, section in enumerate(Board_Section) if
                                         section.section.lower() == character.start.lower()), None)
                if matching_section is not None:
                    # If a matching section is found, set the character's position index.
                    character.position_index = matching_section
                    # Set the actual position coordinates of the character on the game screen, accounting for scale factors.
                    character.set_position(Board_Section[matching_section].x, Board_Section[matching_section].y,
                                           scale_factor_width, scale_factor_height)
                    # Add the character to the list of selected characters in the game.
                    selected_character_objects.append(character)
                    # Display the character on the game screen using the predefined font.
                    character.display(Screen, font)

    run = True
    show_deck = False
    Sentinel = Classes.Enemy("Sentinel", "./EnemyCards/Sentinel.png", "yep", 0, 15)

    current_player_index = 0
    current_characters = selected_characters[current_player_index][0]
    update_player_turn_text(Screen, current_characters)
    current_char = character_mapping.get(current_characters)
    if current_char:
        current_char.display_attribute(Screen)

    while run:
        # Main game loop, processing events, updating game state, and rendering.

        MousePos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        current_character = selected_character_objects[current_player_index]

        EndTurnButton = Button(image=pygame.image.load("Stuff/SmallRect.png"),
                               pos=(1800 * scale_factor_width, 100 * scale_factor_height),
                               text_input="End Turn", font=game_events.get_font(40), base_color="#b68f40",
                               hovering_color="Blue")
        EndTurnButton.changeColor(MousePos)
        EndTurnButton.update(Screen)

        TakeCardButton = Button(image=pygame.image.load("Stuff/SmallRect.png"),
                                pos=(110 * scale_factor_width, 1000 * scale_factor_height),
                                text_input="Take Card", font=game_events.get_font(40), base_color="#b68f40",
                                hovering_color="Blue")
        TakeCardButton.changeColor(MousePos)
        TakeCardButton.update(Screen)

        ShowDeckButton = Button(image=pygame.image.load("Stuff/SmallRect.png"),
                                pos=(1800 * scale_factor_width, 150 * scale_factor_height),
                                text_input="Show Deck", font=game_events.get_font(40), base_color="#b68f40",
                                hovering_color="Blue")
        ShowDeckButton.changeColor(MousePos)
        ShowDeckButton.update(Screen)

        enter_button = Button(image=pygame.image.load("Stuff/SmallRect.png"),
                              pos=(1700 * scale_factor_width, 950 * scale_factor_height),
                              text_input="Enter", font=game_events.get_font(40), base_color="#b68f40",
                              hovering_color="Blue")

        Fight_button = Button(image=pygame.image.load("Stuff/SmallRect.png"),
                              pos=(1700 * scale_factor_width, 950 * scale_factor_height),
                              text_input="Fight", font=game_events.get_font(40), base_color="#b68f40",
                              hovering_color="Blue")

        rect_height = 70
        rect_y_start = current_screen_height - rect_height
        attributes_display_area = pygame.Rect(0, rect_y_start, current_screen_width, rect_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                handle_movement(event, selected_character_objects, current_player_index, Board_Section, Screen,
                                game_board)

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
                        check_enemy = isinstance(drawn_card, Classes.Enemy)
                        if check_enemy:
                            game_events.fight(current_char, drawn_card, my_die, Screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if enter_button.checkForInput(MousePos) and current_section == "Tavern":
                    game_events.Tavern_action(my_die, current_char, Screen)
                elif enter_button.checkForInput(MousePos) and current_section == "Chapel":
                    game_events.Chapel_action(current_char, Screen)
                elif enter_button.checkForInput(MousePos) and current_section == "City":
                    game_events.City_action(current_char, my_die, Screen)
                elif enter_button.checkForInput(MousePos) and current_section == "Village":
                    game_events.village_action(current_char, my_die, Screen)
                if Fight_button.checkForInput(MousePos) and current_section == "Sentinel":
                    game_events.fight(current_char, Sentinel, my_die, Screen)
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
                    if isinstance(drawn_card, (Classes.ObjectCard, Classes.MagicObject, Classes.Spell, Classes.Follower)):
                        current_character.deck.append(drawn_card)
                        if isinstance(drawn_card, (Classes.ObjectCard, Classes.MagicObject, Classes.Follower)):
                            drawn_card.apply_effect(current_character, Screen)
                        drawn_card = None
                if ShowDeckButton.checkForInput(MousePos):
                    game_events.draw_deck_popup(Screen, current_character.deck)

        current_garacter = selected_character_objects[current_player_index]

        background_color = (0, 0, 0)

        # Define the area where the text is displayed
        text_area_rect = pygame.Rect(1200, current_screen_height - 40, 400, 40)

        Screen.fill(background_color, text_area_rect)

        # Now draw the new text as before
        font = game_events.get_font(30)
        current_section_name = get_current_section_name(current_garacter, Board_Section)
        section_text = font.render(f"Current Section: {current_section_name}", True, (255, 255, 255))
        Screen.blit(section_text, (1200, current_screen_height - 40))

        current_section = Board_Section[current_character.position_index].section
        if current_section in ["Tavern", "Village", "Chapel", "City"]:
            enter_button.changeColor(MousePos)
            enter_button.update(Screen)
        elif current_section in "Sentinel":
            Fight_button.changeColor(MousePos)
            Fight_button.update(Screen)
        pygame.display.update()

    pygame.quit()


def CharSelection(num_players):
    """
    Displays and manages the character selection screen for the specified number of players. Each player chooses their characters from a given set.

    Args:
        num_players (int): The number of players participating in the game, determining how many selections are made.

    This function initializes a selection interface where players can view and select characters based on visual representations and text descriptions. The selections are captured, stored, and used to initialize the game state with the chosen characters.
    """
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

        CharText = game_events.get_font(75).render(f"Player {current_player} Character Selection", True, "#b68f40")
        CharRect = CharText.get_rect(center=(current_screen_width // 2, int(100 * scale_factor_height)))
        Screen.blit(CharText, CharRect)

        character_buttons = []

        for i, character in enumerate(Cards.characters):
            x_offset = (i % 5) * 200
            y_offset = (i // 5) * 200 + (i // 5) * 75
            button = Button(image=pygame.image.load("Stuff/Brick.png"), pos=(400 + x_offset, 300 + y_offset),
                            text_input=character.name, font=game_events.get_font(25), base_color="#b68f40",
                            hovering_color="Blue", char_name=character.name)
            character_buttons.append(button)

        for button in character_buttons:
            button.update(Screen)

        for i, image in enumerate(character_images):
            x_offset = (i % 5) * 200
            y_offset = (i // 5) * 200 + (i // 5) * 75 - 20
            Screen.blit(image, (325 + x_offset, 200 + y_offset))

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
    """
    Displays and manages the player number selection screen of the game. This function allows users to choose how many players will participate in the game.

    It provides a user interface where players can select between different options (e.g., 2 Players, 3 Players, 4 Players) to determine the number of participants. Upon selecting a player count, the function transitions to character selection for the specified number of players.
    """
    pygame.display.set_caption("Player_Selection")
    while True:
        CharMousePos = pygame.mouse.get_pos()

        Screen.fill("black")

        CharText = game_events.get_font(75).render("Player Selection", True, "#b68f40")
        CharRect = CharText.get_rect(center=(Screen.get_width() // 2, 200))

        TwoPlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 400),
                                  text_input="2 Players", font=game_events.get_font(50), base_color="#b68f40",
                                  hovering_color="Blue")
        ThreePlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 600),
                                    text_input="3 Players", font=game_events.get_font(50), base_color="#b68f40",
                                    hovering_color="Blue")
        FourPlayersButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 800),
                                   text_input="4 Players", font=game_events.get_font(50), base_color="#b68f40",
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
    """
    Displays and manages the main menu interface of the game. This function handles user interactions for starting the game or quitting.

    The main menu provides the player with the options to either start playing by entering into player selection or to exit the game. The function maintains a loop that continuously checks for user input and updates the display accordingly.
    """
    pygame.display.set_caption("Menu")
    original_wtf_image = pygame.image.load("wtf.png")
    # Scale the image to match the screen dimensions
    scaled_wtf_image = pygame.transform.scale(original_wtf_image, (current_screen_width, current_screen_height))

    while True:
        Screen.blit(scaled_wtf_image, (0, 0))

        MenuMousePos = pygame.mouse.get_pos()

        MenuText = game_events.get_font(100).render("Main Menu", True, "#b68f40")
        MenuRect = MenuText.get_rect(center=(Screen.get_width() // 2, 200))

        PlayButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 450),
                            text_input="PLAY", font=game_events.get_font(75), base_color="#b68f40",
                            hovering_color="Blue")
        QuitButton = Button(image=pygame.image.load("Stuff/Rect.png"), pos=(Screen.get_width() // 2, 750),
                            text_input="QUIT", font=game_events.get_font(75), base_color="#b68f40",
                            hovering_color="Blue")

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
