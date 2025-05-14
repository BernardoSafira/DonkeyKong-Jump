import pygame
import sys
from pygame.locals import *
 
pygame.init()
vec = pygame.math.Vector2  #pra jogos 2d

w = 400 #largura
h = 450 #altura

#Elementos da fisica do jogo
aceleracao = 0.5
friccao = -0.12

FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((w, h))
pygame.display.set_caption("Donkey Kong: JUMP")
pygame.display.set_icon(pygame.image.load('icon.png'))

class DonkeyKong(pygame.sprite.Sprite): # Donkey Kong eh a classe do player
    def __init__(self):
        super().__init__() 

        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 420))

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
 
class plataforma(pygame.sprite.Sprite): # classe para as plataformas do jogo
    def __init__(self):
        super().__init__()

        self.surf = pygame.Surface((w, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (w/2, h - 10))
 
PT1 = plataforma()
P1 = DonkeyKong()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
 
# game loop principal
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() # para o  codigo para não quebrar como o resto do game loop vindo dps
     
    displaysurface.fill((0,0,0))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(FPS)