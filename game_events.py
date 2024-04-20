import pygame
import sys
import Classes
import button

pygame.init()

default_resolution = pygame.display.Info()

current_screen_width = default_resolution.current_w
current_screen_height = default_resolution.current_h

default_resolution_width = 1920
default_resolution_height = 1080

scale_factor_width = current_screen_width / default_resolution_width
scale_factor_height = current_screen_height / default_resolution_height

Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def get_font(size):
    """
        Loads and returns a pygame font object at a specified size.

        Args:
            size (int): The font size to load.

        Returns:
            pygame.font.Font: The loaded font object at the specified size.
        """
    return pygame.font.Font("Stuff/font.ttf", size)


def draw_deck_popup(screen, character_deck):
    """
    Displays a popup window that lists all cards in a character's deck on the screen.

    Args:
        screen (pygame.Surface): The display surface to draw the popup on.
        character_deck (list): A list of Card objects that the character currently holds.

    The function calculates the placement of each card image within a defined area of the screen,
    ensuring that all cards are visible and neatly arranged.
    """
    popup_bg_rect = pygame.Rect(200, 50, current_screen_width - 200, current_screen_height - 100)
    pygame.draw.rect(screen, (0, 0, 0), popup_bg_rect)

    start_x, start_y = 200, 100
    for card in character_deck:
        card_image = card.image
        screen.blit(card_image, (start_x, start_y))
        start_x += 200
        if start_x > popup_bg_rect.width - 150:
            start_x = 150
            start_y += 160


