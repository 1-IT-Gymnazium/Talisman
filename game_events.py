import pygame
import sys
import time
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
    return pygame.font.Font("Stuff/font.ttf", size)


def draw_deck_popup(screen, character_deck):
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
                elif fight_stage == "enemy_rolled":
                    fight_surface.fill(bg_color, text_area)
                    fight_stage = "player_roll"
                elif fight_stage == "player_roll":
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
    elif stage == "player_roll":
        message2 = get_font(30).render("Press space to roll for yourself", True, "#b68f40")
        surface.blit(message2, (250, 50))
    elif stage == "player_rolled":
        player_stat_total = font.render(f"Total {enemy_stat.capitalize()}: {player_fin}", True, "#b68f40")
        surface.blit(player_stat_total, (450, 500))


def fight_result(surface, winner):
    surface.blit(winner, (300, 200))


def Tavern_action(dice, character, screen):
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
