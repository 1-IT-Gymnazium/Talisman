# from enum import Enum
import pygame
import random


# Make life craft strength gold values adding manual, for card and effect that affect it
# cuz I don't know ho to make it automatic
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

    def display(self, screen):
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        # screen.blit(text, (self.x + 10, self.y + 10))


class Cards:
    def __init__(self, image, types):
        self.image = image
        self.types = types


class ObjectCard(Cards):
    def __init__(self, name, image, effect):
        super().__init__(image, "Object")
        self.name = name
        self.effect = effect


class MagicObject(Cards):
    def __init__(self, name, image, effect):
        super().__init__(image, "MagicObject")
        self.name = name
        self.effect = effect


class Follower(Cards):
    def __init__(self, name, image, effect):
        super().__init__(image, "Follower")
        self.name = name
        self.effect = effect


class Stranger(Cards):
    def __init__(self, name, image, effect):
        super().__init__(image, "Stranger")
        self.name = name
        self.effect = effect


class Enemy(Cards):
    def __init__(self, name, image, effect, craft, strength):
        super().__init__(image, "Enemy")
        self.name = name
        self.effect = effect
        self.craft = craft
        self.strength = strength


class Place(Cards):
    def __init__(self, name, image, effect):
        super().__init__(image, "Place")
        self.name = name
        self.effect = effect


class Spell(Cards):
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

        for row in range(row):
            for col in range(columns):
                x = col * cell_width
                y = row * cell_height
                pygame.draw.rect(screen, (0, 0, 0),
                                 (x + screen_width / 10, y + screen_height / 10, cell_width, cell_height), 1)
        for character in characters:
            character.display(screen)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
