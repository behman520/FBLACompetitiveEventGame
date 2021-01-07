import pygame
from pygame.locals import *

pygame.init()

# squares in grid are 33 pixels
screen_width = 1300
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FBLA Project')

game_over = 0

# load images
background = pygame.image.load('background.jpg')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (33, 33))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, game_over):

        if game_over == 0:
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

            # check for collision with enemies
            if pygame.sprite.collide_mask(self, obstacle):
                game_over = -1

        # draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over


player = Player(10, 375)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        img = pygame.image.load('obstacle.png')
        self.image = pygame.transform.scale(img, (66, 66))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.y -= self.move_direction
        self.move_counter += 1
        if self.move_counter > 550:
            self.move_direction *= -1
            self.move_counter = 0

        screen.blit(self.image, self.rect)


obstacle = Obstacle(650, 600)

run = True
while run:

    screen.blit(background, (0, 0))

    game_over = player.update(game_over)
    obstacle.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
