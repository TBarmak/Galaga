"""
Taylor Barmak

This program allows the user to play Galaga using the arrow keys and space bar.

Recent updates:
- Game main loop
- Sizing relative to the screen
- Created class for the player

Next fixes:
- Player movement
- Enemy ships

"""
import pygame

class PlayerShip:
    def __init__(self, coordinates):
        self.lives = 3
        self.position = coordinates

pygame.init()

# Get screen dimensions
infoObject = pygame.display.Info()

# Constant to size the window
HEIGHT_MULTIPLIER = 0.6
H_TO_W_MULTIPLIER = 0.8
height = infoObject.current_h * HEIGHT_MULTIPLIER
print("Height: " + str(height))
width = height * H_TO_W_MULTIPLIER
print("Width: " + str(width))
size = (int(width), int(height))
screen = pygame.display.set_mode(size) # , pygame.RESIZABLE)
pygame.display.set_caption("Galaga")

clock = pygame.time.Clock()

"""
Code start screen here
"""

# Create the player
player = PlayerShip([(width/2, height*0.9), (width*0.47, height*0.95), (width*0.53, height*0.95)])

gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False

    screen.fill((0, 200, 255))

    pygame.draw.polygon(screen, (255, 255, 255), player.position)

    pygame.display.update()

    clock.tick(60)

pygame.quit()


