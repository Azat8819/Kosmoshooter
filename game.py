import time
import asyncio
import random
import pygame_menu
import sys
import pygame

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космошутер")
clock = pygame.time.Clock()


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()
        laser_sound.set_volume(5)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            self.speedy = random.randrange(1, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()

            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class GoldenMeteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            self.speedy = random.randrange(1, 10)

    class mol(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = random.choice(meteor_images)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)
            self.speedx = random.randrange(-5, 5)

        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-140, - 100)
                self.speedy = random.randrange(1, 10)


triger = False


def a():
    global triger
    triger = True


def menu():
    menu = pygame_menu.Menu('Welcome', 800, 600,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', a)
    pygame.display.flip()
    menu.add.button('Quit', pygame_menu.events.EXIT)


# waighting = True
# while waighting:
# 	if triger:
# 		waighting = False
# 	else:
# 		menu.mainloop(screen)
sound_on = 0


def show_go_screen():
    global sound_on
    pygame.mixer.music.load("assets/music.ogg")
    pygame.mixer.music.set_volume(0.2)
    screen.blit(background, [0, 0])
    draw_text(screen, "Нажмите  пробел чтобы продолжить", 20, WIDTH // 2, HEIGHT * 3 / 4)
    draw_text(screen, "Нажмите клавишу ESCAPE  чтобы выйти", 20, 390, 500)
    draw_text(screen, "Нажмите клавишу M чтобы включить/выключить музыку", 20, 390, 550)
    draw_text(screen, "Космошутер", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Добро пожаловать в меню", 65, 400, 60)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        sound_on += 1
                        if sound_on % 2 == 0:
                            pygame.mixer.music.play()
                        if sound_on % 2 == 1:
                            pygame.mixer.music.stop()
        except Exception:
            sys.exit()


def end():
    global sound_on
    global score
    pygame.mixer.music.load("assets/music.ogg")
    pygame.mixer.music.set_volume(0.2)
    score = 0
    screen.blit(background, [0, 0])
    draw_text(screen, "Игра окончена!", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Нажмите  пробел чтобы начать заново", 20, WIDTH // 2, HEIGHT * 3 / 4)
    draw_text(screen, "Нажмите клавишу ESCAPE  чтобы выйти", 20, 390, 500)
    draw_text(screen, "Нажмите клавишу M чтобы включить/выключить музыку", 20, 390, 550)
    pygame.display.flip()
    time.sleep(2)
    waiting = True
    player.shield += 100
    while waiting:
        clock.tick(60)
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        sound_on += 1
                        if sound_on % 2 == 0:
                            pygame.mixer.music.play()
                        if sound_on % 2 == 1:
                            pygame.mixer.music.stop()
        except Exception:
            sys.exit()


def endscore():
    global score
    screen.blit(background, [0, 0])
    draw_text(screen, "ПОБЕДА!", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, f"Выход через: 5 секунд", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    time.sleep(5)
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                pygame.quit()


meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png",
               "assets/meteorGrey_big4.png", "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png",
               "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png", "assets/meteorGrey_tiny1.png",
               "assets/meteorGrey_tiny2.png", "assets/meteorZolot.png", "assets/hil.png"]

zeteor_images = []
zeteor_list = ["assets/meteorZolot.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

explosion_anim = []

for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

background = pygame.image.load("assets/background.png").convert()

laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

game_over = True
running = True
lp = True

while running:
    if game_over:

        show_go_screen()

        game_over = False

        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.set_volume(0.2)
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

        if score >= 200:
            endscore()

    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
    if player.shield <= 0:
        end()

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()
pygame.quit()
