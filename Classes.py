import pygame
import random
import game_events

pygame.init()

default_resolution = pygame.display.Info()

current_screen_width = default_resolution.current_w
current_screen_height = default_resolution.current_h

default_resolution_width = 1920
default_resolution_height = 1080

scale_factor_width = current_screen_width / default_resolution_width
scale_factor_height = current_screen_height / default_resolution_height


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
    def __init__(self, name, image, strength, craft, life, fate, gold, alignment, start):
        self.name = name
        self.strength = strength
        self.craft = craft
        self.life = life
        self.gold = 0
        self.alignment = alignment
        self.talisman = False
        self.fate = fate
        self.gold = gold
        self.trophy = 0
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

        attributes = ["Life = " + str(self.life),
                      "Strength = " + str(self.strength),
                      "Craft = " + str(self.craft),
                      "Fate = " + str(self.fate),
                      "Gold = " + str(self.gold),
                      "Alignment = " + str(self.alignment)]
        x_offset = 10
        font = game_events.get_font(30)

        total_width = sum(font.size(attr)[0] for attr in attributes) + x_offset * (len(attributes) - 1)

        # Calculate the starting x position to center the attributes block
        base_x = (current_screen_width - total_width) / 2  # Assuming current_screen_width is defined

        current_x = base_x
        for attribute in attributes:
            attribute_surface = font.render(attribute, True, (0, 0, 255))
            screen.blit(attribute_surface, (current_x, base_y))
            current_x += attribute_surface.get_width() + x_offset

    def update_and_display_stats(self, screen):
        rect = pygame.Rect(400, 800, 1000, 600)
        screen.fill((0, 0, 0), rect)

        base_y = (1050 * scale_factor_height) + (current_screen_height - (1080 * scale_factor_height))
        attributes = [
            f"Life = {self.life}",
            f"Strength = {self.strength}",
            f"Craft = {self.craft}",
            f"Fate = {self.fate}",
            f"Gold = {self.gold}",
            f"Alignment = {self.alignment}"
        ]
        x_offset = 10
        font = game_events.get_font(30)

        total_width = sum(font.size(attr)[0] for attr in attributes) + x_offset * (len(attributes) - 1)

        current_x = (current_screen_width - total_width) / 2
        for attribute in attributes:
            attribute_surface = font.render(attribute, True, (0, 0, 255))
            screen.blit(attribute_surface, (current_x, base_y))
            current_x += attribute_surface.get_width() + x_offset

        # Update the display only for the part that changed
        pygame.display.update(rect)

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
    def __init__(self, name, image, effect, effect_value=None):
        super().__init__(image, "Object")
        self.name = name
        self.effect = effect
        self.effect_value = effect_value

    def apply_effect(self, character, screen):
        if self.effect == "add_strength":
            character.strength += self.effect_value
        elif self.effect == "give_gold":
            character.gold += self.effect_value
            character.deck.remove(self)

        character.update_and_display_stats(screen)


class MagicObject(Card):
    def __init__(self, name, image, effect, effect_value=None):
        super().__init__(image, "MagicObject")
        self.name = name
        self.effect = effect
        self.effect_value = effect_value

    def apply_effect(self, character, screen):
        if self.effect == "add_strength":
            character.strength += self.effect_value
        elif self.effect == "give_craft":
            character.craft += self.effect_value
        elif self.effect == "give_both":
            character.strength += self.effect_value
            character.craft += self.effect_value

        character.update_and_display_stats(screen)


class Follower(Card):
    def __init__(self, name, image, effect, effect_value=None):
        super().__init__(image, "Follower")
        self.name = name
        self.effect = effect
        self.effect_value = effect_value

    def apply_effect(self, character, screen):
        if self.effect == "add_strength":
            character.strength += self.effect_value
        elif self.effect == "give_craft":
            character.craft += self.effect_value
        elif self.effect == "give_both":
            character.strength += self.effect_value
            character.craft += self.effect_value

        character.update_and_display_stats(screen)


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

