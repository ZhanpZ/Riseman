import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#initialize the game window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Riseman")

#load image
backyground_img = pygame.image.load(os.path.join("img", "background.jpg")).convert()
player_img = pygame.image.load(os.path.join("img", "player_baby.png")).convert()
player2_img = pygame.image.load(os.path.join("img", "player_KG5.png")).convert()
player2_img = pygame.transform.scale(player2_img, (100, 78))
player3_img = pygame.image.load(os.path.join("img", "player_MHigh.png")).convert()
player3_img = pygame.transform.scale(player3_img, (100, 78))
player4_img = pygame.image.load(os.path.join("img", "player_work.png")).convert()
player4_img = pygame.transform.scale(player4_img, (100, 78))
mini_img = pygame.transform.scale(player_img, (50, 35))
mini_img.set_colorkey(WHITE)
pygame.display.set_icon(mini_img)
tier1_img = []
tier1_img.append(pygame.image.load(os.path.join("img", "enemy_dog.png")).convert())
tier1_img.append(pygame.image.load(os.path.join("img", "enemy_bug.png")).convert())
tier1_img.append(pygame.image.load(os.path.join("img", "enemy_ghost.png")).convert())
tier2_img = []
tier2_img.append(pygame.image.load(os.path.join("img", "enemy_bully.png")).convert())
tier2_img.append(pygame.image.load(os.path.join("img", "enemy_sport.png")).convert())
tier2_img.append(pygame.image.load(os.path.join("img", "enemy_math.png")).convert())
tier3_img = []
tier3_img.append(pygame.image.load(os.path.join("img", "enemy_love.png")).convert())
tier3_img.append(pygame.image.load(os.path.join("img", "enemy_test.png")).convert())
tier3_img.append(pygame.image.load(os.path.join("img", "enemy_parent.png")).convert())
tier4_img = []
tier4_img.append(pygame.image.load(os.path.join("img", "enemy_money.png")).convert())
tier4_img.append(pygame.image.load(os.path.join("img", "enemy_time.png")).convert())
tier4_img.append(pygame.image.load(os.path.join("img", "enemy_marriage.png")).convert())
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
#explosion
explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
explosion_animation['py'] = []
for i in range(9):
    explosion_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    explosion_img.set_colorkey(BLACK)
    explosion_animation['lg'].append(pygame.transform.scale(explosion_img, (75, 75)))
    explosion_animation['sm'].append(pygame.transform.scale(explosion_img, (30, 30)))
    player_explosion_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_explosion_img.set_colorkey(BLACK)
    explosion_animation['py'].append(player_explosion_img)
#support items
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "Plus.jpg")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "puncher.png")).convert()

#load sound
bullet_sound = pygame.mixer.Sound(os.path.join("sound", "punch.mp3"))
bullet_sound.set_volume(0.2)
death_sound = pygame.mixer.Sound(os.path.join("sound", "deathsound.mp3"))
death_sound.set_volume(0.1 )
explosion_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "Pop.mp3")),
    pygame.mixer.Sound(os.path.join("sound", "splat.mp3"))
]
pygame.mixer.music.load(os.path.join("sound", "Space Ambience.mp3"))
pygame.mixer.music.set_volume(0.4)
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow.mp3"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow.mp3"))

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(backyground_img, (0,0))
    draw_text(screen, 'Riseman', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '<- and -> to move the person - Space Bar for shooting', 20, WIDTH/2, HEIGHT/2)
    draw_text(screen, 'Press any key to Start', 15, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 78))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 10
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
            if self.gun > 1 and pygame.time.get_ticks() - self.gun_time > 5000:
                self.gun -= 1
                self.gun_time = pygame.time.get_ticks()

            if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
                self.hidden = False
                self.rect.centerx = WIDTH /2
                self.rect.bottom = HEIGHT - 10

            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RIGHT]:
                self.rect.x += 5
            if key_pressed[pygame.K_LEFT]:
                self.rect.x -= 5

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet) 
                bullet_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)  
                bullet_sound.play()

    
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(tier1_img)
        self.image_original = pygame.transform.scale(self.image_original, (50, 55))
        self.image_original.set_colorkey(WHITE)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
            self.rotate()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(2, 10)
                self.speedx = random.randrange(-3, 3)    

class Rock2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(tier2_img)
        self.image_original = pygame.transform.scale(self.image_original, (60, 55))
        self.image_original.set_colorkey(WHITE)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
            self.rotate()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(2, 10)
                self.speedx = random.randrange(-3, 3)    

class Rock3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(tier3_img)
        self.image_original = pygame.transform.scale(self.image_original, (70, 55))
        self.image_original.set_colorkey(WHITE)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
            self.rotate()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(2, 10)
                self.speedx = random.randrange(-3, 3)    

class Rock4(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(tier4_img)
        self.image_original = pygame.transform.scale(self.image_original, (80, 55))
        self.image_original.set_colorkey(WHITE)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
            self.rotate()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(2, 10)
                self.speedx = random.randrange(-3, 3)    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (50, 38))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30

    def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(explosion_animation[self.size]):
                    self.kill()
                else:
                    self.image = explosion_animation[self.size][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image = pygame.transform.scale(self.image, (50, 38))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.kill()

pygame.mixer.music.play(-1)

#game loop
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        boss = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
        for i in range(8):
            if(score < 100):
                r = Rock()
                all_sprites.add(r)
                rocks.add(r)
            elif(score > 100):
                r = Rock2()
                all_sprites.add(r)
                rocks.add(r)


    clock.tick(FPS)
    #get input
    for event in pygame.event.get(): #receive the list of input from mouse and keyboard and each is an event
        if event.type == pygame.QUIT:
            running = False #jump out of the game loop when input to quit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update game
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(explosion_sounds).play()
        score += int(hit.radius)
        explosion = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explosion)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        if(score < 1000):
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)
        elif((score > 1000) and (score <= 2000)):
            player.image = player2_img
            r = Rock2()
            all_sprites.add(r)
            rocks.add(r)
        elif((score > 2000) and (score <= 3000)):
            player.image = player3_img
            r = Rock3()
            all_sprites.add(r)
            rocks.add(r)
        elif((score > 3000)):
            player.image = player4_img
            r = Rock4()
            all_sprites.add(r)
            rocks.add(r)             


    
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        random.choice(explosion_sounds).play()
        player.health -= hit.radius
        explosion = Explosion(hit.rect.center, 'sm')
        all_sprites.add(explosion)
        if(score < 1000):
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)
        elif((score > 1000) and (score <= 2000)):
            player.image = player2_img
            r = Rock2()
            all_sprites.add(r)
            rocks.add(r)
        elif((score > 2000) and (score <= 3000)):
            player.image = player3_img
            r = Rock3()
            all_sprites.add(r)
            rocks.add(r)
        elif((score > 3000)):
            player.image = player4_img
            r = Rock4()
            all_sprites.add(r)
            rocks.add(r)       
        if player.health <= 0:
            death = Explosion(player.rect.center, 'py')
            all_sprites.add(death)
            death_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    #support item
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()
        
    if player.lives == 0 and not(death.alive()):
        show_init = True

    #screen showing
    screen.fill((WHITE))
    all_sprites.draw(screen)
    draw_health(screen, player.health, 5, 15)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_lives(screen, player.lives, mini_img, WIDTH - 100, 15)
    pygame.display.update()

pygame.quit()
