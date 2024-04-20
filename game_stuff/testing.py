import pygame

# Initialize Pygame
pygame.init()

# Base resolution
default_resolution_width = 1920
default_resolution_height = 1080

# Actual screen size
screen_width = 1600
screen_height = 900

# Calculate scaling factors
scale_factor_width = screen_width / default_resolution_width
scale_factor_height = screen_height / default_resolution_height

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Get Board Coordinates')

# Load and scale the board image
board_image = pygame.image.load('./board.png')
scaled_board_image = pygame.transform.scale(board_image, (int(board_image.get_width() * scale_factor_width), int(board_image.get_height() * scale_factor_height)))

# Calculate the top left position to center the board
board_x = (screen_width - scaled_board_image.get_width()) // 2
board_y = (screen_height - scaled_board_image.get_height()) // 2

# Game loop flag
running = True

# List to hold the coordinates
board_path = []

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the left mouse button is pressed, get the mouse position
            if event.button == 1:
                pos = pygame.mouse.get_pos()

                # Adjust position to account for the centered board
                adjusted_pos = (pos[0] - board_x, pos[1] - board_y)

                # Scale the position back to base resolution coordinates
                base_pos = (int(adjusted_pos[0] / scale_factor_width), int(adjusted_pos[1] / scale_factor_height))
                board_path.append(base_pos)
                print(f"Added coordinate: {base_pos}")

    # Draw the scaled and centered board
    screen.blit(scaled_board_image, (board_x, board_y))

    pygame.display.flip()

# Print out the list of coordinates when the game loop ends
print("Final board path:")
for pos in board_path:
    print(pos)

# Quit Pygame
pygame.quit()
