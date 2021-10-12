import pygame
from pygame.draw import *
from random import randint

#print("Please print your nick: ")
#pname = input()

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

ballsOnScreen = 5 #Задаёт количество мячиков на экране
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

points = 0 #Счётчик очков
ls = []
'''
Массив в котором эл-ты типа [x,y,r,c,vx,vy], где
x,y - координаты центра шарика,
r -радиус шарика
с - номер цвета из массива COLORS
vx, vy - скорости шарика по соотв. осям
'''

def new_ball(ls):
    '''
    Фунция добавляет шарик в наш массив со случайными начальными координатами и скоростями
    '''
    ls.append([randint(100,1100), randint(100,800), randint(30,50), randint(0, 5),randint(-20,20),randint(-20,20)])
    return ls

def hit(event):
    '''
    Функция обрабатывает щелчки и возвращает номер шарика в массиве по которому щёлкнули и -1
    если не попали по шарику
    event - событие типа Event 
    '''
    (mx, my) = event.pos
    hit = -1
    for i in range(len(ls)):
        if (mx-ls[i][0])**2 + (my-ls[i][1])**2 < ls[i][2]**2:
            hit = i
    return hit
            
            

def drawls(ls):
    '''
    Функция отрисовывает все шарики на экране и двигает их с заданной в списке ls скоростью
    '''
    for i in range(len(ls)):
        ls[i][0] += ls[i][4]
        ls[i][1] += ls[i][5]
        if ls[i][0]>=1150 :
            ls[i][4] = randint(-20,0)
            ls[i][5] = randint(-20,20)
        if ls[i][0]<0 :
            ls[i][4] = randint(0,20)
            ls[i][5] = randint(-20,20)
            
        if ls[i][1]>=850 :
            ls[i][4] = randint(-20,20)
            ls[i][5] = randint(-20,0)
        if ls[i][1]<0 :
            ls[i][4] = randint(-20,20)
            ls[i][5] = randint(0,20)
        circle(screen, COLORS[ls[i][3]], (ls[i][0],ls[i][1]), ls[i][2])
    return ls

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Thanks for game! Your score: ", points)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            k = hit(event)
            if k != -1:
                points+=1
                ls.pop(k)
            
    
    if len(ls) < ballsOnScreen:
        ls = new_ball(ls)
    ls = drawls(ls)
    
    f = pygame.font.Font(None, 36)
    text = f.render('Score:' + str(points), 1, (180, 0, 0))
    screen.blit(text, (250, 20))
    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
