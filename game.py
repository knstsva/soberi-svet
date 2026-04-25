import pygame
import random
import sys
import math
import os

pygame.init()

# ---------------- AUDIO ----------------
pygame.mixer.init()

click = None
hit = None

try:
    if os.path.exists("click.wav"):
        click = pygame.mixer.Sound("click.wav")
except:
    pass

try:
    if os.path.exists("hit.wav"):
        hit = pygame.mixer.Sound("hit.wav")
except:
    pass

def play_click():
    if click:
        click.play()

def play_hit():
    if hit:
        hit.play()

def play_music():
    if os.path.exists("music.mp3"):
        try:
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("СОБЕРИ СВЕТ")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
BG = (20, 10, 40)
PINK = (255, 100, 180)
BLUE = (120, 180, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 230, 120)

font = pygame.font.SysFont("arial", 26)
big = pygame.font.SysFont("arial", 60)

# ---------------- STATES ----------------
MENU = "menu"
MODE = "mode"
DIFF = "diff"
GAME = "game"
RESULT = "result"

state = MENU

# ---------------- GAME DATA ----------------
mode = 1
time_limit = 60
goal = 15

timer = 0
record = 0

fireworks = []

# ---------------- PLAYER ----------------
class Player:
    def __init__(self, x, y, color, keys):
        self.x = x
        self.y = y
        self.color = color
        self.keys = keys
        self.score = 0

    def move(self):
        k = pygame.key.get_pressed()
        if k[self.keys[0]]: self.y -= 4
        if k[self.keys[1]]: self.y += 4
        if k[self.keys[2]]: self.x -= 4
        if k[self.keys[3]]: self.x += 4

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 18)

class Point:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x = random.randint(50, WIDTH-50)
        self.y = random.randint(50, HEIGHT-50)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), 10)

# ---------------- FIREWORKS ----------------
def spawn_firework():
    x = random.randint(200, WIDTH-200)
    y = random.randint(100, 400)

    for _ in range(30):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 6)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        color = random.choice([PINK, BLUE, YELLOW, WHITE])

        fireworks.append([x, y, vx, vy, color, 60])

def update_fireworks():
    for f in fireworks[:]:
        f[0] += f[2]
        f[1] += f[3]
        f[5] -= 1

        pygame.draw.circle(screen, f[4], (int(f[0]), int(f[1])), 3)

        if f[5] <= 0:
            fireworks.remove(f)

# ---------------- START ----------------
def start_game():
    global p1, p2, point, timer, state

    p1 = Player(200, 300, PINK, (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d))

    if mode == 2:
        p2 = Player(700, 300, BLUE, (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT))
    else:
        p2 = None

    point = Point()
    timer = time_limit * 60
    state = GAME

# ---------------- MENU ----------------
def menu():
    global state

    play_music()

    while state == MENU:
        clock.tick(60)
        screen.fill(BG)

        screen.blit(big.render("СОБЕРИ СВЕТ", True, WHITE), (250, 120))

        b1 = pygame.Rect(300, 250, 300, 60)
        b2 = pygame.Rect(300, 340, 300, 60)

        pygame.draw.rect(screen, PINK, b1)
        pygame.draw.rect(screen, BLUE, b2)

        screen.blit(font.render("СТАРТ", True, WHITE), (420, 265))
        screen.blit(font.render("ВЫХОД", True, WHITE), (420, 355))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                play_click()
                if b1.collidepoint(e.pos):
                    state = MODE
                if b2.collidepoint(e.pos):
                    sys.exit()

        pygame.display.flip()

# ---------------- MODE ----------------
def mode_select():
    global state, mode

    while state == MODE:
        clock.tick(60)
        screen.fill(BG)

        screen.blit(big.render("РЕЖИМ", True, WHITE), (360, 120))

        b1 = pygame.Rect(300, 250, 300, 60)
        b2 = pygame.Rect(300, 340, 300, 60)

        pygame.draw.rect(screen, PINK, b1)
        pygame.draw.rect(screen, BLUE, b2)

        screen.blit(font.render("1 ИГРОК", True, WHITE), (400, 265))
        screen.blit(font.render("2 ИГРОКА", True, WHITE), (400, 355))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                play_click()
                if b1.collidepoint(e.pos):
                    mode = 1
                    state = DIFF
                if b2.collidepoint(e.pos):
                    mode = 2
                    state = DIFF

        pygame.display.flip()

# ---------------- DIFF ----------------
def difficulty():
    global state, time_limit

    while state == DIFF:
        clock.tick(60)
        screen.fill(BG)

        screen.blit(big.render("СЛОЖНОСТЬ", True, WHITE), (280, 100))

        buttons = [
            (120, "ЛЕГКО 120"),
            (60, "СРЕДНЕ 60"),
            (30, "СЛОЖНО 30")
        ]

        for i, (t, txt) in enumerate(buttons):
            r = pygame.Rect(250, 220 + i*80, 400, 60)
            pygame.draw.rect(screen, PINK if i%2==0 else BLUE, r)
            screen.blit(font.render(txt, True, WHITE), (300, r.y+15))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                play_click()
                for i, (t, _) in enumerate(buttons):
                    r = pygame.Rect(250, 220 + i*80, 400, 60)
                    if r.collidepoint(e.pos):
                        time_limit = t
                        start_game()

        pygame.display.flip()

# ---------------- GAME ----------------
def game():
    global state, timer, record

    clock.tick(60)
    screen.fill(BG)

    p1.move()
    if p2:
        p2.move()

    if math.hypot(p1.x-point.x, p1.y-point.y) < 18:
        p1.score += 1
        point.spawn()
        play_hit()

    if p2 and math.hypot(p2.x-point.x, p2.y-point.y) < 18:
        p2.score += 1
        point.spawn()
        play_hit()

    p1.draw()
    if p2:
        p2.draw()
    point.draw()

    timer -= 1

    screen.blit(font.render(f"P1: {p1.score}", True, WHITE), (20, 20))
    if p2:
        screen.blit(font.render(f"P2: {p2.score}", True, WHITE), (20, 60))

    collected = p1.score + (p2.score if p2 else 0)

    screen.blit(font.render(f"СОБРАНО: {collected}/{goal}", True, WHITE), (20, 100))
    screen.blit(font.render(f"ВРЕМЯ: {timer//60}", True, WHITE), (20, 140))

    if timer <= 0 or collected >= goal:
        state = RESULT

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

# ---------------- RESULT ----------------
def result():
    global state, record

    collected = p1.score + (p2.score if p2 else 0)

    new_record = collected > record
    if new_record:
        record = collected
        spawn_firework()

    while state == RESULT:
        clock.tick(60)
        screen.fill(BG)

        update_fireworks()

        title = "ПОБЕДА" if collected >= goal else "ПОРАЖЕНИЕ"
        screen.blit(big.render(title, True, WHITE), (320, 180))

        screen.blit(font.render(f"Счёт: {collected}", True, WHITE), (380, 300))
        screen.blit(font.render(f"Рекорд: {record}", True, WHITE), (380, 340))

        if new_record:
            screen.blit(font.render("НОВЫЙ РЕКОРД!", True, YELLOW), (360, 420))

        screen.blit(font.render("Нажми любую клавишу", True, WHITE), (320, 500))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.KEYDOWN:
                state = MENU

        pygame.display.flip()

# ---------------- LOOP ----------------
while True:
    if state == MENU:
        menu()
    elif state == MODE:
        mode_select()
    elif state == DIFF:
        difficulty()
    elif state == GAME:
        game()
    elif state == RESULT:
        result()