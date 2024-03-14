import pygame

# Initialize Pygame
pygame.init()

# Load your board image
screen = pygame.display.set_mode((1600, 900))
board_image = pygame.image.load('./board.png')


# Create a screen with the size of your board
pygame.display.set_caption('Get Board Coordinates')

# Game loop flag
running = True

# List to hold the coordinates
board_path = []
screen.blit(board_image,(0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the left mouse button is pressed, get the mouse position and add it to the list
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                board_path.append(pos)
                print(f"Added coordinate: {pos}")

    # Draw the board
    screen.blit(board_image, (0, 0))
    pygame.display.flip()

# Print out the list of coordinates when the game loop ends
print("Final board path:")
for pos in board_path:
    print(pos)

# Quit Pygame
pygame.quit()
