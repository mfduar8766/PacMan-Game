import pygame as pg
import random
from Settings2 import *
img_dir = path.join(path.dirname(__file__), 'img')
sndDir = path.join(path.dirname(__file__), 'sound')

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(FONTNAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pg.sprite.Sprite):
    def __init__(self, game, Wall):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.wall = Wall
        self.player_img = pg.image.load(path.join(img_dir, "pm.png")).convert()
        self.player_mini_img = pg.transform.scale(self.player_img, (15, 19))
        self.player_mini_img.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.player_img, (25, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = HEIGHT/2 + 200
        self.rect.y = HEIGHT/2+240
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.movementSpeed = 3
       
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx -= self.movementSpeed
        if keystate[pg.K_RIGHT]:
            self.speedx += self.movementSpeed
        if keystate[pg.K_UP]:
            self.speedy -=self.movementSpeed
        if keystate[pg.K_DOWN]:
            self.speedy +=self.movementSpeed
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.bottom = HEIGHT
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        verticalCollision = pg.sprite.spritecollide(self, self.wall,False)
        for hit in verticalCollision:
            if self.speedy > 0:
                self.rect.bottom = hit.rect.top
            elif self.speedy < 0:
                self.rect.top = hit.rect.bottom 
            self.speedy = 0

        horrizontalCollision = pg.sprite.spritecollide(self, self.wall,False)
        for hit in horrizontalCollision:
            if self.speedx > 0:
                self.rect.right = hit.rect.left
            elif self.speedx < 0:
                self.rect.left = hit.rect.right
            self.speedx = 0
        
    def respawnPlayer(self):
        self.rect.x = HEIGHT/2
        self.rect.y = HEIGHT/2+240

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, height, width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Food(pg.sprite.Sprite):
    def __init__(self, x, y, height, width):
        pg.sprite.Sprite.__init__(self)
        self.foodImg = pg.image.load(path.join(img_dir, "food.png")).convert()
        self.foodMinImg = pg.transform.scale(self.foodImg, (20, 20))
        self.foodMinImg.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.foodImg, (12, 12))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Always follow pacman 
class OrangeGhost(pg.sprite.Sprite):
    def __init__(self, player, wall):
        pg.sprite.Sprite.__init__(self)
        self.pacman = player
        self.wall = wall
        self.player_img = pg.image.load(path.join(img_dir, "ghosr1.png")).convert()
        self.player_mini_img = pg.transform.scale(self.player_img, (35, 35))
        self.player_mini_img.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.player_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = HEIGHT/2 - 15
        self.rect.y = HEIGHT/2 - 42
        self.speedx = 1
        self.speedy = 1
       
    def update(self):
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.bottom = HEIGHT
            self.rect.bottom = HEIGHT
        self.moveTowardsPlayerX()
        self.checkHorrizonatal()
        self.moveToPlayerY()
        self.checkVertical()


    def checkHorrizonatal(self):
        horrizontalCollision = pg.sprite.spritecollide(self, self.wall,False)
        for hit in horrizontalCollision:
            # if self.rect.top > hit.rect.bottom:
            #     self.rect.top += self.speedy
            # if self.rect.bottom > hit.rect.top:
            #     self.rect.bottom -= self.speedy
            # if self.rect.right > hit.rect.left:
            #     self.rect.right -= self.speedx
            # if self.rect.left > self.rect.right:
            #     self.rect.left +=self.speedx
            # elif self.rect.top > hit.rect.bottom and self.rect.right > hit.rect.left:
            #     self.rect.top += self.speedy
            #     self.rect.right -=self.speedx
            # elif self.rect.bottom > hit.rect.top and self.rect.left > hit.rect.right:
            #     self.rect.bottom -= self.speedy
            #     self.rect.left +=self.speedx



            #close
            # if self.rect.right > hit.rect.left and self.rect.top > self.rect.bottom:
            #     self.rect.right -=self.speedx
            #     self.rect.top +=self.speedy
            # if self.rect.left > hit.rect.right and self.rect.bottom > self.rect.top:
            #     self.rect.left +=self.speedx
            #     self.rect.bottom -=self.speedy
             


            # if self.rect.right > hit.rect.left:
            #     self.rect.right -= self.speedx
            # if self.rect.left > self.rect.right:
            #     self.rect.lef += self.speedx
            
    # def checkVertical(self):
    #    verticalCollision = pg.sprite.spritecollide(self, self.wall,False)
    #    for hit in verticalCollision:
    #         if self.rect.top > hit.rect.bottom:
    #             self.rect.top += self.speedy
    #         elif self.rect.bottom > self.rect.top:
    #             self.rect.bottom -= self.speedy
       

    def moveTowardsPlayerX(self):
        if self.rect.x < self.pacman.rect.x:
            self.rect.x += self.speedx
        elif self.rect.x > self.pacman.rect.x:
            self.rect.x -= self.speedx
        return self.speedx
    
    def moveToPlayerY(self):
        if self.rect.y < self.pacman.rect.y:
            self.rect.y += self.speedy
        elif self.rect.y > self.pacman.rect.y:
            self.rect.y -= self.speedy
        return self.speedy

       
