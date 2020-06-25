#lib
import pygame , random , time , os
from pygame.locals import *
from itertools import repeat

pygame.init()
#screen
WIDTH , HEIGHT = 400 , 600
screen = pygame.display.set_mode((WIDTH , HEIGHT))

#speed and score
speed = 5
score = 0

#fps
fps = pygame.time.Clock()

#font
font_1 = pygame.font.SysFont("Helvetica",24)
game_over = font_1.render("Game Over!!",True,(255,255,255))
play = font_1.render("press 'space'to start",True,(0,0,0))

#title and icon
pygame.display.set_caption("car")
icon = pygame.image.load(os.path.join("img","icon.png"))
pygame.display.set_icon(icon)

#background
background = pygame.transform.scale(pygame.image.load(os.path.join("img","background.png")),(WIDTH , HEIGHT))
bg_move_x , bg_move_y = 0 , 0

#enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("img","enemy.png"))
        self.surf = pygame.Surface((40 , 70))
        self.rect = self.surf.get_rect(center = (random.randint(40,WIDTH-40), 0))
    def move(self):
        global score
        self.rect.move_ip(0,speed)
        if (self.rect.bottom > 600):
            global score
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("img","player.png"))
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))

    def move(self):
        if self.rect.left > 0:
              if pygame.key.get_pressed()[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:
              if pygame.key.get_pressed()[K_RIGHT]:
                  self.rect.move_ip(5, 0)

#var
player = Player()
enemy = Enemy()

#sprite
enemies = pygame.sprite.Group()
enemies.add(enemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

#
a = pygame.USEREVENT + 1
pygame.time.set_timer(a, 1000)

#title
def title():
  while True:
    screen.fill((0,255,255))
    screen.blit(play , (90,300))
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main()
    pygame.display.update()

#Game Loop
def main():
  while True:
    global speed
    pygame.event.pump()
    fps.tick(60)
    screen.blit(background , (0,0))
    for event in pygame.event.get():
        if event.type == a:
              speed += 0.5
        if event.type == QUIT:
            exit()


    #score
    score_font = font_1.render(str(score), True, (0,255,0))
    screen.blit(score_font ,(0,0))


    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(player, enemies):
        screen.fill((255,0,0))
        screen.blit(game_over, (125,300))
        pygame.display.update()
        time.sleep(2)
        for entity in all_sprites:
            entity.kill()
            time.sleep(2)
            pygame.quit()
            exit()

    pygame.display.update()


title()
