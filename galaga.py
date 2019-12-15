"""
Taylor Barmak

This program allows the user to play Galaga using the arrow keys and space bar.

Recent updates:
- Player can't move off screen
- Starry background

Next fixes:
- Enemy ships
- Player can't move off screen

"""
# Imports
import pygame
import random

# Global Variables
HEIGHT = 0  # Height of window
WIDTH = 0   # Width of window
star_locations = []    # List of coordinates and sizes for the stars

class PlayerShip:
    """
    Class to represent the player's ship
    Instance variables:
    lives - an int representing the number of lives remaining
    position - a list of three tuples (coordinates) where the triangular ship will go
    speed - an int representing the speed the ship is moving at
    """
    def __init__(self):
        """
        Default constructor for PlayerShip
        Initializes lives to 3, the position to be in the middle of the screen close to the bottom, and the speed to 0
        """
        self.lives = 3
        self.position = [(WIDTH*0.5, HEIGHT*0.85), (WIDTH*0.47, HEIGHT*0.9), (WIDTH*0.53, HEIGHT*0.9)]
        self.speed = 0

    def move_speed(self):
        """
        Moves the player across the screen according to their speed
        :return: None
        """
        for i in range(len(self.position)):
            self.position[i] = (self.position[i][0] + self.speed, self.position[i][1])

    def set_speed(self, speed):
        """
        Sets the player's speed to the speed entered as the argument
        :param speed: an int representing the player's speed
        :return: None
        """
        self.speed = speed

    def keep_in_bounds(self):
        """
        Keeps the player's coordinates from moving outside of the viewable window
        :return: None
        """
        # If it's too far left, move it to the farthest left allowed
        if self.position[0][0] < WIDTH*0.1:
            self.position = [(WIDTH*0.1, HEIGHT*0.85), (WIDTH*0.07, HEIGHT*0.9), (WIDTH*0.13, HEIGHT*0.9)]
        # If it's too far right, move it to the farthest right allowed
        elif self.position[0][0] > WIDTH*0.9:
            self.position = [(WIDTH * 0.9, HEIGHT * 0.85), (WIDTH * 0.87, HEIGHT * 0.9), (WIDTH * 0.93, HEIGHT * 0.9)]

def set_dimensions():
    """
    Sets the global HEIGHT and WIDTH constants which are the height and width of the window of the game.
    They are scaled relative to the screen size.
    :return: None
    """
    global HEIGHT
    global WIDTH
    # Get screen dimensions
    infoObject = pygame.display.Info()

    # Constant to size the window
    HEIGHT_MULTIPLIER = 0.6
    H_TO_W_MULTIPLIER = 0.8
    HEIGHT = int(infoObject.current_h * HEIGHT_MULTIPLIER)
    WIDTH = int(HEIGHT * H_TO_W_MULTIPLIER)

def draw_heart(surface, color, pos, width):
    """
    Method draws a heart with the provided color, position, and width
    :param surface: the surface to draw the heart on
    :param color: the color of the heart
    :param pos: a tuple of the x and y coordinates of the top left of a square containing the heart
    :param width: an int representing the width of the square containing the heart
    :return: None
    """
    # Draw two circles and a triangle to make a heart
    pygame.draw.circle(surface, color, (int(pos[0] + width/4), int(pos[1] + width/4)), int(width/4))
    pygame.draw.circle(surface, color, (int(pos[0] + 3 * width/4), int(pos[1] + width/4)), int(width/4))
    pygame.draw.polygon(surface, color, [(pos[0], pos[1] + width/4), (pos[0] + width/2, pos[1] + width),
                                         (pos[0] + width, pos[1] + width/4)])

def show_lives():
    """
    Show the number of lives a player has at the bottom left corner
    :return: None
    """
    # Draw a heart for each life
    for i in range(player.lives):
        draw_heart(screen, (255, 0, 0), (0.05 * WIDTH + (30 * i), .95 * HEIGHT), 20)

def generate_stars(number):
    """
    Creates locations and radii randomly for stars
    It produces the number of stars provided in the argument and appends them to the global star_locations variable. The
    stars are represented as a tuple with the first and second entries representing the coordinates of the center, and
    the third entry representing the radius.
    :param number: an int representing the number of stars to be generated
    :return: None
    """
    global star_locations
    for i in range(number):
        star_locations.append((random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 2)))

def draw_stars(surface):
    """
    Draw the stars on the screen according to the global star_locations varaible
    :param surface: The surface to draw the stars on
    :return: None
    """
    for star in star_locations:
        pygame.draw.circle(surface, (255, 255, 255), star[:2], star[2])



if __name__ == '__main__':
    pygame.init()

    set_dimensions()
    size = (int(WIDTH), int(HEIGHT))
    screen = pygame.display.set_mode(size) # , pygame.RESIZABLE)
    pygame.display.set_caption("Galaga")

    clock = pygame.time.Clock()

    """
    Code start screen here
    """

    # Create the player
    player = PlayerShip()

    # Generate the stars for the background
    generate_stars(300)

    gameOn = True
    while gameOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
            if event.type == pygame.KEYUP and 1 not in pygame.key.get_pressed():
                player.set_speed(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.set_speed(-5)
                if event.key == pygame.K_RIGHT:
                    player.set_speed(5)

        player.move_speed()
        player.keep_in_bounds()
        screen.fill((0, 0, 100))
        draw_stars(screen)
        pygame.draw.polygon(screen, (255, 255, 255), player.position)
        show_lives()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


