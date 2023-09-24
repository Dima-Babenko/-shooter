from pygame import *
from random import randint
import time as t

init()

mixer.music.load("музика/шум.ogg")
mixer.music.play(-1)

fire_sound1 = mixer.Sound("музика/fire.ogg")

win_width = 700
win_height = 500

win = display.set_mode((win_width, win_height))
display.set_caption("Shooter")

background = transform.scale(image.load("картинки/фон.jpg"), (win_width, win_height))
clock = time.Clock()

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.reload = 0
        self.rate = 15

    def update(self):
        keys1 = key.get_pressed()
        if keys1[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys1[K_RIGHT] and self.rect.x < win_width - 90:
            self.rect.x += self.speed
        if keys1[K_SPACE] and self.reload >= self.rate:
            fire_sound1.play()
            self.fire()
            self.reload = 0
        elif self.reload < self.rate:
            self.reload += 1
    
    def fire(self):
        bul = Bullet("картинки/герб.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bul)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            lost += 1
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

ship = Player("картинки/танк.png", 5, win_height - 100, 80, 100, 7)

finish = False
run = True
FPS = 60

bullets = sprite.Group()

f1 = font.Font(None, 36)
f2 = font.Font(None, 72)
f3 = font.Font(None, 50)

start_time = t.time()

monsters = sprite.Group()
for i in range(5):
    x = randint(80, win_width - 80)
    speed = randint(1, 2)
    monster = Enemy("картинки/орк.png", x, -40, 80, 50, speed)
    monsters.add(monster)

while run:
    current_time = t.time()
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        
        win.blit(background, (0, 0))

        text_score = f1.render(f"рахунок: {score}", True, (255, 255, 255))
        win.blit(text_score,(10, 20))

        text_lost = f1.render(f"пропущено: {lost}", True, (255, 255, 255))
        win.blit(text_lost,(10, 50))

    

        monsters.update()
        bullets.update()

        ship.update()
        ship.reset()
        monsters.draw(win)
        bullets.draw(win)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            x = randint(80, win_width - 80)
            speed = randint(1, 2)
            monster = Enemy("картинки/орк.png", x, -40, 80, 50, speed)
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or lost >= 10:
            finish = True
            lose = f3.render("Не переживай, в грі ще багато раундів!", True, (200, 50, 50))
            win.blit(lose, (10, 200))

        if score >= 30:
            finish = True
            won = f2.render("вінер, вінер!", True, (255, 150, 0))
            win.blit(won, (200, 200))

    display.update()
    clock.tick(FPS)