from enum import Enum
import pygame
import random


class Character:
    def __init__(self, name, strength, craft, life, x, y):
        self.name = name
        self.strength = strength
        self.craft = craft
        self.life = life
        self.gold = 0
        self.talisman = False
        self.x = x
        self.y = y

    def display(self, screen):
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (self.x + 10, self.y + 10))


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
        Character("Warrior", 4, 3, 4, 1000, 1000)
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


