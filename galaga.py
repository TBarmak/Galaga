"""
Taylor Barmak

This program allows the user to play Galaga using the arrow keys and space bar.

Recent updates:
- Add losing screen
- Add screen in between levels
- More levels that get more difficult as you continue
- Fixed bug where one ship could take away all of your lives

Next fixes:
- Do a dance after eliminating all the enemies
- Change color of ship when it gets hit
"""
# Imports
import pygame
import random
import math

# Global Variables
HEIGHT = 0  # Height of window
WIDTH = 0   # Width of window
FLEET_SWAY_SPEED = 0.2   # Constant to determine the sway speed of the enemy ships
SWAY_DIRECTION = True   # bool used to tell if the fleet is swaying left or right
star_locations = []    # List of coordinates and sizes for the stars
enemy_ships = []  # List of enemy ship objects
dropping_ships = []    # List of enemy ships that are falling
resetting_ships = []    # List of enemy ships that are putting themselves back into their original position
moves = 75  # Variable to keep track of if it's time for the ships to change direction
score = 0   # Variable to keep track of the player's score
level = 1  # Variable to keep track of what level the player is on

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
        self.shipHits = [] # List of the ships that have hit the player so that collisions aren't counted twice
        self.position = [(WIDTH*0.5, HEIGHT*0.85), (WIDTH*0.47, HEIGHT*0.9), (WIDTH*0.53, HEIGHT*0.9)]
        self.speed = 0
        self.missiles = []

    def get_position(self):
        """
        Method returns a list of the coordinates that make up the ship
        :return: a list of tuples containing the coordinates of each vertex of the ship
        """
        return self.position

    def draw_player(self, surface):
        """
        Draws the player on the screen
        :param surface: the surface onto which the player will be drawn
        :return: None
        """
        pygame.draw.polygon(surface, (255, 255, 255), player.position)

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

    def shoot(self):
        """
        Method shoots a missile by appending a missile's coordinates to the list of missiles
        :return: None
        """
        self.missiles.append(self.position[0])

    def get_missiles(self):
        """
        Returns the list of missile coordinates
        :return: a list of missile coordinates
        """
        return self.missiles

    def move_missiles(self):
        """
        Method moves the missiles up the screen
        :return: None
        """
        for i in range(len(self.missiles)):
            self.missiles[i] = (self.missiles[i][0], self.missiles[i][1] - 7)

    def remove_missiles(self):
        """
        Method removes missiles from the list of missiles if they have left the screen.
        :return: None
        """
        for missile in self.missiles:
            if missile[1] < 0:
                self.missiles.remove(missile)

    def explode_missile(self, missile):
        """
        Method used to remove a missile when it hits a ship
        :param missile: a tuple representing the coordinates of the missile to be removed
        :return: None
        """
        try:
            self.missiles.remove(missile)
        except:
            pass

    def draw_missiles(self, surface):
        """
        Method draws the missiles on the screen
        :param surface: the surface to draw the missiles on
        :return: None
        """
        for missile in self.missiles:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(missile[0], missile[1], 2, 8))

    def show_lives(self, surface):
        """
        Show the number of lives a player has at the bottom left corner
        :return: None
        """
        # Draw a heart for each life
        for i in range(self.lives):
            draw_heart(surface, (255, 0, 0), (0.05 * WIDTH + (30 * i), .95 * HEIGHT), 20)

    def dec_lives(self, ship):
        """
        Method decrements the number of lives by 1
        :return: None
        """
        if ship not in self.shipHits:
            self.shipHits.append(ship)
        self.lives = 3 - len(self.shipHits)

    def get_lives(self):
        """
        Method returns the number of lives the player has
        :return: an int representing the number of lives remaining
        """
        return self.lives

