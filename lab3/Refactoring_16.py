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
screen = pygame.display.set_mode((800, 800))
screen.fill((51, 51, 51))

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
    
def flash(surface, x, y, w, h):
    '''
    Функция рисует засвеченные облака на данном surface.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    w, h - ширина и высота изобажения. Нормальные пропорции(заложенные при рисовании) если w=800 
    '''
    sub = pygame.Surface((800,800),pygame.SRCALPHA)
    i = 0
    m = 51
    n = 51
    k = 51
    r = 300
    l = -500
    z = 500
    while i < 25:
        m += 6
        n += 6
        k += 6
        r -= 10
        l += 5
        z += 5
        i += 1
        ellipse(sub, (m, n, k, 128), (l, z, 10*r, r))
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

def city(surface, x, y, w, h):
    '''
    Функция рисует здания на данном surface.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    w, h - ширина и высота изобажения. Нормальные пропорции(заложенные при рисовании) если w=800 h=520
    '''
    sub = pygame.Surface((800,520),pygame.SRCALPHA)
    rect(sub, (50, 50, 50), (0, 0, 800, 120))
    rect(sub, (1, 1, 1, 158), (500, 0, 100, 100))
    rect(sub, (1, 1, 1, 58), (200, 0, 100, 100))
    rect(sub, (1, 1, 1, 150), (0, 0, 100, 100))
    rect(sub, (204, 204, 204), (500, 20, 150, 500))
    rect(sub, (102, 102, 102), (310, 70, 120, 400))
    rect(sub, (102, 102, 102), (450, 110, 120, 400))
    rect(sub, (153, 204, 204), (10, 100, 120, 400))  
    rect(sub, (153, 204, 204), (670, 90, 120, 400)) 
    rect(sub, (220, 220, 220, 128), (20, 150, 300, 300))
    rect(sub, (220, 220, 220, 128), (500, 120, 300, 300))

    surface.blit(tr.scale(sub,(w,h)),(x,y))


car(screen, 270, 600, 230, 95, False, SKYBLUE)
car(screen, 490, 660, 345, 142, True, SKYBLUE)
car(screen, 530, 570, 161, 66, False, SKYBLUE)
car(screen, 430, 520, 92, 38, True, SKYBLUE)
car(screen, 200, 530, 138, 57, True, SKYBLUE)
car(screen, 80, 600, 161, 66, False, SKYBLUE)

clouds(screen, 0,0, 800,250)
city(screen, 0,0, 800,520)
flash(screen, 0,0, 800,800)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
