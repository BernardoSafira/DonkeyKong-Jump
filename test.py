# importações necessárias
import pygame
from pygame.locals import *
import sys
import random
 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

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
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30)) # coloca um quadrado como o player
        self.surf.fill((255,255,0)) # preenche este quadrado com a cor do rgb apontada no argumento
        self.rect = self.surf.get_rect()

        # variaveis bidimensionais pra facilitar calculos dos vetores de movimentação na fisica do jogo (x, y)
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        # variavel que indica se o player esta pulando ou nao
        self.jumping = False
 
    def move(self): # movimentação do player
        self.acc = vec(0,0.5) # gravidade
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # equações fisicas para calcular o movimento com os parametros estabelecidos mais cedo no codigo
        # OBS: Newton era o GOAT       
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        # condicionais para impedir que o jogador saia da tela
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self):  # função de pulo
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self): # função para cancelar o pulo - ativida qnd o jogador solta o espaço
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False) # confere se esta colidindo com algo
        if self.vel.y > 0: # atualiza o estado do player
            if hits: # se colidir com o chao, coloca a velocidade vertical como 0
                if self.pos.y < hits[0].rect.bottom: # impede que o player teleporte para a plataforma por colidir com a parte de baixo da mesma           
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
class platform(pygame.sprite.Sprite): # classe para as plataformas do jogo
    def __init__(self):
        super().__init__()

        # parâmetros ALEATORIOS das plataformas
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10), random.randint(0, HEIGHT-30)))
 
    def move(self): 
        pass
 
 
def check(platform, groupies): # checa se duas plataformas geradas aleatoriamente estão em contato, deletando as novas para garantir que vai ficar sem overlap
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen(): # função de geração randomica das plataformas
    while len(platforms) < 7: # 7 eh o unico numero q n crasha, n me pergunte pq
        width = random.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
             C = check(p, platforms) # chama a função de checagem
        platforms.add(p)
        all_sprites.add(p)

# criação dos objetos 
PT1 = platform()
P1 = DonkeyKong()

# estetica
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

# cria grupo de sprites para colisão
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
platforms = pygame.sprite.Group()
platforms.add(PT1)

# cria as plataformas da tela inicial
for x in range(random.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
# game loop principal
while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() # para o  codigo para não quebrar como o resto do game loop vindo dps
        
        # pulo
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()  
 
    if P1.rect.top <= HEIGHT / 3: # condicional que ve a altura do player para fazer a tela subir junto dele, faz isso atualizando as posições do jogador e das plataformas constantemente
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
 
    plat_gen() # chama a função de geração de plataformas

    displaysurface.fill((0,0,0))
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
 
    pygame.display.update()
    FramePerSec.tick(FPS)