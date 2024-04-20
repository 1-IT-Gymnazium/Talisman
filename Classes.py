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
    """
        Manages a deck of cards, allowing shuffling and display of the deck's backside image on a specified screen.

        Attributes:
            deck (list): A list of card objects to be shuffled and managed.
            cards (list): A duplicate list for operations, currently unused.
            screen (pygame.Surface): The screen where the deck image will be displayed.
            image (pygame.Surface): The image of the deck's backside, loaded during display.
        """
    def __init__(self, deck):
        """
                Initializes the DeckShuffle class with a deck of cards.

                Args:
                    deck (list): A list of card objects.
                """
        self.cards = []
        self.deck = deck
        self.screen = None
        self.image = None

    def shuffle(self):
        """Shuffles the deck randomly."""
        random.shuffle(self.deck)

    def display(self, screen):
        """
                Displays the backside of the deck on the provided screen.

                Args:
                    screen (pygame.Surface): The screen where the deck image will be displayed.
                """
        self.screen = screen
        self.image = pygame.image.load("backside.png")
        screen.blit(self.image, (0, 200))


class Character:
    """
        Represents a character in the game with various attributes and the ability to move on the game board.

        Attributes:
            name (str): The name of the character.
            image (str): Path to the character's image file.
            strength (int): The character's strength attribute.
            craft (int): The character's craft attribute.
            life (int): The character's life points.
            gold (int): The amount of gold the character possesses.
            alignment (str): The character's alignment (e.g., good, evil, neutral).
            talisman (bool): Flag to indicate if the character has a talisman.
            fate (int): The character's fate points.
            trophy (int): The character's trophy points.
            start (str): The starting section name on the board for the character.
            position (tuple): The current position (x, y) on the screen.
            position_index (int): The current index of the board section where the character is.
            section_name (str): The name of the current board section.
            deck (list): A list of cards the character holds.
        """
    def __init__(self, name, image, strength, craft, life, fate, gold, alignment, start):
        """
                Initializes a character with specified attributes.

                Args:
                    name (str): The name of the character.
                    image (str): Path to the character's image file.
                    strength (int): Initial strength.
                    craft (int): Initial craft.
                    life (int): Initial life points.
                    fate (int): Initial fate points.
                    gold (int): Initial amount of gold.
                    alignment (str): Alignment, e.g., 'good', 'evil', 'neutral'.
                    start (str): The starting section on the game board.
                """
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
        """
                Moves the character in a specified direction on the board.

                Args:
                    direction (str): The direction to move ('up', 'down', 'left', 'right').
                    board_sections (list): A list of BoardSection objects representing the game board.
                """
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
        """
                Sets the character's position on the screen, scaled by the given factors.

                Args:
                    x (int): The x-coordinate of the character's position.
                    y (int): The y-coordinate of the character's position.
                    scale_x (float): Horizontal scaling factor.
                    scale_y (float): Vertical scaling factor.
                """
        self.position = (int(x * scale_x), int(y * scale_y))

    def display(self, screen, font):
        """
                Displays the character's name at their current position on the screen.

                Args:
                    screen (pygame.Surface): The screen to draw on.
                    font (pygame.font.Font): The font used to render the character's name.
                """
        name_surface = font.render(self.name, True, (0, 0, 255))
        text_position = self.position
        screen.blit(name_surface, text_position)

    def display_attribute(self, screen):
        """
                Displays the character's attributes (life, strength, etc.) on the screen.

                Args:
                    screen (pygame.Surface): The screen to display attributes on.
                """
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
    """
        Represents a basic card in the game with an image and type.

        Attributes:
            screen (pygame.Surface): The screen where the card will be displayed.
            image_path (str): The file path of the card's image.
            types (str): The type of card, e.g., 'Object', 'MagicObject', etc.
            image (pygame.Surface): The loaded image of the card.
        """
    def __init__(self, image, types):
        """
                Initializes the Card with its image and type.

                Args:
                    image (str): The path to the image file for the card.
                    types (str): The type of card.
                """
        self.screen = None
        self.image_path = image
        self.types = types
        self.image = pygame.image.load(image)

    def display(self, screen):
        """
                Displays the card on the provided screen.

                Args:
                    screen (pygame.Surface): The screen where the card will be displayed.
                """
        self.screen = screen
        screen.blit(self.image, (0, 500))


