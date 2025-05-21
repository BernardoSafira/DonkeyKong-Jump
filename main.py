# importações necessárias
import pygame
from pygame.locals import *
import sys
import random
import time
import os

pygame.init()
vec = pygame.math.Vector2  # 2 para calculos em 2 dimensões

# parametros para a janela
HEIGHT = 450
WIDTH = 400

# parametros fisicos para a movimentação
ACC = 0.5
FRIC = -0.12

# eh o fps, bem auto explicativo
FPS = 60
FramePerSec = pygame.time.Clock()

# fonte para a pontuação do jogo
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# inicia assets
DK_right = pygame.image.load('Sprites DonkeyKong/Stand Idle 1 Right/Idol 1.png')
DK_left = pygame.image.load('Sprites DonkeyKong/Stand Idle 1 Left/Idol 1.png')

DK_run_right = [
    pygame.image.load('Sprites DonkeyKong/Running Right/Running 1.png'),
    pygame.image.load('Sprites DonkeyKong/Running Right/Running 2.png'),
    pygame.image.load('Sprites DonkeyKong/Running Right/Running 3.png'),
    pygame.image.load('Sprites DonkeyKong/Running Right/Running 4.png'),
    pygame.image.load('Sprites DonkeyKong/Running Right/Running 5.png'),
]

DK_run_left = [
    pygame.image.load('Sprites DonkeyKong/Running Left/Running 1.png'),
    pygame.image.load('Sprites DonkeyKong/Running Left/Running 2.png'),
    pygame.image.load('Sprites DonkeyKong/Running Left/Running 3.png'),
    pygame.image.load('Sprites DonkeyKong/Running Left/Running 4.png'),
    pygame.image.load('Sprites DonkeyKong/Running Left/Running 5.png'),
]

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong: JUMP")  # nome da janela

# coloca barril como icone
try:
    pygame.display.set_icon(pygame.image.load('icon.png'))
except pygame.error:
    print("Warning: icon.png not found.")

recordes = []

def salvar_ranking():
    with open("ranking.txt", "w") as f:
        for nome, score in recordes[:10]:
            f.write(f"{nome},{score}\n")

def carregar_ranking():
    if os.path.exists("ranking.txt"):
        with open("ranking.txt", "r") as f:
            for linha in f:
                nome, score = linha.strip().split(",")
                recordes.append((nome, int(score)))
        recordes.sort(key=lambda x: x[1], reverse=True)

def game_over_screen(name, score):
    displaysurface.fill((255, 0, 0))
    text = font.render("Game Over", True, (255, 255, 255))
    displaysurface.blit(text, (WIDTH / 4, HEIGHT / 2 - 50))
    recordes.append((name, score))
    recordes.sort(key=lambda x: x[1], reverse=True)
    salvar_ranking()
    y = HEIGHT / 2
    for i, (n, s) in enumerate(recordes[:5]):
        rank_text = small_font.render(f"{i+1}. {n} - {s}", True, (255, 255, 255))
        displaysurface.blit(rank_text, (WIDTH / 4, y))
        y += 30
    pygame.display.update()
    pygame.time.wait(3000)

