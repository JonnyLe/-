#飞机大战

import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import time
import random

#飞机类
class Baseplane(object):
    def __init__(self,x,y,load,speed,name):
        planeImageFile = load  #读取图片存储位置
        self.speed = speed
        self.image = pygame.image.load(planeImageFile).convert()
        self.X = x
        self.Y = y
        self.name = name
        self.bullt = []
        
        self.hit = False #表示是否要爆炸
        self.bomb_list = [] #用来存储爆炸时需要的图片
        self.crate_images() #调用这个方法向bomb_list中添加图片
        self.image_num = 0#用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0#用来记录当前要显示的爆炸效果的图片的序号
        self.endImage = pygame.image.load('bomb.png').convert()
    #添加爆炸图片
    def crate_images(self):
       pass
    def display(self,screen,Baseplane):
        """显示玩家的飞机"""
        #如果被击中,就显示爆炸效果,否则显示普通的飞机效果
        if self.hit == True:
            screen.blit(self.bomb_list[self.image_index], (self.X, self.Y))
            self.image_num+=1
            if self.image_num == 7:
                self.image_num=0
                self.image_index +=1
            if self.image_index>3:
                screen.blit(self.endImage,(145, 230))
                time.sleep(1)
                exit()#调用exit让游戏退出
                #self.image_index = 0
        else:
            screen.blit(self.image,(self.X, self.Y))
         # 不管玩家飞机是否被击中,都要显示发射出去的子弹
        for bullet in self.bullt:
            bullet.draw(screen)
            if bullet.boom_judge(screen,Baseplane):
                self.bullt.remove(bullet)
    #绘制飞机，并且绘制出对应的子弹
    def draw(self,screen,Baseplane):
        screen.blit(self.image,(self.X,self.Y))
        for bullts in self.bullt:
            bullts.draw(screen)
            if bullts.boom_judge(screen,Baseplane):
                self.bullt.remove(bullts)
            if bullts.judge(self.name):#判断飞机释放的子弹是否越界
                self.bullt.remove(bullts)
    #绘制飞机移动方法
    def move(self,dirction):
        pass
    def bomb(self):
        self.hit = True        
        
#玩家飞机类
class plane(Baseplane):
    def __init__(self,x,y,load,speed,name):
        super().__init__(x,y,load,speed,name)
        self.buttle = []#设置子弹个数
        
    def crate_images(self):
        self.bomb_list.append(pygame.image.load("hero_blowup_n1.png"))
        self.bomb_list.append(pygame.image.load("hero_blowup_n2.png"))
        self.bomb_list.append(pygame.image.load("hero_blowup_n3.png"))
        self.bomb_list.append(pygame.image.load("hero_blowup_n4.png"))
    #飞机移动    
    def move(self,dirction):
        if dirction =='LEFT' and self.X >= -50:
            self.X = self.X - self.speed
        elif dirction =='RIGHT' and self.X <= 360:
            self.X = self.X + self.speed
        elif dirction == 'SPACE':
            print('---------FIRE BOOOM--------')
            self.bullt.append(playerShell(self.X+43,self.Y-18,'bullet-3.gif',int(51),int(39)))
            
    
    

#敌机类
class enemy_plane(Baseplane):
    def __init__(self,x,y,load,speed,name):
        super().__init__(x,y,load,speed,name,)
        self.dirction = 'R'
    def crate_images(self):
        self.bomb_list.append(pygame.image.load("enemy0_down1.png"))
        self.bomb_list.append(pygame.image.load("enemy0_down2.png"))
        self.bomb_list.append(pygame.image.load("enemy0_down3.png"))
        self.bomb_list.append(pygame.image.load("enemy0_down4.png"))   
    def move(self):
        if self.dirction == 'R':
            self.X = self.X + self.speed
            if self.X >= 320:
                self.dirction = 'L'
        elif self.dirction == 'L':
            self.X = self.X - self.speed
            if self.X <= -45:
                self.dirction = 'R'
        randomNum = random.randint(1,100)
        if randomNum in [50]:
            self.bullt.append(enemyShell(self.X+25,self.Y+39,'bullet-1.gif',int(100),int(124)))

#子弹类     
class shells(object):
    def __init__(self,x,y,shell_File,sizex,sizey):
        shell_File = shell_File
        self.image = pygame.image.load(shell_File).convert()
        self.X = x
        self.Y = y
        self.boomimage = []
        self.sizeX = sizex
        self.sizeY = sizey
    def draw_blit(self,screen):
        screen.blit(self.image,(self.X,self.Y))
    def judge(self,flag):
        if flag == 'player':
            if self.Y  < 0:
                return True
            else:
                return False
        elif flag == 'enemy':
            if self.Y > 480:
                return True
            else:
                return False
    #判断是否炸毁：
    def boom_judge(self,screen,Baseplane):
        if (Baseplane.X<self.X) and (Baseplane.X+self.sizeX>self.X) and (Baseplane.Y<self.Y)and(Baseplane.Y+self.sizeY>self.Y):
            Baseplane.bomb()
            return True
    
class playerShell(shells):
    def __init__(self,x,y,shell_File,sizex,sizey):
        super().__init__(x,y,shell_File,sizex,sizey)
        self.boomimage =['enemy0_down1.png','enemy0_down2.png','enemy0_down3.png','enemy0_down4.png'] 
    def draw(self,screen):
        self.Y = self.Y-1
        self.draw_blit(screen)
        
    
class enemyShell(shells):
    def __init__(self,x,y,shell_File,sizex,sizey):
        super().__init__(x,y,shell_File,sizex,sizey)
        self.boomimage = ['hero_blowup_n1.png','hero_blowup_n2.png','hero_blowup_n3.png','hero_blowup_n4.png']
    def draw(self,screen):
        self.Y = self.Y+1
        self.draw_blit(screen)
        
def main():    
    screen = pygame.display.set_mode((320,480),0,32)
    bgimageFile = 'timg.png'
    background = pygame.image.load(bgimageFile).convert()
    
    #创建玩家飞机对象
    plane_load = 'hero.gif'
    player = plane(30,400,plane_load,int(8),'player')
    #创建敌机对象和运动行为
    enemy_load = 'enemy-1.gif'
    enemy = enemy_plane(0,40,enemy_load,int(2),'enemy')
    
    #更新界面
    while True:
        screen.blit(background,(0,0))
        #读取键盘扫描数据
        for event in GAME_EVENTS.get():
            if event.type == GAME_GLOBALS.QUIT:
                print('QUIT!')
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    print('LEFT!')
                    player.move('LEFT')
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    print('RIGHT!')
                    player.move('RIGHT')
                elif event.key == pygame.K_SPACE:
                    print('SPACE!')
                    player.move('SPACE')

        enemy.move()            
#        enemy.draw(screen,player)
#        player.draw(screen,enemy)
        enemy.display(screen,player)
        player.display(screen,enemy)
        pygame.display.update()
        #控制CPU的运行，避免因为死死循环造成CPU占用率过高
        time.sleep(0.01)
    
        
if __name__ == '__main__':
    main() 
