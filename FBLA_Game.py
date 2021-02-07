import pygame
from pygame.locals import *

pygame.init()

# squares in grid are 33 pixels
screen_width = 1300
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FBLA Project')

game_over = False

# loads background
background = pygame.image.load('background.jpg')

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# class for player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (33, 33))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, game_over):

        if game_over == False:
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
            if pygame.sprite.collide_mask(self, obstacle1):
                game_over = True
            if pygame.sprite.collide_mask(self, obstacle2):
                game_over = True

        # draws player onto screen
        screen.blit(self.image, self.rect)

        return game_over


player = Player(10, 375)


# class for obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, move_direction):
        img = pygame.image.load('obstacle.png')
        self.image = pygame.transform.scale(img, (66, 66))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = move_direction
        self.move_counter = 0

    def update(self):
        self.rect.y -= self.move_direction
        self.move_counter += 1
        if self.move_counter > screen_height - 66:
            self.move_direction *= -1
            self.move_counter = 0

        screen.blit(self.image, self.rect)


obstacle1 = Obstacle(screen_width/2 + 33, screen_height - 66, 1)
obstacle2 = Obstacle(screen_width/2 - 66, 0, -1)


# class for coins
coin1_collected = False


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        img = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(img, (33, 33))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, coin1_collected, score_value):
        if not coin1_collected:
            screen.blit(self.image, self.rect)
            if pygame.sprite.collide_mask(self, player):
                coin1_collected = True
                score_value += 1/2
                show_score(textX, textY)
        return  score_value


coin1 = Coin(screen_width/2, screen_height/2)


run = True
while run:
    screen.blit(background, (0, 0))

    show_score(textX, textY)
    game_over = player.update(game_over)
    obstacle1.update()
    obstacle2.update()
    coin1_collected = coin1.update(coin1_collected, int(score_value))
    score_value = coin1.update(int(score_value), coin1_collected)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