def get_player_name():
    name = ""
    entering = True
    while entering:
        displaysurface.fill((0, 0, 0))
        prompt = small_font.render("Digite seu nome: " + name, True, (255, 255, 255))
        displaysurface.blit(prompt, (20, HEIGHT / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    entering = False
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode
    return name

class DonkeyKong(pygame.sprite.Sprite):  # Donkey Kong eh a classe do player
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))  # coloca um quadrado como o player
        self.surf.fill((0, 0, 0))  # preenche este quadrado com a cor do rgb apontada no argumento - deixar invisivel dps
        self.rect = self.surf.get_rect()

        # variaveis bidimensionais pra facilitar calculos dos vetores de movimentação na fisica do jogo (x, y)
        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.walk_count = 0
        self.direction = "right"  # ou "left"   

        # variavel que indica se o player esta pulando ou nao
        self.jumping = False

        # pontuação do jogador como variável - contato com o piso faz a pontuação ser 1 no começo, isso faz começar com 0 sem ter q mecher nas classes 
        self.score = -1

    def move(self):  # movimentação do player
        self.acc = vec(0, 0.5)  # gravidade

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
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

    def cancel_jump(self):  # função para cancelar o pulo - ativida qnd o jogador solta o espaço
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def draw(self): # esta função foi feita com auxilio do chat gpt
        if self.walk_count >= len(DK_run_right) * 5:
            self.walk_count = 0

        if self.vel.x > 3:
            displaysurface.blit(DK_run_right[self.walk_count // 5], (self.pos.x - 18, self.pos.y -35))
            self.direction = "right"
            self.walk_count += 1
        elif self.vel.x < -3:
            displaysurface.blit(DK_run_left[self.walk_count // 5], (self.pos.x - 18, self.pos.y - 35))
            self.direction = "left"
            self.walk_count += 1
        else:
            # parado — mostra uma imagem estática
            if self.direction == "right":
                displaysurface.blit(DK_right, (self.pos.x - 18, self.pos.y -35))
            else:
                displaysurface.blit(DK_left, (self.pos.x - 18, self.pos.y -35))
    
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)  # confere se esta colidindo com algo
        if self.vel.y > 0:  # atualiza o estado do player
            if hits:  # se colidir com o chao, coloca a velocidade vertical como 0
                if self.pos.y < hits[0].rect.bottom:  # impede que o player teleporte para a plataforma por colidir com a parte de baixo da mesma
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    if hits[0].point == True:  # aumenta a pontuação qnd entra em contato com uma plataforma nova
                        hits[0].point = False
                        self.score += 1
    

class platform(pygame.sprite.Sprite):  # classe para as plataformas do jogo
    def __init__(self):
        super().__init__()

        # parâmetros ALEATORIOS das plataformas
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))

        self.speed = random.randint(-1, 1)  # gera a velocidade aleatoria das plataformas qnd se mexem
        self.moving = True  # Marca se a plataforma deve se mexer
        self.point = True  # atributo que marca se a plataforma ja deu o seu ponto

    def move(self):  # movimenta a plataforma para a direita ou esquerda em ritmo constante + fazer ela trocar de lado qnd chega no fim da tela
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

def check(platform, groupies):  # checa se duas plataformas geradas aleatoriamente estão em contato, deletando as novas para garantir que vai ficar sem overlap
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        return False  # ✅ retorno explícito

def plat_gen():  # função de geração randomica das plataformas
    max_attempts = 100  # ✅ limite de tentativas
    while len(platforms) < 7:  # 7 eh o unico numero q n crasha, n me pergunte pq
        width = random.randrange(50, 100)
        p = platform()
        attempts = 0
        while check(p, platforms) and attempts < max_attempts:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
            attempts += 1
        if attempts < max_attempts:
            platforms.add(p)
            all_sprites.add(p)

def reset_game():
    global P1, PT1, all_sprites, platforms
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    PT1 = platform()
    PT1.moving = False  # garante que o piso n sai andando por ai
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((255, 0, 0))
    PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

    P1 = DonkeyKong()

    all_sprites.add(PT1)
    all_sprites.add(P1)
    platforms.add(PT1)

    for _ in range(random.randint(4, 5)):
        pl = platform()
        attempts = 0
        while check(pl, platforms) and attempts < 100:
            pl = platform()
            attempts += 1
        if attempts < 100:
            platforms.add(pl)
            all_sprites.add(pl)

carregar_ranking()
player_name = get_player_name()

reset_game()

while True:
    P1.update()
    P1.move()  # ✅ movimentação do player com base na física

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()  # para o codigo para não quebrar como o resto do game loop vindo dps

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top > HEIGHT:  # checa se a altura do player está abaixo do fim da tela, se sim mata o jogo
        game_over_screen(player_name, P1.score)
        player_name = get_player_name()
        reset_game()
        continue

    if P1.rect.top <= HEIGHT / 3:  # condicional que ve a altura do player para fazer a tela subir junto dele, faz isso atualizando as posições do jogador e das plataformas constantemente
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    plat_gen()  # chama a função de geração de plataformas

    displaysurface.fill((0, 0, 0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        if isinstance(entity, platform):
            entity.move()

    pontos = str(P1.score)  # coloca os pontos no formato de string
    if P1.score > -1:  # coloquei o if pq senao mostrava -1 como a pontuação inicial por um pouquinho
        text = font.render(pontos, True, (255, 255, 255))
        displaysurface.blit(text, (10, 10))

    nome_text = small_font.render(f"Jogador: {player_name}", True, (255, 255, 255))
    displaysurface.blit(nome_text, (10, 50))

    P1.draw()

    pygame.display.update()
    FramePerSec.tick(FPS)
