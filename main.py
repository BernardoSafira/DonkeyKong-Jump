import pygame
import sys
from pygame.locals import *
 
pygame.init()
vec = pygame.math.Vector2  #pra jogos 2d

# parametros para a janela
HEIGHT = 450
WIDTH = 400
# parametros fisicos para a movimentação
ACC = 0.5
FRIC = -0.12
# eh o fps, bem auto explicativo
FPS = 60
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong: JUMP") # nome da janela
pygame.display.set_icon(pygame.image.load('icon.png')) # coloca barril como icone

class DonkeyKong(pygame.sprite.Sprite): # Donkey Kong eh a classe do player
    def __init__(self):
        super().__init__() 

        self.surf = pygame.Surface((30, 30)) # coloca um quadrado 30 por 40
        self.surf.fill((128,255,40)) # preenche este quadrado com a cor do rgb apontada no argumento
        self.rect = self.surf.get_rect(center = (10, 420))

        # variaveis bidimensionais pra facilitar calculos dos vetores de movimentação na fisica do jogo (x, y)
        self.pos = vec((10, 385)) 
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def move(self): # movimentação do player
        self.acc = vec(0,0)
 
        pressed_keys = pygame.key.get_pressed()
        
        # condicionais para cada tecla
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC     
        
        # equações fisicas para calcular o movimento com os parametros mais cedo no codigo
        # OBS: Newton era o GOAT
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # condicionais para impedir que o jogador  saia da tela
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
     
        self.rect.midbottom = self.pos
 
class plataforma(pygame.sprite.Sprite): # classe para as plataformas do jogo
    def __init__(self):
        super().__init__()

        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

# criação dos objetos 
PT1 = plataforma()
P1 = DonkeyKong()

# estetica
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
 
    pygame.display.update() # atualiza o display constantemente	
    P1.move() # possibilita o player a se movimentar
    FramePerSec.tick(FPS)