class enemyShip:
    """
    Class to represent an enemy ship
    Instance variables:
    position - a tuple with the x and y coordinates of the ship
    xspeed - the horizontal velocity of the ship
    yspeed - the vertical velocity of the ship
    """
    def __init__(self, position, val):
        """
        One argument constructor for the enemy ship class
        Initializes the position to the argument provided, xspeed to 2, yspeed to 0, and width to 5.
        :param position: a tuple representing the x and y coordinates of the ship
        :param val: the value of the ship (how many points are received for destroying it)
        """
        self.position = position
        self.init_position = position
        self.xspeed = FLEET_SWAY_SPEED
        self.yspeed = 0
        self.width = 15
        self.value = val

    def get_init_pos(self):
        """
        Method returns the initial position of the enemy ship
        :return: a tuple containing the coordinates of the position where the ship started
        """
        return self.init_position

    def draw_ship(self, surface):
        """
        Method draws the enemy ship as a square onto the surface provided
        :param surface: the surface to draw the ship onto
        :return: None
        """
        pygame.draw.rect(surface, (255, 153, 51), pygame.Rect(self.position[0], self.position[1], self.width, self.width))

    def change_direction(self):
        """
        Method reverses the horizontal speed of the enemy ship
        :return: None
        """
        if SWAY_DIRECTION == True:
            self.xspeed = FLEET_SWAY_SPEED
        else:
            self.xspeed = -FLEET_SWAY_SPEED

    def move_speed(self):
        """
        Method moves enemy ships postion based on its xspeed and yspeed
        :return: None
        """
        self.position = (self.position[0] + self.xspeed, self.position[1] + self.yspeed)

    def get_position(self):
        """
        Method returns the position of the ship
        :return: a tuple representing the position of the ship
        """
        return self.position

    def set_position(self, position):
        """
        Method sets the position of the ship to the argument provided
        :param position: a tuple containing the x and y coordinates of the ship
        :return: None
        """
        self.position = position

    def get_width(self):
        """
        Method returns the width of the ship
        :return: an int representing the width of the ship
        """
        return self.width
    def get_value(self):
        """
        Method returns the value of the ship
        :return: an int representing the value of the ship
        """
        return self.value

    def drop(self):
        """
        Method makes an enemy start dropping towards the player
        :return: None
        """
        self.yspeed = 2

    def pursue(self, player):
        """
        Method causes the ship to adjust its velocity to pursue the player
        :param player: the playerShip to pursue
        :return: None
        """
        pPos = player.get_position()[1]
        ePos = self.position
        slope = (pPos[1] - ePos[1]) / (pPos[0] - ePos[0])
        x_speed = 2 / slope
        if x_speed > 2:
            x_speed = 2
        elif x_speed < -2:
            x_speed = -2
        self.xspeed = x_speed

    def reset(self, pos, speed):
        """
        Player returns to a desired position provided as the argument
        :param pos: the position to return to
        :return: None
        """
        if self.position[0] < pos[0]:
            self.xspeed = 1
        elif self.position[0] > pos[0]:
            self.xspeed = -1
        if self.position[1] < pos[1]:
            self.yspeed = 1
        elif self.position[1] > pos[1]:
            self.yspeed = -1
        if abs(self.position[0] - pos[0]) < 10:
            self.position = (pos[0], self.position[1])
        if abs(self.position[1] - pos[1]) < 10:
            self.position = (self.position[0], pos[1])
        if self.position == pos:
            self.xspeed = speed
            self.yspeed = 0
            resetting_ships.remove(self)

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

def generate_enemies(rows):
    """
    Method generates enemy ships and appends them to the global variable enemy_ships
    :param rows: a list or tuple where each entry specifies the number of ships in that row
    :return: None
    """
    global enemy_ships
    for row_index in range(len(rows)):
        for i in range(rows[row_index]):
            ship = enemyShip(((1 + i) * WIDTH/(1 + rows[row_index]), 30*(1 + row_index)), 10)
            enemy_ships.append(ship)

def draw_enemies(surface):
    """
    Method draws the enemy ships in the global enemy ships list onto the surface provided
    :param surface: the surface to draw the ships onto
    :return: None
    """
    for ship in enemy_ships:
        ship.draw_ship(surface)

