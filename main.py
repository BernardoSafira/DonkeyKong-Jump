# importações necessárias
import pygame
from pygame.locals import *
import sys
import random
 
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

        self.surf = pygame.Surface((43, 43)) # coloca um quadrado 30 por 40
        self.surf.fill((128,255,40)) # preenche este quadrado com a cor do rgb apontada no argumento
        self.rect = self.surf.get_rect(center = (10, 420))

        # variaveis bidimensionais pra facilitar calculos dos vetores de movimentação na fisica do jogo (x, y)
        self.pos = vec((10, 385)) 
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def move(self): # movimentação do player
        self.acc = vec(0,0.5) # gravidade
        pressed_keys = pygame.key.get_pressed()
        
        # condicionais para cada tecla
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC     
        if pressed_keys[K_SPACE]:
            P1.jump()
        
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
    
    def jump(self):
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        if hits:
            self.vel.y = -15

    def update(self): # atualiza o estado do player
        hits = pygame.sprite.spritecollide(P1 , plataformas, False) # confere se esta colidindo com algo
        if P1.vel.y > 0:        
            if hits: # se colidir com o chao, coloca a velocidade vertical como 0
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1

 
class piso(pygame.sprite.Sprite): # classe para o piso do jogo
    def __init__(self):
        super().__init__()

        # parametros do piso
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
class plataforma(pygame.sprite.Sprite): # classe para as plataformas do jogo
    def __init__(self):
        super().__init__()

        # parâmetros ALEATORIOS das plataformas
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10), random.randint(0, HEIGHT-30)))

def plat_gen(): # função de geração randomica das plataformas
    while len(plataformas) < 7: # 7 eh o unico numero q funciona de um jeito bom, n me pergunte pq
        width = random.randrange(50,100)

        p  = plataforma()             
        p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
        plataformas.add(p)
        all_sprites.add(p)

# criação dos objetos 
chao = piso()
P1 = DonkeyKong()

# estetica
all_sprites = pygame.sprite.Group()
all_sprites.add(chao)
all_sprites.add(P1)

# cria grupo de sprites para colisão
plataformas = pygame.sprite.Group()
plataformas.add(chao)

# cria as plataformas da tela inicial
for x in range(random.randint(5, 6)):
    pl = plataforma()
    plataformas.add(pl)
    all_sprites.add(pl)

# game loop principal
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() # para o  codigo para não quebrar como o resto do game loop vindo dps
        
    displaysurface.fill((0,0,0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    plat_gen() # chama a função de geração de plataformas

    if P1.rect.top <= HEIGHT / 3: # condicional que ve a altura do player para fazer a tela subir junto dele, faz isso atualizando as posições do jogador e das plataformas constantemente
        P1.pos.y += abs(P1.vel.y)
        for plat in plataformas:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    pygame.display.update() # atualiza o display constantemente	
    P1.update() # atualiza o player constantemente
    P1.move() # possibilita o player a se movimentar

    FramePerSec.tick(FPS)