class ObjectCard(Card):
    """
       Represents an Object card, a specific type of card with an effect that can be applied to characters.

       Attributes:
           name (str): The name of the card.
           effect (str): The effect description, e.g., 'add_strength'.
           effect_value (int, optional): The value by which the effect alters the character's attribute.
       """
    def __init__(self, name, image, effect, effect_value=None):
        """
                Initializes an Object card with name, image, effect, and effect value.

                Args:
                    name (str): The name of the card.
                    image (str): The path to the card's image file.
                    effect (str): The description of the card's effect.
                    effect_value (int, optional): The numerical value of the effect.
                """
        super().__init__(image, "Object")
        self.name = name
        self.effect = effect
        self.effect_value = effect_value

    def apply_effect(self, character, screen):
        """
                Applies the card's effect to a character.

                Args:
                    character (Character): The character to which the effect is applied.
                    screen (pygame.Surface): The screen where updates are to be displayed.
                """
        if self.effect == "add_strength":
            character.strength += self.effect_value
        elif self.effect == "give_gold":
            character.gold += self.effect_value
            character.deck.remove(self)

        character.update_and_display_stats(screen)


class MagicObject(Card):
    """
        Represents a Magic Object card with special effects that can influence a character's attributes.

        Attributes:
            name (str): The name of the magic object card.
            effect (str): A description of the effect, e.g., 'give_craft'.
            effect_value (int, optional): The amount by which the effect modifies the character's attributes.
        """
    def __init__(self, name, image, effect, effect_value=None):
        """
                Initializes a Magic Object card.

                Args:
                    name (str): The name of the magic object.
                    image (str): The path to the card's image file.
                    effect (str): The effect that the card has on characters.
                    effect_value (int, optional): The value associated with the effect.
                """
        super().__init__(image, "MagicObject")
        self.name = name
        self.effect = effect
        self.effect_value = effect_value

    def apply_effect(self, character, screen):
        """
                Applies the effect of the magic object to a character.

                Args:
                    character (Character): The character affected by the magic object.
                    screen (pygame.Surface): The screen for displaying updates.
                """
        if self.effect == "add_strength":
            character.strength += self.effect_value
        elif self.effect == "give_craft":
            character.craft += self.effect_value
        elif self.effect == "give_both":
            character.strength += self.effect_value
            character.craft += self.effect_value

        character.update_and_display_stats(screen)


class Follower(Card):
    """
        Represents a Follower card that can attach to a character and modify their attributes.

        Attributes:
            name (str): The name of the follower.
            effect (str): A description of what the follower does, e.g., 'add_strength'.
            effect_value (int, optional): The numerical value associated with the effect.
        """
    def __init__(self, name, image, effect, effect_value=None):
        """
               Initializes a Follower card with a specific effect on a character.

               Args:
                   name (str): The name of the follower.
                   image (str): The image path for the follower card.
                   effect (str): The effect description.
                   effect_value (int, optional): The value of the effect, if applicable.
               """
        super().__init__(image, "Follower")
        self.name = name
        self.effect = effect
        self.effect_value = effect_value

    def apply_effect(self, character, screen):
        """
                Applies the effect of the follower to the character.

                Args:
                    character (Character): The character to apply the effect to.
                    screen (pygame.Surface): The screen where updates are displayed.
                """
        if self.effect == "add_strength":
            character.strength += self.effect_value
        elif self.effect == "give_craft":
            character.craft += self.effect_value
        elif self.effect == "give_both":
            character.strength += self.effect_value
            character.craft += self.effect_value

        character.update_and_display_stats(screen)


class Stranger(Card):
    """
       Represents a Stranger card, which typically triggers a one-time or unique effect when encountered.

       Attributes:
           name (str): The name of the stranger.
           effect (str): A description of the effect this stranger has in the game.
       """
    def __init__(self, name, image, effect):
        """
                Initializes a Stranger card with a specific game effect.

                Args:
                    name (str): The name of the stranger.
                    image (str): The image path for the card.
                    effect (str): The narrative or mechanical effect the stranger has when encountered.
                """

        super().__init__(image, "Stranger")
        self.name = name
        self.effect = effect


