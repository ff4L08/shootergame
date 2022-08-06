from pygame import*
from random import*

#mixer.init()
#mixer.music.load("jungle.ogg")
#mixer.music.play
#fire_sound = mixer.Sound('fire.ogg')
img_back = 'background.png'
img_hero = 'spaceship.png'
img_enemy = 'enemy2.png'
playerScore = 0

class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
    
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image).convert_alpha(), (size_x, size_y))
        self.speed = Vector2(player_speed)

        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #method drawing the character on the window
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed.x

        if keys[K_RIGHT] and self.rect.x < WIN_WIDTH - 80:
            self.rect.x += self.speed.x
    
class TextSprite(sprite.Sprite):
    def __init__(self, text, color, pos, font_size):
        self.font = font.Font(None, font_size)
        self.color = color
        self.pos = pos
        self.update_text(text)
        self.rect = self.image.get_rect()
    def update_text(self, new_text):
        self.image = self.font.render(new_text,True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Bullet(GameSprite):
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Boomerang(GameSprite):
    def update(self):
        self.rect.topleft += self.speed
        self.speed.x += 1
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.top > WIN_HEIGHT or self.rect.left > WIN_WIDTH:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed.y
        if self.rect.top > WIN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIN_WIDTH-(self.rect.width))

def fire():
    b = Bullet("spaceship.png", ship.rect.centerx - 8, ship.rect.centery-30, 16, 70, (0,-15))
    bullets.add(b)

def fireBoomer():
    b = Boomerang("spaceship.png", ship.rect.centerx - 8, ship.rect.centery-30, 16, 70, (-25,-15))
    bullets.add(b)
    
font.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 800
playerScoreText = TextSprite(text = "Score: 0", color = "white" , pos = (20,20), font_size = 40)
finishTextWin = TextSprite(text = 'You Win!!', color = 'green' , pos = (0, 0), font_size = 200)
finishTextWin.rect.center = (WIN_WIDTH/2, WIN_HEIGHT/2)
finishTextLose = TextSprite(text = 'You Lose!!', color = 'red' , pos = (0, 0), font_size = 200)
finishTextLose.rect.center = (WIN_WIDTH/2, WIN_HEIGHT/2)
display.set_caption('shooter')
window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
background = transform.scale(image.load(img_back), (WIN_WIDTH, WIN_HEIGHT))
bullets = sprite.Group()
ship = Player(img_hero, 5, WIN_HEIGHT - 190, 80, 190, 10)
enemies = sprite.Group()
for _ in range(10):
    e1 = Enemy(img_enemy, randint(0, WIN_WIDTH-30), WIN_HEIGHT - 0, 80, 80, randint(1,2))
    enemies.add(e1)

finish = False
run = True
clock = time.Clock()

while run:
    for ev in event.get():
        if ev.type == QUIT:
            run = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                fire()
            if ev.key == K_z:
                fireBoomer()
    if not finish:
        window.blit(background, (0, 0))
        
        bullets.update()
        enemies.update()
        ship.update()
        
        hits = sprite.groupcollide(enemies, bullets, True, False)
        for hit in hits:
            e1 = Enemy(img_enemy, randint(0, WIN_WIDTH-30), WIN_HEIGHT - 0, 80, 80, randint(1,2))
            enemies.add(e1)
            playerScore += 200
            playerScoreText.update_text("Score: " + str(playerScore))
            

        playerCollide = sprite.spritecollide(ship, enemies, True)
        for collide in playerCollide:
            e1 = Enemy(img_enemy, randint(0, WIN_WIDTH-30), WIN_HEIGHT - 0, 80, 80, randint(1,2))
            enemies.add(e1)
            playerScore -= 5000
            playerScoreText.update_text("Score: " + str(playerScore))

        
        
        playerScoreText.draw(window)
        bullets.draw(window)
        enemies.draw(window)
        ship.draw(window)

        if playerScore >= 15000:
            finish = True
            finishTextWin.draw(window)
        
        # if playerScore < 0:
        #     finish = True
        #     finishTextLose.draw(window)
        
        display.update()
    

    clock.tick(60)