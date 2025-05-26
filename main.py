# importações necessárias
import pygame
from pygame.locals import *
import sys
import random
import time
import os

pygame.init()
pygame.mixer.init()  # Inicializa o mixer de som

vec = pygame.math.Vector2  # 2 para cálculos em 2 dimensões

# parâmetros para a janela
HEIGHT = 450
WIDTH = 400

# parâmetros físicos para a movimentação
ACC = 0.5
FRIC = -0.12

FPS = 60
FramePerSec = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# inicia assets
fundo = pygame.image.load('selva.png')
fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

imagem_inicial = pygame.image.load('LOGO_DK.jpg')
imagem_inicial = pygame.transform.scale(imagem_inicial, (WIDTH, HEIGHT))
imagem_game_over = pygame.image.load('Tela de Game Over.png')
imagem_game_over = pygame.transform.scale(imagem_game_over, (WIDTH, HEIGHT))

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

DK_jump_right = [
    pygame.image.load('Sprites DonkeyKong/Jump Right/Jump 1.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Right/Jump 2.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Right/Jump 3.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Right/Jump 4.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Right/Jump 5.png'),
]

DK_jump_left = [
    pygame.image.load('Sprites DonkeyKong/Jump Left/Jump 1.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Left/Jump 2.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Left/Jump 3.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Left/Jump 4.png'),
    pygame.image.load('Sprites DonkeyKong/Jump Left/Jump 5.png'),
]

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong: JUMP")

try:
    pygame.display.set_icon(pygame.image.load('icon.png'))
except pygame.error:
    print("Warning: icon.png not found.")

# Carrega trilhas sonoras
musica_nome = 'Soundtrack/Menu.mp3'
musica_fase = 'Soundtrack/Fase.mp3'
som_game_over = pygame.mixer.Sound('Soundtrack/death.mp3')
som_pulo = pygame.mixer.Sound('Soundtrack/Som de pulo.mp3')

# Funções auxiliares para música
def tocar_musica(caminho, loop=-1):
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play(loop)

def parar_musica():
    pygame.mixer.music.stop()

# Tela inicial com a imagem e música
def tela_inicial():
    tocar_musica(musica_nome)
    waiting = True
    while waiting:
        displaysurface.blit(imagem_inicial, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False

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
    parar_musica()
    som_game_over.play()

    # Exibe a imagem de game over por 3 segundos
    displaysurface.blit(imagem_game_over, (0, 0))
    pygame.display.update()
    pygame.time.wait(3000)

    # Registra a pontuação
    recordes.append((name, score))
    recordes.sort(key=lambda x: x[1], reverse=True)
    salvar_ranking()

    # Depois exibe ranking até ENTER
    waiting = True
    while waiting:
        displaysurface.fill((0, 0, 0))
        title = font.render("Ranking", True, (255, 255, 255))
        displaysurface.blit(title, (WIDTH // 3, 20))

        y = 80
        for i, (n, s) in enumerate(recordes[:5]):
            rank_text = small_font.render(f"{i+1}. {n} - {s}", True, (255, 255, 255))
            displaysurface.blit(rank_text, (WIDTH // 4, y))
            y += 30

        info = small_font.render("Aperte ENTER para reiniciar", True, (255, 255, 255))
        displaysurface.blit(info, (WIDTH // 10, HEIGHT - 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False

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
    parar_musica()
    return name

class DonkeyKong(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.walk_count = 0
        self.direction = "right"
        self.jumping = False
        self.jump_count = 0
        self.score = -1

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.acc.x = ACC
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            som_pulo.play()
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3

    def draw(self):
        if self.walk_count >= len(DK_run_right) * 5:
            self.walk_count = 0
        if self.jump_count >= len(DK_jump_right) * 5:
            self.jump_count = len(DK_jump_right) * 5 - 1
        if self.jumping:
            if self.direction == "right":
                displaysurface.blit(DK_jump_right[self.jump_count // 5], (self.pos.x - 18, self.pos.y - 35))
            else:
                displaysurface.blit(DK_jump_left[self.jump_count // 5], (self.pos.x - 18, self.pos.y - 35))
            self.jump_count += 1
        elif self.vel.x > 3:
            displaysurface.blit(DK_run_right[self.walk_count // 5], (self.pos.x - 18, self.pos.y - 35))
            self.direction = "right"
            self.walk_count += 1
            self.jump_count = 0
        elif self.vel.x < -3:
            displaysurface.blit(DK_run_left[self.walk_count // 5], (self.pos.x - 18, self.pos.y - 35))
            self.direction = "left"
            self.walk_count += 1
            self.jump_count = 0
        else:
            if self.direction == "right":
                displaysurface.blit(DK_right, (self.pos.x - 18, self.pos.y - 35))
            else:
                displaysurface.blit(DK_left, (self.pos.x - 18, self.pos.y - 35))
            self.jump_count = 0

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits and self.pos.y < hits[0].rect.bottom:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
                self.jumping = False
                if hits[0].point:
                    hits[0].point = False
                    self.score += 1

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))
        self.speed = random.randint(-1, 1)
        self.moving = True
        self.point = True

    def move(self):
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    for entity in groupies:
        if entity == platform:
            continue
        if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
            return True
    return False

def plat_gen():
    max_attempts = 100
    while len(platforms) < 7:
        p = platform()
        attempts = 0
        while check(p, platforms) and attempts < max_attempts:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - p.surf.get_width()), random.randrange(-50, 0))
            attempts += 1
        if attempts < max_attempts:
            platforms.add(p)
            all_sprites.add(p)

def reset_game():
    global P1, PT1, all_sprites, platforms
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    PT1 = platform()
    PT1.moving = False
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((85, 0, 0))
    PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
    P1 = DonkeyKong()
    all_sprites.add(PT1, P1)
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
tela_inicial()
player_name = get_player_name()
reset_game()
tocar_musica(musica_fase)

while True:
    P1.update()
    P1.move()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
    if P1.rect.top > HEIGHT:
        game_over_screen(player_name, P1.score)
        tela_inicial()
        player_name = get_player_name()
        reset_game()
        tocar_musica(musica_fase)
        continue
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    plat_gen()
    displaysurface.blit(fundo, (0, 0))
    for entity in all_sprites:
        if not isinstance(entity, DonkeyKong):
            displaysurface.blit(entity.surf, entity.rect)
        if isinstance(entity, platform):
            entity.move()
    pontos = str(P1.score)
    if P1.score > -1:
        text = font.render(pontos, True, (255, 255, 255))
        displaysurface.blit(text, (10, 10))
    nome_text = small_font.render(f"Jogador: {player_name}", True, (255, 255, 255))
    displaysurface.blit(nome_text, (10, 50))
    P1.draw()
    pygame.display.update()
    FramePerSec.tick(FPS)