class Enemy(Card):
    """
        Represents an Enemy card that characters can encounter and must overcome using strength or craft.

        Attributes:
            name (str): The name of the enemy.
            effect (str): The specific effect or interaction this enemy has.
            craft (int): The craft value of the enemy, used in challenges.
            strength (int): The strength value of the enemy, used in battles.
        """
    def __init__(self, name, image, effect, craft, strength):
        """
                Initializes an Enemy card with strength and craft attributes for battles.

                Args:
                    name (str): The name of the enemy.
                    image (str): The image path for the card.
                    effect (str): The effect the enemy has when encountered.
                    craft (int): The craft attribute of the enemy.
                    strength (int): The strength attribute of the enemy.
                """
        super().__init__(image, "Enemy")
        self.name = name
        self.effect = effect
        self.craft = craft
        self.strength = strength


class Place(Card):
    """
        Represents a Place card, which provides a location-based effect or interaction in the game.

        Attributes:
            name (str): The name of the place.
            effect (str): A description of the interaction or effect provided by this place.
        """
    def __init__(self, name, image, effect):
        super().__init__(image, "Place")
        self.name = name
        self.effect = effect


class Spell(Card):
    """
        Represents a Spell card that can be used by characters for various effects, typically during their turn or in response to events.

        Attributes:
            name (str): The name of the spell.
            effect (str): A description of what the spell does when cast.
        """
    def __init__(self, name, image, effect):
        """
                Initializes a Spell card with a specific magical effect.

                Args:
                    name (str): The name of the spell.
                    image (str): The image path for the card.
                    effect (str): The specific effect or action of the spell.
                """
        super().__init__(image, "Spell")
        self.name = name
        self.effect = effect


class Dice:
    """
        Represents a die used in the game to determine random outcomes, equipped with multiple sides and images for each side.

        Attributes:
            sides (int): Number of sides on the dice.
            width (int): The width of the dice image.
            height (int): The height of the dice image.
            images (list): List of images, one for each side of the dice.
        """

    def __init__(self, sides=6, width=190, height=190):
        """
                Initializes the dice with a specified number of sides and dimensions for the images.

                Args:
                    sides (int, optional): The number of sides on the dice. Defaults to 6.
                    width (int, optional): The width of each side's image. Defaults to 190.
                    height (int, optional): The height of each side's image. Defaults to 190.
                """
        self.screen = None
        self.sides = sides
        self.value = 1
        self.images = [pygame.image.load(f'die{i}.png') for i in range(1, sides + 1)]
        self.width = width
        self.height = height

    def roll(self):
        """
                Rolls the dice to generate a random value between 1 and the number of sides.
                """
        self.value = random.randint(1, self.sides)

    def display(self, screen):
        """
                Displays the current side of the dice based on the last roll.

                Args:
                    screen (pygame.Surface): The screen where the dice will be displayed.
                """
        self.screen = screen
        image = self.images[self.value - 1]
        screen.blit(image, (0, 0))


class BoardSection:
    """
        Represents a section of the game board with specific coordinates and potential connections to other sections.

        Attributes:
            x (int): The x-coordinate of the board section.
            y (int): The y-coordinate of the board section.
            section (str): The name of the board section.
            up_neighbor_index (int, optional): Index of the neighboring section above this one.
            down_neighbor_index (int, optional): Index of the neighboring section below this one.
            left_neighbor_index (int, optional): Index of the neighboring section to the left of this one.
            right_neighbor_index (int, optional): Index of the neighboring section to the right of this one.
        """
    def __init__(self, x, y, section, up=None, down=None, left=None, right=None):
        """
                Initializes a BoardSection with coordinates, a name, and neighbor connections.

                Args:
                    x (int): The x-coordinate of the section.
                    y (int): The y-coordinate of the section.
                    section (str): The name or type of the board section.
                    up (int, optional): Index of the upper neighboring section.
                    down (int, optional): Index of the lower neighboring section.
                    left (int, optional): Index of the left neighboring section.
                    right (int, optional): Index of the right neighboring section.
                """
        self.x = x
        self.y = y
        self.section = section
        self.up_neighbor_index = up
        self.down_neighbor_index = down
        self.left_neighbor_index = left
        self.right_neighbor_index = right

