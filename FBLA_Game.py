import pygame
from pygame.locals import *
import pickle

pygame.init()

# squares in grid are 33 pixels
screen_width = 1300
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FBLA Project')

main_menu = True
instructions_screen = False
game = False
level = 1

# loads background
background = pygame.image.load('background.jpg')

# score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_textX = 10
score_textY = 10


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# lives
life_count = 3
life_font = pygame.font.Font('freesansbold.ttf', 32)
life_textX = screen_width - 150
life_textY = 10


def show_lives(x, y):
    lives = life_font.render("Lives: " + str(life_count), True, (255, 255, 255))
    screen.blit(lives, (x, y))


# class for button
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.image = image
        self.transform_image = pygame.transform.scale(image, (250, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    # draws button
    def draw_button(self):
        screen.blit(self.image, self.rect)
        action = False

        # gets mouse position
        pos = pygame.mouse.get_pos()

        # checks mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


start_button = Button(screen_width/2 - 600, screen_height/2 - 100, pygame.image.load('Start button.png'))
exit_button = Button(screen_width/2 + 50, screen_height/2 - 100, pygame.image.load('Exit button.png'))
main_menu_button1 = Button(screen_width/2 - 270, screen_height/2 - 50, pygame.image.load('Main Menu button.png'))
instructions_button = Button(screen_width/2 - 270, screen_height/2 + 150, pygame.image.load('Instructions button.png'))
main_menu_button2 = Button(screen_width/2 - 270, screen_height/2 - 320, pygame.image.load('Main Menu button.png'))


# class for player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (33, 33))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, life_count, x, y):
        if life_count != 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x -= 1
            if key[pygame.K_RIGHT]:
                self.rect.x += 1
            if key[pygame.K_UP]:
                self.rect.y -= 1
            if key[pygame.K_DOWN]:
                self.rect.y += 1

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
            elif self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.right > screen_width:
                self.rect.right = screen_width
            elif self.rect.left < 0:
                self.rect.left = 0

            # checks for collision with enemies
            if pygame.sprite.spritecollide(self, level1_obstacle_group, False):
                self.rect.x = x
                self.rect.y = y
                life_count -= 1

        # draws player onto screen
        screen.blit(self.image, self.rect)

        return life_count


player = Player(10, screen_height/2)


# class for obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, move_directionY, move_directionX, move_counter):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('obstacle.png')
        self.image = pygame.transform.scale(img, (66, 66))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_directionY = move_directionY
        self.move_directionX = move_directionX
        self.start_move_counter = 0
        self.move_counter = move_counter

    def update(self):
        self.rect.y -= self.move_directionY
        self.rect.x -= self.move_directionX
        self.start_move_counter += 1
        if self.start_move_counter > self.move_counter:
            self.move_directionY *= -1
            self.move_directionX *= -1
            self.start_move_counter = 0

        screen.blit(self.image, self.rect)

# Obstacles for level 1
level1_obstacle_group = pygame.sprite.Group()
level1_obstacle1 = Obstacle(screen_width/2 + 33, screen_height - 66, 1, 0, screen_height - 66)
level1_obstacle_group.add(level1_obstacle1)
level1_obstacle2 = Obstacle(screen_width/2 - 99, 0, -1, 0, screen_height - 66)
level1_obstacle_group.add(level1_obstacle2)
level1_obstacle3 = Obstacle(screen_width/2 + 500, screen_height - 300, 0, 2, (screen_width - 200)/2)
level1_obstacle_group.add(level1_obstacle3)
level1_obstacle4 = Obstacle(screen_width/2 + 500, screen_height - 500, 0, 2, (screen_width - 200)/2)
level1_obstacle_group.add(level1_obstacle4)

# Obstacles for level 2
level2_obstacle_group = pygame.sprite.Group()
level2_obstacle1 = Obstacle()
level2_obstacle_group.add(level2_obstacle1)
level2_obstacle2 = Obstacle()
level2_obstacle_group.add(level2_obstacle2)
level2_obstacle3 = Obstacle()
level2_obstacle_group.add(level2_obstacle3)
level2_obstacle4 = Obstacle()
level2_obstacle_group.add(level2_obstacle4)


# class for coins
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(img, (33, 33))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


level1_coin_group = pygame.sprite.Group()
level1_coin1 = Coin(screen_width / 2, screen_height / 2)
level1_coin_group.add(level1_coin1)
level1_coin2 = Coin(100, 100)
level1_coin_group.add(level1_coin2)
level1_coin3 = Coin(screen_width - 100, 100)
level1_coin_group.add(level1_coin3)
level1_coin4 = Coin(100, screen_height - 100)
level1_coin_group.add(level1_coin4)
level1_coin5 = Coin(screen_width - 100, screen_height - 100)
level1_coin_group.add(level1_coin5)


# class for finish line
level_completed = False


class FinishLine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Finish line.png')
        self.image = pygame.transform.scale(img, (50, screen_height - 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    '''def update(self, level_completed):
        screen.blit(self.image, self.rect)
        if not level_completed:
            if pygame.sprite.collide_mask(self, player):
                level_completed = True
                player.rect.x = 10
                player.rect.y = screen_height/2
        return level_completed'''


finish_line_group = pygame.sprite.Group()
finish_line = FinishLine(screen_width - 50, screen_height/2 - (screen_height - 100)/2)
finish_line_group.add(finish_line)

# game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_overX = screen_width/2 - 180
game_overY = 100


# prints game over text
def print_game_over(x, y):
    game_over = game_over_font.render("Game over!", True, (255, 255, 255))
    screen.blit(game_over, (x, y))


# prints instructions text
def print_instructions(x, y):
    screen.blit(pygame.image.load('Instruction text.png'), (x, y))


run = True
while run:
    screen.blit(background, (0, 0))

    if main_menu == True:
        if exit_button.draw_button():
            run = False
        if start_button.draw_button():
            main_menu = False
            game = True
            life_count = 3
            score_value = 0
        if instructions_button.draw_button():
            instructions_screen = True
            main_menu = False
            game = False
            life_count = 3
    elif main_menu == False and game == True:
        show_score(score_textX, score_textY)
        show_lives(life_textX, life_textY)
        if level == 1:
            life_count = player.update(life_count, 10, screen_height/2)
            level1_obstacle_group.draw(screen)
            level1_obstacle_group.update()
            level1_coin_group.draw(screen)
            finish_line_group.draw(screen)
            if pygame.sprite.spritecollide(player, level1_coin_group, True):
                score_value += 1
            if pygame.sprite.spritecollide(player, finish_line_group, False):
                player.rect.x = 10
                player.rect.y = screen_height / 2
                level1_obstacle_group.remove(level1_obstacle1, level1_obstacle2, level1_obstacle3, level1_obstacle4)
                level += 1
        if level == 2:
            life_count = player.update(life_count, 10, screen_height/2)
        if level == 3:
            life_count = player.update(life_count, 10, screen_height/2)
        '''level_completed = finish_line.update(level_completed)
        if level_completed == True:
            level += 1
            level_completed = False'''
        if life_count == 0:
            screen.blit(background, (0, 0))
            print_game_over(game_overX, game_overY)
            if main_menu_button1.draw_button():
                main_menu = True
    elif instructions_screen == True and main_menu == False:
        screen.blit(background, (0, 0))
        print_instructions(screen_width/2 - 400, screen_height/2 - 100)
        if main_menu_button2.draw_button():
            main_menu = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif pygame.key.get_pressed()[K_ESCAPE]:
            run = False

    pygame.display.update()

pygame.quit()