def fight(character, enemy, dice, screen):
    """
    Conducts a combat sequence between a player's character and an enemy, using dice rolls to determine the outcome.

    Args:
        character (Character): The player's character involved in the fight.
        enemy (Enemy): The enemy that the character is fighting.
        dice (Dice): A dice object used for rolling during the fight to determine attack strength.
        screen (pygame.Surface): The display surface on which the fight visuals are rendered.

    The function handles the sequence of combat, including rolling for enemy and player attacks, and determines
    the winner based on the total attack values.
    """
    fight_surface = pygame.Surface((800, 600))
    fight_surface.fill((0, 0, 0))
    fight_rect = fight_surface.get_rect(center=(current_screen_width // 2, current_screen_height // 2))

    fight_stage = "enemy_roll"
    enemy_stat = 'craft' if enemy.craft > enemy.strength else 'strength'
    enemy_stat_value = enemy.craft if enemy.craft > enemy.strength else enemy.strength
    player_stat_value = character.craft if enemy_stat == 'craft' else character.strength
    enemy_total, player_total = None, None

    display_fight_details(fight_surface, character, enemy, enemy_stat, enemy_stat_value, enemy_total, player_total,
                          fight_stage)
    screen.blit(fight_surface, fight_rect.topleft)
    pygame.display.flip()

    bg_color = (0, 0, 0)
    text_area = pygame.Rect(250, 50, 400, 200)

    while fight_stage != "done":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if fight_stage == "enemy_roll":
                    dice.roll()
                    enemy_total = int(enemy_stat_value) + dice.value
                    fight_stage = "enemy_rolled"
                    fight_surface.fill(bg_color, text_area)
                elif fight_stage == "enemy_rolled":
                    dice.roll()
                    player_total = int(player_stat_value) + dice.value
                    fight_stage = "player_rolled"
                elif fight_stage == "player_rolled":
                    fight_stage = "result"

                display_fight_details(fight_surface, character, enemy, enemy_stat, enemy_stat_value, enemy_total,
                                      player_total,
                                      fight_stage)
                screen.blit(fight_surface, fight_rect.topleft)
                pygame.display.flip()

                if fight_stage == "result":
                    if player_total > enemy_total:
                        winner = get_font(30).render("You Win", True, "#b68f40")
                    else:
                        winner = get_font(30).render("You lose", True, "#b68f40")
                        character.life -= 1
                        character.update_and_display_stats(screen)
                    fight_result(fight_surface, winner)
                    screen.blit(fight_surface, fight_rect.topleft)
                    pygame.display.flip()
                    fight_stage = "done"


def display_fight_details(surface, player, enemy, enemy_stat, enemy_stat_value, enemy_fin, player_fin, stage):
    """
    Updates the fight surface with the current details of the fight sequence. This function visualizes
    both the player's and enemy's stats and states at various stages of the fight.

    Args:
        surface (pygame.Surface): The surface on which to draw the fight details, typically a subsurface for the fight area.
        player (Character): The player's character involved in the fight.
        enemy (Enemy): The enemy character involved in the fight.
        enemy_stat (str): The primary stat being contested in the fight (either 'craft' or 'strength').
        enemy_stat_value (int): The base value of the enemy's contested stat before the dice roll.
        enemy_fin (int): The final value of the enemy's contested stat after adding the dice roll.
        player_fin (int): The final value of the player's contested stat after adding the dice roll.
        stage (str): The current stage of the fight, controlling what information is displayed ('enemy_roll', 'enemy_rolled', 'player_rolled').

    This function dynamically updates depending on the fight stage to provide feedback such as:
    - Prompts for rolling dice.
    - Showing the results of dice rolls.
    - Displaying final attack values.
    """
    player_image = pygame.image.load(player.image)
    enemy_image = pygame.image.load(enemy.image_path)

    surface.blit(player_image, (450, 100))
    surface.blit(enemy_image, (50, 100))

    font = get_font(30)
    enemy_stat_text = font.render(f"{enemy_stat.capitalize()}: {enemy_stat_value}", True, "#b68f40")
    surface.blit(enemy_stat_text, (50, 450))

    if stage == "enemy_roll":
        message1 = get_font(30).render("Press space to roll for enemy", True, "#b68f40")
        surface.blit(message1, (250, 50))
    elif stage == "enemy_rolled":
        enemy_total_stat = font.render(f"{enemy_stat.capitalize()}: {enemy_fin}", True, "#b68f40")
        surface.blit(enemy_total_stat, (50, 500))
        message2 = get_font(30).render("Press space to roll for yourself", True, "#b68f40")
        surface.blit(message2, (250, 50))
    elif stage == "player_rolled":
        player_stat_total = font.render(f"Total {enemy_stat.capitalize()}: {player_fin}", True, "#b68f40")
        surface.blit(player_stat_total, (450, 500))


def fight_result(surface, winner):
    """
        Displays the result of a fight on the given surface.

        Args:
            surface (pygame.Surface): The surface where the fight result is to be displayed.
            winner (pygame.Surface): The rendered text indicating the fight's outcome.
        """
    surface.blit(winner, (300, 200))


def Tavern_action(dice, character, screen):
    """
    Handles interactions within the Tavern game location, where the player can roll a dice to trigger various random events.
    This function dynamically updates the game state based on dice roll outcomes and displays results on the screen.

    Args:
        dice (Dice): The dice object used for determining the outcome of the Tavern interaction.
        character (Character): The player's character that is experiencing the Tavern actions.
        screen (pygame.Surface): The display surface where Tavern actions and outcomes are visualized.

    The function maintains a loop that awaits player input to roll the dice. Based on the roll, different effects
    may impact the player's character such as losing life, engaging in a fight, gaining or losing gold, teleportation,
    or other thematic actions specific to the Tavern location.
    """
    popup_active = True
    dice_result_displayed = False
    while popup_active:
        popup_bg = pygame.Rect(300, 200, 800, 600)
        pygame.draw.rect(screen, (0, 0, 0), popup_bg)
        font = get_font(30)
        options = font.render("Press space to roll a dice for action", True, "#b68f40")
        screen.blit(options, (350, 250))  # Adjust position as needed

        roll_options = {
            1: "Get drunk and lose 1 life",
            2: "Fight with a Farmer",
            3: "Gamble and lose 1 gold",
            4: "Gamble and win 1 gold",
            5: "A wizard offers teleportation(Move anywhere next round)",
            6: "Steal 3 gold"
        }
        y_offset = 350
        for roll, action in roll_options.items():
            option_text = get_font(30).render(f"{roll}: {action}", True, "#b68f40")
            screen.blit(option_text, (350, y_offset))
            y_offset += 50

        if dice_result_displayed:
            result_text = get_font(50).render(f"Dice Roll: {dice.value}", True, (255, 0, 0))
            screen.blit(result_text, (350, 300))
            pygame.display.update()
            pygame.time.delay(2000)
            handle_tavern_dice_roll(dice.value, character, screen)
            popup_active = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice.roll()
                    dice_result_displayed = True


def handle_tavern_dice_roll(dice_result, character, screen):
    """
    Processes the result of a dice roll when a character is in the Tavern location, applying the corresponding
    effects directly to the character's attributes or triggering specific game actions.

    Args:
        dice_result (int): The result of the dice roll, which determines the specific outcome or action to be applied.
        character (Character): The player's character that experiences the outcome of the dice roll.
        screen (pygame.Surface): The display surface where any resulting changes or effects are visually updated.

    The function interprets the dice roll result and applies various effects such as modifying the character's
    life or gold, or initiating a fight scenario. Each outcome is also visually updated on the provided screen.
    """
    initial_stats = (character.life, character.gold)
    rect = pygame.Rect(500, 800, 600, 600)
    my_die = Classes.Dice()

    if dice_result == 1:
        character.life -= 1
    elif dice_result == 2:
        farmer = Classes.Enemy("Farmer", "./EnemyCards/Farmer.png", "Encounter Farmer", 2, 3)
        fight(character, farmer, my_die, Screen)
    elif dice_result == 3:
        character.gold = max(0, character.gold - 1)
    elif dice_result == 4:
        character.gold += 1
    elif dice_result == 5:
        pass
    elif dice_result == 6:
        character.gold += 3

    if (character.life, character.gold) != initial_stats:
        screen.fill((0, 0, 0), rect)
        character.display_attribute(screen)
        pygame.display.update()


def Chapel_action(character, screen):
    """
    Manages interactions at the Chapel location within the game, applying different effects based on the character's
    alignment. This function simulates a character praying at the chapel and receiving various consequences.

    Args:
        character (Character): The player's character who is interacting at the Chapel location.
        screen (pygame.Surface): The display surface on which the Chapel interactions and their outcomes are visually presented.

    The function first displays a message indicating the character is praying, then waits and processes the result of this
    action based on the character's moral alignment:
    - Evil characters lose life.
    - Neutral characters experience no change.
    - Good characters have an opportunity to perform another action (not implemented in this function).

    All outcomes are visually updated on the screen, and any changes to the character's stats are displayed.
    """
    global result_text
    rect = pygame.Rect(500, 800, 600, 600)
    popup_bg = pygame.Rect(300, 200, 800, 600)
    pygame.draw.rect(screen, (0, 0, 0), popup_bg)
    font = get_font(30)
    chapel_text = font.render("You have entered the chapel and you are praying", True, "#b68f40")
    screen.blit(chapel_text, (350, 250))
    pygame.display.update()

    pygame.time.delay(5000)

    if character.alignment == "Evil":
        character.life -= 1
        result_text = get_font(40).render("You have lost one life", True, "#b68f40")
    elif character.alignment == "Neutral":
        result_text = get_font(40).render("Nothing happened", True, "#b68f40")
    elif character.alignment == "Good":
        result_text = get_font(40).render("Throw dice again", True, "#b68f40")

    screen.fill((0, 0, 0), popup_bg)
    screen.blit(result_text, (350, 300))
    pygame.display.update()

    if character.alignment == "Good":
        pass

    if character.alignment == "Evil":
        screen.fill((0, 0, 0), rect)
        character.display_attribute(screen)
        pygame.display.update()


def City_action(character, dice, screen):
    """
    Manages interactions in the City location, allowing the character to either visit the enchantress by rolling a dice
    or visiting a doctor by clicking a button. Each choice leads to different outcomes that affect the character's game state.

    Args:
        character (Character): The player's character interacting in the City.
        dice (Dice): The dice object used to determine outcomes when visiting the enchantress.
        screen (pygame.Surface): The screen where city interactions are rendered.

    This function maintains a loop that waits for user input, either a dice roll for random enchantress outcomes or
    a button press for a doctor's visit, each affecting the character's attributes or game progress differently.
    """
    popup_active = True
    dice_result_displayed = False

    while popup_active:
        MousePos = pygame.mouse.get_pos()
        popup_bg = pygame.Rect(300, 200, 1000, 600)
        pygame.draw.rect(screen, (0, 0, 0), popup_bg)
        font = get_font(30)
        city_text = font.render(
            "You have entered the city. Visit enchantress(Roll a dice) or visit a doctor(Press button)", True,
            "#b68f40")
        screen.blit(city_text, (350, 250))
        doctor_button = button.Button(image=pygame.image.load("Stuff/SmallRect.png"),
                                      pos=(967, 402),
                                      text_input="Enter", font=get_font(40), base_color="#b68f40",
                                      hovering_color="Green")
        doctor_button.changeColor(MousePos)
        doctor_button.update(screen)

        roll_options = {
            1: "Skip a turn",
            2: "Lose 1 strength",
            3: "Lose 1 craft",
            4: "Gain 2 craft",
            5: "Gain 2 strength",
            6: "Throw dice again"
        }
        y_offset = 350
        for roll, action in roll_options.items():
            option_text = get_font(30).render(f"{roll}: {action}", True, "#b68f40")
            screen.blit(option_text, (350, y_offset))
            y_offset += 50

        if dice_result_displayed:
            result_text = get_font(50).render(f"Dice Roll: {dice.value}", True, (255, 0, 0))
            screen.blit(result_text, (350, 300))
            pygame.display.update()
            pygame.time.delay(2000)
            City_dice_roll(dice.value, character, screen)
            popup_active = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice.roll()
                    dice_result_displayed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if doctor_button.checkForInput(MousePos):
                    doc_interaction(character, screen)
                    popup_active = False


def City_dice_roll(dice_result, character, screen):
    """
    Processes and applies the results of a dice roll when a character is in the City location. This function modifies the
    character's attributes based on the dice result, reflecting gains or losses in strength or craft.

    Args:
        dice_result (int): The result of the dice roll, determining the specific outcome or action to be applied.
        character (Character): The character experiencing the effects of the dice roll.
        screen (pygame.Surface): The display surface used for visually updating the character's attributes.

    Each possible dice outcome is associated with different changes to the character's attributes:
    - Dice result 1 and 6: No change occurs.
    - Dice result 2: Decreases strength by 1, not allowing it to go below zero.
    - Dice result 3: Decreases craft by 1, not allowing it to go below zero.
    - Dice result 4: Increases craft by 2.
    - Dice result 5: Increases strength by 2.

    The function updates the screen only if there is a change in the character's strength or craft.
    """
    initial_stats = (character.strength, character.craft)
    rect = pygame.Rect(500, 800, 600, 600)

    if dice_result == 1:
        pass
    elif dice_result == 2:
        character.strength -= max(0, character.strength - 1)
    elif dice_result == 3:
        character.craft = max(0, character.craft - 1)
    elif dice_result == 4:
        character.craft += 2
    elif dice_result == 5:
        character.strength += 2
    elif dice_result == 6:
        pass

    if (character.strength, character.craft) != initial_stats:
        screen.fill((0, 0, 0), rect)
        character.display_attribute(screen)
        pygame.display.update()


def doc_interaction(character, screen):
    """
    Manages the interaction with a doctor in the City location, which results in the character gaining additional life.
    This function displays a notification of the healing event and updates the character's life attribute.

    Args:
        character (Character): The character receiving medical attention and healing.
        screen (pygame.Surface): The display surface used for updating and showing the healing effect.

    This function increases the character's life by one and visually updates this change on the screen. If the
    character's life is increased, the function will update the display to reflect the new life total.
    """
    initial_stats = character.life
    rect = pygame.Rect(500, 800, 600, 600)
    doc_text = get_font(50).render("You have healed 1 life", True, "#b68f40")
    screen.blit(doc_text, (800, 600))
    character.life += 1

    if character.life != initial_stats:
        screen.fill((0, 0, 0), rect)
        character.display_attribute(screen)
        pygame.display.update()


def village_action(character, dice, screen):
    """
    Facilitates interactive gameplay in the Village location, allowing the character to roll a dice and experience
    various mystical outcomes based on the roll. This function creates a dynamic, interactive environment where
    the character's moral alignment or attributes can be altered.

    Args:
        character (Character): The character visiting the village, potentially facing significant changes.
        dice (Dice): The dice object used to determine the outcome of the visit.
        screen (pygame.Surface): The display surface on which the village interactions and their outcomes are shown.

    The function runs a loop that displays a menu with possible outcomes and waits for the player to roll the dice.
    Depending on the dice result, the character's alignment may change or their attributes such as strength or craft
    may increase. The function updates the display to show the dice result and applies the corresponding effects.
    """
    popup_active = True
    dice_result_displayed = False

    while popup_active:
        popup_bg = pygame.Rect(300, 200, 1000, 600)
        pygame.draw.rect(screen, (0, 0, 0), popup_bg)
        font = get_font(30)
        village_text = font.render(
            "You have entered the village. Visit Mystic(Roll a dice)", True,
            "#b68f40")
        screen.blit(village_text, (350, 250))

        roll_options = {
            1: "Become evil.",
            2: "Nothing",
            3: "Nothing",
            4: "Become good",
            5: "Gain 2 craft",
            6: "Gain 2 strength"
        }
        y_offset = 350
        for roll, action in roll_options.items():
            option_text = get_font(30).render(f"{roll}: {action}", True, "#b68f40")
            screen.blit(option_text, (350, y_offset))
            y_offset += 50

        if dice_result_displayed:
            result_text = get_font(50).render(f"Dice Roll: {dice.value}", True, (255, 0, 0))
            screen.blit(result_text, (350, 300))
            pygame.display.update()
            pygame.time.delay(2000)
            Village_dice_roll(dice.value, character, screen)
            popup_active = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice.roll()
                    dice_result_displayed = True


def Village_dice_roll(dice_result, character, screen):
    """
        Processes and applies the effects of a die roll when a character is in the village. Effects vary depending
        on the dice result, affecting the character's alignment, strength, or craft.

        Args:
            dice_result (int): The result of the dice roll, determining the effect to apply.
            character (Character): The character to whom the dice roll effects will be applied.
            screen (pygame.Surface): The display surface used for updating the character's attributes visually.

        This function modifies the character's attributes based on the dice roll. Possible outcomes include:
        - Becoming evil or good (alignment change).
        - Increment in craft or strength attributes.
        """
    initial_stats = (character.strength, character.craft)
    rect = pygame.Rect(500, 800, 800, 600)

    if dice_result == 1:
        character.alignment = "Evil"
    elif dice_result == 2:
        pass
    elif dice_result == 3:
        pass
    elif dice_result == 4:
        character.alignment = "Good"
    elif dice_result == 5:
        character.craft += 2
    elif dice_result == 6:
        character.strength += 2

    if (character.strength, character.craft, character.alignment) != initial_stats:
        screen.fill((0, 0, 0), rect)
        character.display_attribute(screen)
        pygame.display.update()