def move_enemies(player):
    """
    Method moves the enemy ships in the global enemy ships list according to their speed
    :return: None
    """
    global moves
    global SWAY_DIRECTION
    # Increment the counter to see if the ships need to sway back
    moves += 1
    for ship in enemy_ships:
        # Change directions if the time has come
        ship.change_direction()
        # Have the dropping ships pursue the player
        if ship in dropping_ships:
            if ship in resetting_ships:
                dropping_ships.remove(ship)
            ship.pursue(player)
            # Reset if they have gone to the bottom of the screen
            if ship.get_position()[1] > HEIGHT:
                dropping_ships.remove(ship)
                ship.set_position((ship.get_position()[0], -ship.get_width()))
                resetting_ships.append(ship)
        # Have the dropping ships reset to their original position
        if ship in resetting_ships:
            desired_pos = (ship.get_init_pos()[0] + (enemy_ships[0].get_position()[0] - enemy_ships[0].get_init_pos()[0]),
                    ship.get_init_pos()[1] + (enemy_ships[0].get_position()[1] - enemy_ships[0].get_init_pos()[1]))
            if SWAY_DIRECTION:
                desired_speed = FLEET_SWAY_SPEED
            else:
                desired_speed = -FLEET_SWAY_SPEED
            ship.reset(desired_pos, desired_speed)
        ship.move_speed()
    if moves > 150:
        SWAY_DIRECTION = not SWAY_DIRECTION
        moves = 0

def check_missile_collisions(player):
    """
    Method checks if a missile has collided with an enemy and removes the missile and enemy if there is a collision
    :param player: the player shooting the missiles (a playerShip object)
    :return: None
    """
    global enemy_ships
    global score
    if len(enemy_ships) > 0:
        width = enemy_ships[0].get_width()
    for missile in player.get_missiles():
        for enemy in enemy_ships:
            ePos = enemy.get_position()
            if ePos[0] < missile[0] < ePos[0] + width and ePos[1] < missile[1] < ePos[1] + width:
                score += enemy.get_value()
                enemy_ships.remove(enemy)
                player.explode_missile(missile)

def check_ship_collisions(player):
    """
    Method checks if an enemy ship has collided with the player ship
    :param player: a playerShip object
    :return: None
    """
    global lives
    for ship in dropping_ships:
        ePos = ship.get_position()
        pPos = player.get_position()
        width = ship.get_width()
        eCenter = (ePos[0] + (width/2), ePos[1] + (width/2))
        pCenter = (pPos[0][0], (pPos[0][1] + pPos[1][1])/2)
        distance = math.sqrt(((eCenter[0] - pCenter[0]) ** 2) + ((eCenter[1] - pCenter[1]) ** 2))
        if distance < (1.5 * width/2) + (pPos[1][1] - pPos[0][1])/2:
            try:
                enemy_ships.remove(ship)
                dropping_ships.remove(ship)
            except:
                pass
            player.dec_lives(ship)

