import pygame
from pygame.draw import *
from random import randint

file = open('best_players.txt', 'r')
lop = []#lop = list of players
for fline in file:
    for i in range(len(fline)):
        if fline[len(fline)-1-i] == ' ':
            lop.append([fline[0:len(fline)-1-i], int(fline[len(fline)-i:len(fline)-1])])
file.close()
print("Please print your nick: ")
pname = input()

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

ballsOnScreen = 7 #Задаёт количество мячиков на экране
specOnScreen = 2
time_of_life = 3.5*FPS
g = 2

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

points = 0 #Счётчик очков
sp = []
ls = []
'''
Массив в котором эл-ты типа [x,y,r,c,vx,vy,t], где
x,y - координаты центра шарика,
r -радиус шарика
с - номер цвета из массива COLORS
vx, vy - скорости шарика по соотв. осям
t - количество тиков которое существует шарик
'''

def new_ball(ls):
    '''
    Фунция добавляет шарик в наш массив со случайными начальными координатами и скоростями
    '''
    ls.append([randint(100,1100), randint(100,800), randint(30,50), randint(0, 5), randint(-20,20), randint(-20,20),0])
    return ls

def createSpec(sp):
    '''
    
    '''
    sp.append([randint(100,1100), randint(100,800), 10, 2, randint(-20,20), randint(-20,20), randint(0,10)])
    return sp

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
def hitspec(event):
    '''
    Функция обрабатывает щелчки и возвращает номер специального шарика в массиве по которому щёлкнули и -1
    если не попали по шарику
    event - событие типа Event 
    '''
    (mx, my) = event.pos
    hit = -1
    for i in range(len(sp)):
        if (mx-sp[i][0])**2 + (my-sp[i][1])**2 < sp[i][2]**2:
            hit = i
    return hit

def drawballs(ls,sp):
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
    for i in range(len(sp)):
        sp[i][5] += g
        sp[i][0] += sp[i][4]
        sp[i][1] += sp[i][5]
        if sp[i][0] >= 1150 or sp[i][0]<0:
            sp[i][4] *= -1
        if sp[i][1] <0:
            sp[i][5] *= -1
        if sp[i][1]>= 850:
            sp[i][1] = 848
            sp[i][5] = -1*abs(sp[i][5])
        circle(screen, COLORS[sp[i][3]], (sp[i][0],sp[i][1]), sp[i][2])
        line(screen, BLACK, [sp[i][0]-sp[i][2], sp[i][1]], [sp[i][0]+sp[i][2], sp[i][1]], width = 2)
        line(screen, BLACK, [sp[i][0], sp[i][1]-sp[i][2]], [sp[i][0], sp[i][1]+sp[i][2]], width = 2)

def killballs(ls,sp):
    '''
    Функция изменяет счётчик времени до смерти мячиков и убирает их если настала им пора уйти
    '''
    a=[]
    for i in range(len(ls)):
        ls[i][6] += 1
        if ls[i][6] >= time_of_life:
            a.append(i)
    for i in range(len(a)-1,-1,-1):
        ls.pop(a[i])
    a.clear()
    for i in range(len(sp)):
        sp[i][6] += 1
        if sp[i][6] >= time_of_life:
            a.append(i)
    for i in range(len(a)-1,-1,-1):
        sp.pop(a[i])


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
            k = hitspec(event)
            if k != -1:
                points+=5
                sp.pop(k)
    killballs(ls,sp)
    if len(ls) < ballsOnScreen:
        ls = new_ball(ls)
    if len(sp) < specOnScreen:
        sp = createSpec(sp)
    drawballs(ls,sp)
    
    f = pygame.font.Font(None, 36)
    text = f.render('Score:' + str(points), 1, (180, 0, 0))
    screen.blit(text, (250, 20))
    
    pygame.display.update()
    screen.fill(BLACK)

file = open('best_players.txt', 'w')
flag = 0
for i in range(len(lop)):
    if lop[i][0] == pname:
        flag = 1
        if lop[i][1] < points:
            lop[i][1] = points
if flag == 0:
    lop.append([pname,points])
sorted(lop, key=lambda a: a[1]) 
for i in range(len(lop)):
    file.write(str(lop[i][0])+' '+str(lop[i][1])+'\n')
file.close()
pygame.quit()
