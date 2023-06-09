from pygame import *
from random import randint
from time import time as tm

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, sizeX, sizeY, speed=0):
        super().__init__()
        self.img = transform.scale(image.load(img), (sizeX, sizeY))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        mw.blit(self.img, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, img, sizeX, sizeY, speed=0, id=0):
        if id == 1: 
            super().__init__(img, 15, maxY - sizeY, sizeX, sizeY, speed)
        else:
             super().__init__(img, maxX - sizeX - 15, maxY - sizeY, sizeX, sizeY, speed)
        self.id = id       
    def keyProcessing(self):
        keys = key.get_pressed()
        if self.id == 2:
            if keys[K_UP]:
                self.rect.y -= self.speed
            if keys[K_DOWN]:
                self.rect.y += self.speed
        else:
            if keys[K_w]:
                self.rect.y -= self.speed
            if keys[K_s]:
                self.rect.y += self.speed
        #self.rect.x *= (self.rect.x + 1 + abs(self.rect.x +1)) / ((self.rect.x +1)* 2)
        #self.rect.x = (self.rect.x // (maxX - self.rect.width)) * (maxX - self.rect.width) + (self.rect.x %  (maxX - self.rect.width)) * (1 - (self.rect.x // (maxX - self.rect.width)))
        if self.rect.y > (maxY - self.rect.height):
            self.rect.y = (maxY - self.rect.height)
        elif self.rect.y < 0:
            self.rect.y = 0

class Ball(GameSprite):
    def __init__(self, img, x, y, sizeX, sizeY, speed):
        super().__init__(img, x, y, sizeX, sizeY, speed)
        self.speedX = (1 - 2 * (randint(0, 1))) * speed
        self.speedY = (1 - 2 * (randint(0, 1))) * speed
    def move(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        if self.rect.y <= 0:
            self.speedY *= -1
            return 3
        if self.rect.y >= maxY - self.rect.height:
            self.speedY *= -1
            return 4
        if self.rect.x <= 0:
            self.speedX *= -1
            return 1
        if self.rect.x >= maxX - self.rect.width:
            self.speedX *= -1
            return 2
        return 0

bgColor = (255, 255, 255)
maxX = 1280
maxY = 720
selfPrevShotTime = tm()
mw = display.set_mode((maxX, maxY))
display.set_caption('PINGPONG')

mixer.init()#инициализировать микшер
#mixer.music.load('space.ogg')#загрузить фоновую музыку
#mixer.music.play()#начать воспроизведение фоновой музыки
fire = mixer.Sound('ppfire.ogg')#загрузить звук выстрела

game = False
clock = time.Clock()
playerL1 = Player('Plt1.png', 25, 100, 5, 1)
playerR2 = Player('Plt2.png', 25, 100, 5, 2)
ball = Ball('Ball.png', (maxX - 35)//2, (maxY - 35)//2, 35, 35, 5)

font.init()
font_ = font.SysFont('Arial', 50)

victoryL = font_.render('Player 1 WON', True, (255, 0, 0))
victoryR = font_.render('Player 2 WON', True, (255, 0, 0))

gameRes = 0
while game != True:
    keys = key.get_pressed()
    if keys[K_SPACE]:
        game = True
    for e in event.get():
        if e.type == QUIT:
            game = False
while game:
    if gameRes == 0:
        mw.fill(bgColor)
        playerL1.keyProcessing()         
        playerL1.reset()
        playerR2.keyProcessing()         
        playerR2.reset()
        gameRes = ball.move()
        if gameRes > 2:
            gameRes = 0
        if sprite.collide_rect(ball, playerL1) or sprite.collide_rect(ball, playerR2):
            ball.speedX *= -1
            fire.play()
        ball.reset()
    elif gameRes == 1:
        mw.blit(victoryL, (maxX//2, maxY//2))
    elif gameRes == 2:
        mw.blit(victoryR, (maxX//2, maxY//2))
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(50)