class BlueGhost(pg.sprite.Sprite):
    def __init__(self, wall):
        pg.sprite.Sprite.__init__(self)
        self.wall = wall
        self.player_img = pg.image.load(path.join(img_dir, "blueg.png")).convert()
        self.player_mini_img = pg.transform.scale(self.player_img, (35, 35))
        self.player_mini_img.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.player_img, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = HEIGHT/2 - 30
        self.rect.y = HEIGHT/2 - 42
        self.speedx = 1
        self.speedy = 1

    def update(self):
        self.rect.x += random.randrange(3)
        self.rect.y += random.randrange(2)
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.bottom = HEIGHT
        self.checkVertical()
        self.checkHorrizonatal()

    def checkHorrizonatal(self):
        horrizontalCollision = pg.sprite.spritecollide(self, self.wall,False)
        for hit in horrizontalCollision:
            if self.rect.right > hit.rect.left:
                self.rect.right -= self.speedy
            elif self.rect.left > self.rect.right:
                self.rect.lef += self.speedy
            
    def checkVertical(self):
       verticalCollision = pg.sprite.spritecollide(self, self.wall,False)
       for hit in verticalCollision:
            if self.rect.top > hit.rect.bottom:
                self.rect.top += self.speedy
            elif self.rect.bottom > self.rect.top:
                self.rect.bottom -= self.speedy

class RedGhost(pg.sprite.Sprite):
    def __init__(self, wall):
        pg.sprite.Sprite.__init__(self)
        self.wall = wall
        self.player_img = pg.image.load(path.join(img_dir, "ghost3.png")).convert()
        self.player_mini_img = pg.transform.scale(self.player_img, (35, 35))
        self.player_mini_img.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.player_img, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = HEIGHT/2 - 30
        self.rect.y = HEIGHT/2 - 42
        self.speedx = 1
        self.speedy = 1

    def update(self):
        self.rect.x += random.randrange(3)
        self.rect.y += random.randrange(3)
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.bottom = HEIGHT
        self.checkVertical()
        self.checkHorrizonatal()

    def checkHorrizonatal(self):
        horrizontalCollision = pg.sprite.spritecollide(self, self.wall,False)
        for hit in horrizontalCollision:
            if self.rect.right > hit.rect.left:
                self.rect.right -= self.speedy
            elif self.rect.left > self.rect.right:
                self.rect.lef += self.speedy
            
    def checkVertical(self):
       verticalCollision = pg.sprite.spritecollide(self, self.wall,False)
       for hit in verticalCollision:
            if self.rect.top > hit.rect.bottom:
                self.rect.top += self.speedy
            elif self.rect.bottom > self.rect.top:
                self.rect.bottom -= self.speedy
                        
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.wallGroup = pg.sprite.Group()
        # self.foodGroup = pg.sprite.Group()
        self.playerGroup = pg.sprite.Group()
        self.ghostGroup = pg.sprite.Group() 
        self.foodGroup = pg.sprite.Group() 
        self.player = Player(self, self.wallGroup)
        self.ghost1 = RedGhost(self.wallGroup) 
        self.ghost4 = OrangeGhost(self.player, self.wallGroup)
        self.ghost2 = BlueGhost(self.wallGroup)
        self.ghostGroup.add(self.ghost1, self.ghost4, self.ghost2)
        self.playerGroup.add(self.player)
        self.all_sprites.add(self.playerGroup, self.ghostGroup, self.wallGroup)

        for food in FOOD:
            f = Food(*food)
            self.all_sprites.add(f)
            self.foodGroup.add(f)

        for wall in WALL:
            w = Wall(*wall)
            self.all_sprites.add(w)
            self.wallGroup.add(w)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):           
        # Check if player eats food
        self.all_sprites.update()
        hit = pg.sprite.spritecollide(self.player, self.foodGroup, True)
        if hit:
            self.score+=1

        #Ghost gets player
        kill = pg.sprite.spritecollideany(self.player, self.ghostGroup,False)
        if kill:
            self.player.lives -=1
            self.draw_lives(50,5,self.player.lives,self.player.player_mini_img)
            self.player.respawnPlayer()
            if self.player.lives == 0:
                self.new()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                pg.mixer.Sound(path.join(sndDir, 'eating.mp3'))
                pg.mixer.music.load(path.join(sndDir, 'eating.mp3'))
                pg.mixer.music.play()
                pg.mixer.music.set_volume(0.3)
            else:
                pg.mixer.music.stop()
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_lives(30,5,self.player.lives,self.player.player_mini_img)
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.Sound(path.join(sndDir, 'startmusic.mp3'))
        pg.mixer.music.load(path.join(sndDir, 'startmusic.mp3'))
        pg.mixer.music.play()
        draw_text(self.screen, "PAC MAN!", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.waitForKeyPressed()   

    def waitForKeyPressed(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    waiting = False
                    

    def show_go_screen(self):
        self.screen.fill(BLACK)
        draw_text(self.screen, "YOU LOSE", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, str(self.score), 40, 300, 400)
        pg.display.flip()
        self.waitForKeyPressed()  

    def draw_lives(self, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            self.screen.blit(img, img_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    # g.show_go_screen()

pg.quit()



# for h in hit:
#             if self.rect.bottom > h.rect.top:
#                self.speedx = 0
#             if self.rect.top > h.rect.bottom:
#                 self.speedx = 0