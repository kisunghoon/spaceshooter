#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tasdik
# @Contributers : Branden (Github: @bardlean86)
# @Date:   2016-01-17
# @Email:  prodicus@outlook.com  Github: @tasdikrahman
# @Last Modified by:   tasdik
# @Last Modified by:   Branden
# @Last Modified by:   Dic3
# @Last Modified time: 2016-10-16
# MIT License. You can find a copy of the License @ http://prodicus.mit-license.org

## Game music Attribution
##Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

## Additional assets by: Branden M. Ardelean (Github: @bardlean86)

from __future__ import division
import pygame
import random
import time
import math 
import pymysql
from os import path

## assets folder

##경로를 병합하여 새로운 경로 생성
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

###############################
## to be placed in "constant.py" later
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
###############################

###############################
## to placed in "__init__.py" later
## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
pygame.mixer.pre_init(44100,-16,2,512)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()     ## For syncing the FPS
###############################

font_name = pygame.font.match_font('arial')
db_final_score=0
def main_menu():
    global screen
    menu_song = pygame.mixer.Sound(path.join(sound_folder, 'menu.ogg'))
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    menu_song.play(-1)
    title = pygame.image.load(path.join(img_dir, "main.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
    screen.blit(title, (0,0))
    pygame.display.update()
    global volume
    volume = 1

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
            elif ev.key == pygame.K_u:
                if(volume>0.99):
                    volume = 1
                    menu_song.set_volume(volume)
                    ready.set_volume(volume)
                else:
                    volume +=0.1
                    menu_song.set_volume(volume)
                    ready.set_volume(volume)
            elif ev.key == pygame.K_d:
                if(volume<0.11):
                    volume = 0.1
                    menu_song.set_volume(volume)
                    ready.set_volume(volume)
                else:
                    volume -=0.1
                    menu_song.set_volume(volume)
                    ready.set_volume(volume)
            elif ev.key == pygame.K_h:  # H를 누르면 도움말 image를 띄워준다
                title = pygame.image.load(path.join(img_dir, "keyboard_img.png")).convert()
                title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
                screen.blit(title, (0,0))
                pygame.display.flip()
                clock.tick(60)
                while True:  # 다시 H를 눌러야 도움말 화면에서 빠져나올 수 있다.
                    ev2 = pygame.event.wait()
                    if ev2.type == pygame.KEYDOWN and ev2.key == pygame.K_h:
                        break
                title = pygame.image.load(path.join(img_dir, "main.png")).convert()  # 다시 main 이미지를 띄워준다
                title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
                screen.blit(title, (0,0))
                pygame.display.flip()
                clock.tick(60)
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "or [Q] To Quit , H]] To Help", 20, WIDTH/2, (HEIGHT/2)+40)
            draw_text(screen, "[U] To Sounds Up , [D] To Sounds Down", 20, WIDTH/2, (HEIGHT/2)+80)

            pygame.display.update()

    #pygame.mixer.music.stop()
    ready.play()
    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH/2, HEIGHT/2)
    menu_song.stop()
    pygame.display.update()


def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    pct = max(pct, 0) 
    ## moving them to top
    # BAR_LENGTH = 100
    # BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