def display_score(surface):
    """
    Method displays the score in the bottom right corner of the screen
    :param surface:
    :return:
    """
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render(str(score), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (WIDTH * 0.9, HEIGHT * 0.95)
    surface.blit(text, textRect)

def display_start(surface):
    """
    Method displays the start screen
    :param surface: the surface to draw the start screen on
    :return: None
    """
    surface.fill((0, 0, 100))
    draw_stars(surface)
    font1 = pygame.font.Font('freesansbold.ttf', 80)
    font2 = pygame.font.Font('freesansbold.ttf', 30)
    font3 = pygame.font.Font('freesansbold.ttf', 20)
    title = font1.render("Galaga", True, (255, 255, 255))
    author = font2.render("Taylor Barmak", True, (255, 255, 255))
    instructions = font3.render("Press [space] to play.", True, (255, 255, 255))
    textRectTitle = title.get_rect()
    textRectAuthor = author.get_rect()
    textRectInstructions = instructions.get_rect()
    textRectTitle.center = (WIDTH * 0.5, HEIGHT * 0.5)
    textRectAuthor.center = (WIDTH * 0.5, HEIGHT * 0.6)
    textRectInstructions.center = (WIDTH*0.5, HEIGHT * 0.8)
    surface.blit(title, textRectTitle)
    surface.blit(author, textRectAuthor)
    surface.blit(instructions, textRectInstructions)

def display_lost(surface):
    """
    Method displays the screen that appears when the player loses
    :param surface: the surface to draw the lost screen on
    :return: None
    """
    surface.fill((0, 0, 100))
    draw_stars(surface)
    font1 = pygame.font.Font('freesansbold.ttf', 70)
    font2 = pygame.font.Font('freesansbold.ttf', 80)
    font3 = pygame.font.Font('freesansbold.ttf', 100)
    message = font1.render("You lost!", True, (255, 255, 255))
    scoreMsg = font2.render("Score: " , True, (255, 255, 255))
    finalScore = font3.render(str(score), True, (255, 255, 255))
    textRectMessage = message.get_rect()
    textRectScoreMsg = scoreMsg.get_rect()
    textRectScore = finalScore.get_rect()
    textRectMessage.center = (WIDTH * 0.5, HEIGHT * 0.3)
    textRectScoreMsg.center = (WIDTH * 0.5, HEIGHT * 0.5)
    textRectScore.center = (WIDTH * 0.5, HEIGHT * 0.75)
    surface.blit(message, textRectMessage)
    surface.blit(scoreMsg, textRectScoreMsg)
    surface.blit(finalScore, textRectScore)

def display_continue(surface):
    """
    Method displays the screen that appears in between levels
    :param surface: the surface to draw the continue screen on
    :return: None
    """
    surface.fill((0, 0, 100))
    draw_stars(surface)
    font1 = pygame.font.Font('freesansbold.ttf', 30)
    message = font1.render("Press [space] to continue", True, (255, 255, 255))
    textRectMessage = message.get_rect()
    textRectMessage.center = (WIDTH * 0.5, HEIGHT * 0.5)
    surface.blit(message, textRectMessage)

def drop_enemies(prob):
    """
    Method causes enemies to drop out of the sky at a speed relative to the argument provided
    :param prob: the higher this number the faster the enemies fall
    :return: None
    """
    if len(enemy_ships) > 0:
        num = random.random() * 500
        if num < prob:
            ship = random.choice(enemy_ships)
            dropping_ships.append(ship)
            ship.drop()

if __name__ == '__main__':
    pygame.init()

    set_dimensions()
    size = (int(WIDTH), int(HEIGHT))
    screen = pygame.display.set_mode(size) # , pygame.RESIZABLE)
    pygame.display.set_caption("Galaga")

    clock = pygame.time.Clock()

    # Create the player
    player = PlayerShip()

    # Generate the stars for the background
    generate_stars(300)

    generate_enemies([9, 5, 6, 7])

    atStart = True  # variable to determine if start screen should be shown
    lost = False    # Variable for if player lost the game
    completedLevel = False  # Variable for if player is in between levels
    playing = True  # Variable for if the game should continue
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            # If a key is released and there are no other keys pressed, set speed to 0
            if event.type == pygame.KEYUP and 1 not in pygame.key.get_pressed():
                player.set_speed(0)
            # If a key is pressed, respond accordingly
            if event.type == pygame.KEYDOWN:
                # Move left if the left key is pressed
                if event.key == pygame.K_LEFT:
                    player.set_speed(-5)
                # Move right if the right key is pressed
                if event.key == pygame.K_RIGHT:
                    player.set_speed(5)
                # Shoot missiles if the space bar is pressed
                if event.key == pygame.K_SPACE:
                    if atStart:
                        atStart = not atStart
                    if completedLevel:
                        level += 1
                        completedLevel = False
                        generate_enemies([9, 5, 6, 7])
                    else:
                        player.shoot()

        if atStart:
            display_start(screen)
        elif lost:
            display_lost(screen)
        elif completedLevel:
            display_continue(screen)
        else:
            # Move the coordinates of the player and missiles
            player.move_speed()
            player.move_missiles()
            player.remove_missiles()
            # Keep the player in the viewable frame
            player.keep_in_bounds()

            # Move the enemy ships
            drop_enemies(2 * level)
            move_enemies(player)

            # If all ships have been eliminated, show the in between levels screen
            if len(enemy_ships) == 0:
                completedLevel = True

            # Check for collisions between the missiles and enemies
            check_missile_collisions(player)
            check_ship_collisions(player)
            if player.get_lives() < 0:
                lost = True

            # Cover everything up with the background and draw the stars
            screen.fill((0, 0, 100))
            draw_stars(screen)

            # Draw the player, missiles, and show the lives
            player.draw_player(screen)
            player.draw_missiles(screen)
            player.show_lives(screen)

            # Draw the enemy ships
            draw_enemies(screen)

            # Show the score of the game
            display_score(screen)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


