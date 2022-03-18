#Little wizard
FPS=60
WIDTH=700
HEIGHT=800

WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)
import pygame
import random
import os
#遊戲初始化&創建視窗
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Little wizard")
clock=pygame.time.Clock()
#載入圖片
background_img=pygame.image.load(os.path.join("img","background.png")).convert()
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
enemy_img=pygame.image.load(os.path.join("img","enemy.png")).convert()
fireball_img=pygame.image.load(os.path.join("img","fireball.png")).convert()
firebreath_img=pygame.image.load(os.path.join("img","firebreath.png")).convert()
icon_img=pygame.transform.scale(player_img,(50,40))
pygame.display.set_icon(icon_img)
#載入字體
font_name=os.path.join("font.ttf")
#載入音效
fireball_sound=pygame.mixer.Sound(os.path.join("sound","fireball.sound.wav"))
pygame.mixer.music.load(os.path.join("sound","bgm.mp3"))
pygame.mixer.music.play(-1)

#分數顯示
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)
def new_enemy():
    e=Enemy()
    all_sprite.add(e)
    enemys.add(e)
def draw_heealth(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGTH=200
    BAR_HEIGHT=20
    fill=(hp/100)*BAR_LENGTH
    outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)
def draw_init():
    screen.blit(background_img,(0,0))
    draw_text(screen,"Little wizard",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"W,A,S,D移動 空白鍵攻擊",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"按任意鍵開始遊戲~生命為0時遊戲結束",18,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)   
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                return True
            elif event.type==pygame.KEYUP:
                waiting=False
                return False
    


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(80,100))
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius=30
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-10
        self.speedx=9
        self.speedy=9
        self.health=99
        self.fire_lv=1
        self.breath_time=0
        
    def update(self):
        now=pygame.time.get_ticks()
        if self.fire_lv>=2 and now-self.breath_time>2000:
            self.fire_lv-=1
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x-=self.speedx
        if key_pressed[pygame.K_w]:
            self.rect.y-=self.speedy
        if key_pressed[pygame.K_s]:
            self.rect.y+=self.speedy
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.top<0:
            self.rect.top=0   
        if self.rect.bottom>HEIGHT:
            self.rect.bottom=HEIGHT     
    
    
    def shoot(self):
        if self.fire_lv==1:
            fireball=Fireball(self.rect.centerx,self.rect.top)
            all_sprite.add(fireball)
            fireballs.add(fireball)
            fireball_sound.play()
            pygame.mixer.Sound.set_volume(fireball_sound,1.0)
        elif self.fire_lv>=2:
            firebreath=Firebreath(self.rect.centerx,self.rect.top) 
            all_sprite.add(firebreath)
            firebreaths.add(firebreath)
            fireball_sound.play()
            pygame.mixer.Sound.set_volume(fireball_sound,1.0)
    def lv_up(self):
        self.fire_lv+=1
        self.breath_time=pygame.time.get_ticks()
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(enemy_img,(120,144))
        self.image.set_colorkey(RED)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-150,-100)
        self.speedy=random.randrange(4,7)
        self.speedx=random.randrange(-4,4)

    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>HEIGHT:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-150,-100)
class Fireball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(fireball_img,(40,64))
        self.image.set_colorkey(GREEN)
        self.rect=self.image.get_rect()
        self.radius=17
        self.rect.centerx=x
        self.rect.centery=y
        self.speedy=-12

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()
class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(["breath","heart"])
        self.image=power_imgs[self.type]
        self.image.set_colorkey(GREEN)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.speedy=5
        
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()
class Firebreath(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(firebreath_img,(80,128))
        self.image.set_colorkey(GREEN)
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.speedy=-12

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()
all_sprite=pygame.sprite.Group()
enemys=pygame.sprite.Group()
fireballs=pygame.sprite.Group()
firebreaths=pygame.sprite.Group()
player=Player()
powers=pygame.sprite.Group()
all_sprite.add(player)
score=0
for i in range(10 ):#敵人數量
    new_enemy()            

power_imgs={}
power_imgs["breath"]=pygame.image.load(os.path.join("img","breath.png")).convert()
power_imgs["heart"]=pygame.image.load(os.path.join("img","heart.png")).convert()




#遊戲迴圈
show_init=True
running=True
while running:
    if show_init:
        close=draw_init()
        if close:
            break
        show_init=False
        all_sprite=pygame.sprite.Group()
        enemys=pygame.sprite.Group()
        fireballs=pygame.sprite.Group()
        firebreaths=pygame.sprite.Group()
        player=Player()
        powers=pygame.sprite.Group()
        all_sprite.add(player)
        score=0
        for i in range(10 ):#敵人數量
            new_enemy()  
        
    clock.tick(FPS) 
    #取得輸入
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()
    
    
       
    #更新遊戲
    all_sprite.update()
    hits=pygame.sprite.groupcollide(enemys,fireballs,True,True)#碰撞判定
    for hit in hits:
        score+=1
        if random.random()>0.95:
            pow=Power(hit.rect.center)
            all_sprite.add(pow)
            powers.add(pow)
        new_enemy()
    hits=pygame.sprite.groupcollide(enemys,firebreaths,True,False)
    for hit in hits:
        score+=1
        if random.random()>0.95:
            pow=Power(hit.rect.center)
            all_sprite.add(pow)
            powers.add(pow)
        new_enemy()
    hits=pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)  #人物撞擊死亡
    for hit in hits:
        new_enemy()
        player.health-=33
        if player.health<=0:
            show_init=True
    #寶物，人物相撞
    hits=pygame.sprite.spritecollide(player,powers,True,)
    for hit in hits:
        if hit.type=="heart":
            player.health+=33
            if player.health>99:
                player.health=99
        if hit.type=="breath":
            player.lv_up()
            
            
           

    #畫面顯示
    screen.fill(BLACK)#R,G,B
    screen.blit(background_img,(0,0))
    all_sprite.draw(screen)
    draw_text(screen,str(score),50,WIDTH/2,10)
    draw_heealth(screen,player.health,5,20)
    pygame.display.update() 


pygame.quit()