def db(final_score):
    sss = final_score
    conn = pymysql.connect(host="localhost",user="root",password="sunghoon12",db="db",charset="utf8")
    curs = conn.cursor()

    sql= """
    insert into score(no) 
    values (%s)
    """
    curs.execute(sql,sss)
    conn.commit()
    print("db 연결 성공")
    

    sql2 = "select MAX(no) from score"
    
    curs.execute(sql2)
    rows = curs.fetchall()
    db_final_score = rows   
    list_score=list(db_final_score)
    print(type(list_score))
    print("최고점수",list_score)

    conn.close()
    return list_score

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.power_time = pygame.time.get_ticks()
        self.speedx = 0 
        self.speedy=0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
        self.is_shadow = False  # 그림자 분신술을 쓰고 있는 상태인지에 대한 변수
        self.power_overwhelm_flag = 0   # 무적 상태인 지를 체크하는 flag 변수. 초기값 0.
        self.power_overwhelm_time = pygame.time.get_ticks()  # 가장 최근 무적 상태가 된 time.

    def update(self):
        ## time out for powerups
        if score > 0:
            self.image = pygame.transform.scale(player_img, (50, 38)) 
            self.image.set_colorkey(BLACK)          
        if score > 1000:
            self.image = pygame.transform.scale(player_img2, (50, 38))
            self.image.set_colorkey(BLACK)  
        if score > 2000:
            self.image = pygame.transform.scale(player_img3, (50, 38))
            self.image.set_colorkey(BLACK) 

        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        ## time out for power_overwhelm  # 무적 상태는 10초만 유지하게 한다.
        if self.power_overwhelm_flag == 1 and pygame.time.get_ticks() - self.power_overwhelm_time > 10000:
            self.power_overwhelm_flag = 0
            self.power_overwhelm_time = pygame.time.get_ticks()
            self.image = pygame.transform.scale(player_img, (50, 38))
            self.image.set_colorkey(BLACK)

        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0
        self.speedy = 0     ## makes the player static in the screen by default. 
        # then we have to check whether there is an event hanlding being done for the arrow keys being 
        ## pressed 

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5

        #Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()

            
        ## check for the borders at the left and right
        if self.is_shadow == False:
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT-10:
                self.rect.bottom = HEIGHT-10
        else:
            if self.rect.right > WIDTH + 80:
                self.rect.right = WIDTH + 80
            if self.rect.left < -40:
                self.rect.left = -40
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT-10:
                self.rect.bottom = HEIGHT-10            

        self.rect.x += self.speedx  # speedx, speedy만큼 플레이어의 위치를 이동시킨다.
        self.rect.y += self.speedy
        
    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.set_volume(volume)
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.set_volume(volume)
                shooting_sound.play()

            """ MOAR POWAH """
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top) # Missile shoots from center of ship
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.set_volume(volume)
                shooting_sound.play()
                missile_sound.set_volume(volume)
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def liveup(self):
        self.lives +=1
        

    def power_overwhelm(self):   ## 무적 상태로 만든다. 체력을 100으로 만들고 비행기 이미지가 커진다. 
        self.shield = 100
        self.power_overwhelm_flag = 1
        self.image = pygame.transform.scale(player_img, (75, 57))
        self.image.set_colorkey(BLACK)
        self.power_overwhelm_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2 - 50, HEIGHT + 200)


# defines the enemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)        ## for randomizing the speed of the Mob
        
        ## randomize the movements a little more 
        self.speedx = random.randrange(-3, 3)

        ## adding rotation to the mob element
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ## now what if the mob element goes out of the screen

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)        ## for randomizing the speed of the Mob

## defines the sprite for Powerups
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)

        self.type = random.choice(['shield', 'gun','lives'])
        self.random_k = random.randrange(0, 100)
        if self.random_k >= 70: # 30% 확률의 확률로 무적 아이템 혹은 분신술 아이템으로 바뀐다.
            self.type = random.choice(['power_overwhelm', 'star'])

        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.center = center
        self.speedy = 2

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.top > HEIGHT:
            self.kill()

            

## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy

        ## kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()

        ## now we need a way to shoot
        ## lets bind it to "spacebar".
        ## adding an event for it in Game loop

## FIRE ZE MISSILES
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


###################################################
## Load all game images

background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
## ^^ draw this rect first 

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_img2 = pygame.image.load(path.join(img_dir, 'playerShip1_orange2.png')).convert()
player_img3 = pygame.image.load(path.join(img_dir, 'playerShip1_orange3.png')).convert()

life = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert_alpha()
# meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, image)).convert())

## meteor explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    ## resize the explosion
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    ## player explosion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

## load power ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['lives'] = pygame.image.load(path.join(img_dir, 'life_gold.png')).convert()
powerup_images['power_overwhelm'] = pygame.image.load(path.join(img_dir, 'power_overwhelm.png')).convert_alpha()
powerup_images['star'] = pygame.image.load(path.join(img_dir, 'star.png')).convert_alpha()
###################################################


###################################################
### Load all game sounds
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl3_sound = pygame.mixer.Sound(path.join(sound_folder, 'expl3.wav'))
expl6_sound = pygame.mixer.Sound(path.join(sound_folder, 'expl6.wav'))
## main background music
#pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.2)      ## simmered the sound down a little

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
###################################################

## TODO: make the game music loop over again and again. play(loops=-1) is not working
# Error : 
# TypeError: play() takes no keyword arguments
#pygame.mixer.music.play()
    
