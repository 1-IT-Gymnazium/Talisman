class Button:
    """
        A class to create interactive button elements for a PyGame application, supporting text rendering,
        dynamic color changes based on hover state, and interaction detection.

        Attributes:
            image (pygame.Surface): The graphical image of the button. Can be None if the button only uses text.
            x_pos (int): The x-coordinate of the button's position.
            y_pos (int): The y-coordinate of the button's position.
            font (pygame.font.Font): The font used for rendering the button's text.
            base_color (tuple): The color of the text when the button is not being hovered over.
            hovering_color (tuple): The color of the text when the button is being hovered over by the mouse.
            text_input (str): The text displayed on the button.
            char_name (str, optional): An additional attribute to store character names or other identifiers associated with the button.
            text (pygame.Surface): The rendered text surface.
            rect (pygame.Rect): The rectangular area of the button used for interaction detection.
            text_rect (pygame.Rect): The rectangular area used for positioning the text on the button.

        Methods:
            update(screen): Renders the button's image and text to the specified display surface.
            checkForInput(mouse_pos): Checks if the mouse position intersects with the button's rectangular area.
            changeColor(position): Changes the text color based on whether the mouse is over the button.
        """
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, char_name=None):
        """
           Initializes a new Button object with specified graphical properties, text, and interaction settings.

           Args:
               image (pygame.Surface or None): The graphical image to display as the button's background.
                                              If None, the button will use the rendered text as the background.
               pos (tuple): The (x, y) position tuple representing the center of the button on the screen.
               text_input (str): The text to be displayed on the button.
               font (pygame.font.Font): The font object used to render the button's text.
               base_color (str): The RGB color tuple used for the text when the button is not being hovered over.
               hovering_color (str): The RGB color tuple used for the text when the button is hovered over by the mouse.
               char_name (str, optional): An optional name or identifier associated with the button, useful for linking the button
                                          to specific character actions or choices.

           This constructor sets up the button with an optional image or text background, configures its positioning,
           and prepares text rendering based on mouse interaction states. It also defines hitboxes for interaction detection.
           """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.char_name = char_name
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
            Draws the button onto the specified PyGame display surface (screen). This includes both the background image
            and the text of the button.

            Args:
                screen (pygame.Surface): The PyGame display surface onto which the button will be drawn.

            This method is responsible for rendering the button's graphical components onto the game's display.
            It checks if there is a specific image set for the background of the button and draws it, followed by
            overlaying the button's text. If no specific image is set, it assumes the background is handled by the text rendering.

            The button's text and image are positioned according to the pre-set rectangle attributes (`self.rect` for the image
            and `self.text_rect` for the text), ensuring proper alignment and placement on the screen.
            """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, mouse_pos):
        """
            Checks if the mouse cursor is over the button's area, which is necessary for determining whether the button
            has been hovered over or clicked.

            Args:
                mouse_pos (tuple): The current mouse cursor position, typically obtained from pygame.mouse.get_pos(),
                                   containing coordinates (x, y).

            Returns:
                bool: Returns True if the mouse cursor is over the button, False otherwise.

            This method utilizes the `collidepoint` method of the pygame.Rect object associated with the button (`self.rect`).
            It evaluates whether the provided mouse position intersects with the rectangle that defines the button's area.
            This functionality is crucial for interactive GUI elements in PyGame, allowing for responsive feedback and actions
            based on user input.
            """
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def changeColor(self, position):
        """
            Updates the text color of the button depending on whether the mouse cursor is hovering over it.
            This dynamic visual feedback helps users identify interactive elements on the screen.

            Args:
                position (tuple): The current position of the mouse cursor, given as (x, y) coordinates.

            The method checks if the mouse position is within the rectangular bounds of the button. If the cursor
            is within the button's area, it changes the text color to the hovering color to indicate interactivity.
            If the cursor is outside the button's area, it reverts the text color to the base color.

            This functionality enhances user experience by providing immediate visual feedback about button interactivity,
            aiding in navigation and usability within the application.
            """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
