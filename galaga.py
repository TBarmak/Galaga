"""
Taylor Barmak

This program allows the user to play Galaga using the arrow keys and space bar.

Recent updates:
- Player movement
- Can be imported as a module
- Lives indicator

Next fixes:
- Enemy ships

"""
import pygame

# Global Variables
HEIGHT = 0
WIDTH = 0

class PlayerShip:
    def __init__(self):
        self.lives = 3
        self.position = [(WIDTH/2, HEIGHT*0.85), (WIDTH*0.47, HEIGHT*0.9), (WIDTH*0.53, HEIGHT*0.9)]
        self.speed = 0

    def move_speed(self):
        for i in range(len(self.position)):
            self.position[i] = (self.position[i][0] + self.speed, self.position[i][1])

    def set_speed(self, speed):
        self.speed = speed

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
    HEIGHT = infoObject.current_h * HEIGHT_MULTIPLIER
    WIDTH = HEIGHT * H_TO_W_MULTIPLIER

def draw_heart(surface, color, pos, width):
    pygame.draw.circle(surface, color, (int(pos[0] + width/4), int(pos[1] + width/4)), int(width/4))
    pygame.draw.circle(surface, color, (int(pos[0] + 3 * width/4), int(pos[1] + width/4)), int(width/4))
    pygame.draw.polygon(surface, color, [(pos[0], pos[1] + width/4), (pos[0] + width/2, pos[1] + width), (pos[0] + width, pos[1] + width/4)])

def show_lives():
    for i in range(player.lives):
        draw_heart(screen, (255, 0, 0), (0.05 * WIDTH + (30 * i), .95 * HEIGHT), 20)


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
        screen.fill((0, 200, 255))
        pygame.draw.polygon(screen, (255, 255, 255), player.position)
        show_lives()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