def GameOver():
    screen.fill(BLACK)
    draw_text(screen, "GameOver!", 40, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Best Score!", 20, 110, 30)
    draw_text(screen, str(final_score), 30, WIDTH / 2, 25)  

    pygame.display.update()

#############################
## Game loop
player_shadow_run = False
running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)

        #Stop menu music
        pygame.mixer.music.stop()
        #Play the gameplay music
        gamesound = pygame.mixer.Sound(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        gamesound.set_volume(volume)
        gamesound.play(-1)    ## makes the gameplay sound in an endless loop
        menu_display = False
        
        ## group all the sprites together for ease of update
        all_sprites = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        ## spawn a group of mob
        mobs = pygame.sprite.Group()
        for i in range(8):      ## 8 mobs
            # mob_element = Mob()
            # all_sprites.add(mob_element)
            # mobs.add(mob_element)
            newmob()

        ## group for bullets
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        #### Score board variable
        score = 0
        final_score=0
    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB: ###  BACKQUOTE `를 누르면 게임이 일시정지되고, 
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:  ## 다시 '를 눌러야 일시정지가 풀린다.
                        break
        # ## event for shooting the bullets
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()      ## we have to define the shoot()  function

    #2 Update
    all_sprites.update()


    ## check if a bullet hit a mob
    ## now we have a group of bullets and a group of mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    ## now as we delete the mob element when we hit one with a bullet, we need to respawn them again
    ## as there will be no mob_elements left out 
    for hit in hits:
        score += 60 - hit.radius         ## give different scores for hitting big and small metoers
        expl3_sound.set_volume(volume)
        expl6_sound.set_volume(volume)
        sounds = [expl3_sound,expl6_sound]
        random.choice(sounds).play()
        # m = Mob()
        # all_sprites.add(m)
        # mobs.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()        ## spawn a new mob

    ## ^^ the above loop will create the amount of mob objects which were killed spawn again
    #########################

    
    ## check if the player collides with the mob
    
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)        ## gives back a list, True makes the mob element disappear
    for hit in hits:
        if player.power_overwhelm_flag == 0: #무적 상태가 아닐 때만 체력이 깎인다
            player.shield -= hit.radius * 2   # 플레이어의 체력이 hit.radius의 2배만큼 깎인다.
            expl = Explosion(hit.rect.center, 'sm')  # explosion 클래스의 객체 expl을 만든다. (작은 폭발이 일어난다)
            all_sprites.add(expl)   # Sprite 그룹에 expl을 추가한다
        newmob()
        if player.shield <= 0: 
            player_die_sound.set_volume(volume)
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            if player_shadow_run == True: # 본 캐릭터 비행기가 죽으면 분신술 비행기도 같이 죽는다
                player_shadow_run = False  ## 분신술 숨기고
                player11.kill()  ## 왼쪽 분신술 비행기 객체를 없애고
                player12.kill()  ## 오른쪽 분신술 비행기 객체를 없앤다.
            # running = False     ## GAME OVER 3:D
            player.hide()
            player.lives -= 1
            player.shield = 100

    ## if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
        if hit.type == 'power_overwhelm':  # 무적 아이템을 먹었다면 power_overwhelm() 함수를 호출한다.
            player.power_overwhelm()  
        if hit.type =='lives':
            player.liveup()
        if hit.type == 'star' and player_shadow_run == False:  # 별 아이템(분신술 스킬)을 먹었을 때, 
            player_shadow_run = True
            player_shadow_start_time = pygame.time.get_ticks()
            player11 = Player()
            player11.is_shadow = True
            player11.rect.centerx = player.rect.centerx - 40  ## 왼쪽 분신술 비행기의 좌표 재지정.
            player11.rect.bottom = player.rect.bottom
            player11.power = player.power
            all_sprites.add(player11)
            player12 = Player()
            player12.is_shadow = True
            player12.rect.centerx = player.rect.centerx + 60 ## 오른쪽 분신술 비행기의 좌표 재지정.
            player12.rect.bottom = player.rect.bottom
            player12.power = player.power
            all_sprites.add(player12)
    
    if player == True and player_shadow_run == True:  ## 현재 1P가 분신술을 쓰고 있다면
        if pygame.time.get_ticks() - player_shadow_start_time > 10000: ## 분신술은 10초동안 상태를 유지한다.
            player_shadow_run = False  
            player11.kill()
            player12.kill() 
        else:
            player11.rect.centerx = player.rect.centerx - 40  
            player11.rect.bottom = player.rect.bottom
            player12.rect.centerx = player.rect.centerx + 60
            player12.rect.bottom = player.rect.bottom
            all_sprites.add(player11)
            all_sprites.add(player12)


    ## if player died and the explosion has finished, end game
    if player.lives == 0 and not death_explosion.alive():

        ## running = False
        
        final_score = score
        final_score= db(final_score)
        ## print((db_final_score))
        GameOver()  
        time.sleep(2)
        pygame.display.update()
        gamesound.stop()
        menu_display = True


    #3 Draw/render
    screen.fill(BLACK)
    ## draw the stargaze.png image
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)     ## 10px down from the screen
    draw_text(screen, "HP : "+str(player.shield), 18, WIDTH / 8, 20) ## HP추가
    draw_shield_bar(screen, 5, 5, player.shield)

    # Draw lives
    draw_lives(screen, WIDTH - 477, 575, player.lives, player_mini_img)

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()