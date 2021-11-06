import pygame
from pygame.draw import *
from random import randint

#Считывание списка игроков из файла
file = open('best_players.txt', 'r')
lop = []#lop = list of players
for fline in file:
    for i in range(len(fline)):
        if fline[len(fline)-1-i] == ' ':
            lop.append([fline[0:len(fline)-1-i], int(fline[len(fline)-i:len(fline)-1])])
file.close()
print("Please print your nick: ")
pname = input()

WIDTH = 1200
HEIGHT = 900
FPS = 30
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

ballsOnScreen = 7 #Задаёт количество мячиков на экране
specOnScreen = 2 #FIXIT
time_of_life = 10*FPS
g = 2

points = 0 #Счётчик очков

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

class Target:
    def __init__(self):
        self.r = randint(15, 25)
        self.x = randint(self.r, WIDTH-self.r)
        self.y = randint(self.r, HEIGHT-self.r)
        self.vx = randint(-20, 20)
        self.vy = randint(-20, 20)
        self.ax = 0
        self.ay = 2
        self.color = COLORS[randint(0, 5)]
        self.time = 0
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay
        if self.x < self.r:
            self.x = self.r
            self.vx = abs(self.vx)
        if self.x > WIDTH-self.r:
            self.x = WIDTH-self.r
            self.vx = -abs(self.vx)
        if self.y < self.r:
            self.y = self.r
            self.vy = abs(self.vy)
        if self.y > HEIGHT-self.r:
            self.y = HEIGHT-self.r
            self.vy = -abs(self.vy)
        self.t += 1
    
    def check_death(self):
        if self.t >= time_of_life:
            return True
        else:
            return False
    
    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)

class Bullet:
    def __init__(self, gun):
        self.x = gun.x
        self.y = gun.y
        self.vx = gun.p
        self.vy = ?
        self.ax = 0
        self.ay = 2
        self.color = BLACK
        self.aell = 30
        self.bell = 10
        self.angle = 0
        #self.r = 5
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay
        
    def draw(self):
        subplot = pygame.Surface((self.aell/2,self.bell),pygame.SRCALPHA)
        ellipse(subplot, BLACK, (-self.aell/2,0,self.aell,self.bell))
        subplot = pygame.transform.rotate(subplot, self.angle)
        screen.blit(subplot, (self.x, self.y))
        #circle(screen, BLACK, (self.x, self.y), self.r)
    
    def hittest(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2:
            return True
        else:
            return False

class Gun:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT/2
        self.power = 0
        self.fire = 0
        
    def fire_start(self):
        self.fire = 1
        
    def file_end(self):
        self.fire = 0
    
    def draw(self, mouse):
        subplot = pygame.Surface((self.aell/2,self.bell),pygame.SRCALPHA)
        rect(subplot, BLACK, (self.x, self.y, self.a, self.b), width = 2)
        rect(subplot, BLACK, (self.x, self.y, self.a*self.power, self.b))

gun = Gun()


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Thanks for game! Your score: ", points)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
        elif event.type == pygame.MOUSEBUTTONUP:
            
            
    
    f = pygame.font.Font(None, 36)
    text = f.render('Score:' + str(points), 1, (180, 0, 0))
    screen.blit(text, (250, 20))
    
    pygame.display.update()
    screen.fill(BLACK)

#Запись результатов в файл
file = open('best_players.txt', 'w')
flag = 0
for i in range(len(lop)):
    if lop[i][0] == pname:
        flag = 1
        if lop[i][1] < points:
            lop[i][1] = points
if flag == 0:
    lop.append([pname,points])
lop = sorted(lop, key=lambda a: a[1], reverse=True) 
for i in range(len(lop)):
    file.write(str(lop[i][0])+' '+str(lop[i][1])+'\n')
file.close()
pygame.quit()