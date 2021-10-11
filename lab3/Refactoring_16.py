import pygame
from pygame.draw import *
import pygame.transform as tr
import random

pygame.init()

LIGHTGREY = (200, 200, 200)
BLACK = (0,34,43)
LIGHTCYAN = (224,255,255)
SKYBLUE = (0,204,255)

FPS = 30
screen = pygame.display.set_mode((800, 1000))
screen.fill((81, 81, 81))

def clouds(surface, x, y, w, h):
    '''
    Функция рисует обдака на данном surface.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    w, h - ширина и высота изобажения. Нормальные пропорции(заложенные при рисовании) если w=800 h=250
    '''
    sub = pygame.Surface((800,250),pygame.SRCALPHA)
    
    ellipse(sub, (10, 10, 10, 128), (100, 30, 120, 40))
    ellipse(sub, (10, 10, 10, 128), (630, 50, 150, 60))
    ellipse(sub, (10, 10, 10, 128), (430, 40, 300, 70))
    ellipse(sub, (102, 153, 153, 128), (200, 150, 400, 100))
    ellipse(sub, (102, 153, 153, 128), (100, -10, 500, 120))
    ellipse(sub, (102, 153, 153, 128), (600, -20, 500, 120))
    ellipse(sub, (200, 200, 200, 128), (20, 20, 100, 30))
    ellipse(sub, (100, 100, 100, 128), (240, 40, 150, 30))
    ellipse(sub, (150, 150, 150, 128), (640, 30, 120, 40))
    surface.blit(tr.scale(sub,(w,h)),(x,y))
    
def betterflash(surface, x, y, w, h):
    '''
    Функция рисует засвеченные облака на данном surface.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    w, h - ширина и высота изобажения. Нормальные пропорции(заложенные при рисовании) если w=3000, h=300
    '''
    sub = pygame.Surface((3000,300),pygame.SRCALPHA)
    for i in range(25):
        ellipse(sub, (255,255,255,5*i), (5*i,5*i,10*(300-10*i),300-10*i))
    surface.blit(tr.scale(sub,(w,h)),(x,y))

def car(surface, x, y, w, h, inverse, color):
    '''
    Функция рисует машину на данном surface.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    w, h - ширина и высота изобажения. Нормальные пропорции(заложенные при рисовании) если w/h = 46/19
    inverse - булева переменная, если True, то изображение инвертируется по x
    color - цвет корпуса машины, заданный в формате, подходящем для pygame.Color
    '''
    sub = pygame.Surface((2300,950),pygame.SRCALPHA)
    ellipse(sub, BLACK, (0, 650, 150, 50))
    polygon(sub, color, [(500,0),(1500,0),(1500,400),(2300,400),(2300,800),(100,800),(100,400),(500,400)])
    rect(sub, LIGHTCYAN, (600,100,350,300))
    rect(sub, LIGHTCYAN, (1150,100,250,300))
    ellipse(sub, BLACK, (200,650,400,300))
    ellipse(sub, BLACK, (1700,650,400,300))
    surface.blit(tr.scale(tr.flip(sub,inverse,False),(w,h)),(x,y))

def bettercity(surface, x, y, w, h, inverse, alpha):
    '''
    Функция рисует здания на данном surface.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    w, h - ширина и высота изобажения. Нормальные пропорции(заложенные при рисовании) если w=606 h=643
    inverse - булева переменная, если True, то изображение инвертируется по x
    alpha - коэффициент прозрачности в типе pygame.Color
    '''
    sub = pygame.Surface((606,643),pygame.SRCALPHA)
    rect(sub, (255,255,255,alpha), (0,0,606,526))
    rect(sub, (184,197,201,alpha), (3,3,600,520))
    rect(sub, (148,169,174,alpha), (13,18,120,553))
    rect(sub, (148,174,169,alpha), (150,40,130,510))
    rect(sub, (184,201,197,alpha), (100,125,120,500))
    
    rect(sub, (220,228,227,alpha), (450,20,130,540))
    rect(sub, (111,146,139,alpha), (400,150,130,500))
    
    
    surface.blit(tr.scale(tr.flip(sub,inverse,False),(w,h)),(x,y))


clouds(screen, 0,0, 800,250)

bettercity(screen, 400,-100, 606,643, 0, 30)
bettercity(screen, -100,-100, 606,643, 0, 30)
bettercity(screen, 300,100, 606,643, 1, 255)
bettercity(screen, -100,150, 606,643, 0, 255)

car(screen, 270, 800, 230, 95, False, SKYBLUE)
car(screen, 490, 860, 345, 142, True, SKYBLUE)
car(screen, 530, 770, 161, 66, False, SKYBLUE)
car(screen, 470, 720, 92, 38, True, SKYBLUE)
car(screen, 200, 760, 138, 57, True, SKYBLUE)
car(screen, 80, 800, 161, 66, False, SKYBLUE)

betterflash(screen, -500,700, 3000,300)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
