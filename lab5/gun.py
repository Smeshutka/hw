import math
import random
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREEN = (0, 105, 0)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1500
HEIGHT = 900
TARGETS_ON_SCREEN = 2
TIME_OF_LIFE = FPS * 2


class Bullet:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса bullet

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.time = 0

    def move(self, ay=0,k=0.99 ):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна.
        """
        
        self.x += self.vx
        self.y += self.vy
        self.vy += ay
        if self.x >= WIDTH-self.r:
            self.x = WIDTH-self.r
            self.vx *= -k
        if self.y >= HEIGHT-self.r:
            self.y = HEIGHT-self.r
            self.vy *= -k
        if self.x <= self.r:
            self.x = self.r
            self.vx *= -k
        if self.y <= self.r:
            self.y = self.r
            self.vy *= -k
        

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        self.time +=1

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2+(self.y-obj.y)**2 <= (self.r+obj.r)**2:
            return True
        else:
            return False
        
    def check_death(self):
        if self.time > TIME_OF_LIFE:
            return True
        else:
            return False


class Tank:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.color = GREY
        self.x = 500
        self.y = 450
        self.v = 0
        self.MAX_V = 5
        self.body_an = 0
        self.dan = 0.05
        self.dv = 0.1

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, ar):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Bullet(self.screen, self.x, self.y)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        ar.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def draw_tank(self):
        subsur = pygame.Surface((100,50), pygame.SRCALPHA)
        pygame.draw.rect(subsur, DARK_GREEN, (0,0,100,50))
        pygame.draw.rect(subsur, BLACK, (0,0,100,50),width=2)
        subsur = pygame.transform.rotate(subsur, -self.body_an*180/math.pi)
        a,b = subsur.get_size()
        self.screen.blit(subsur, (self.x-a/2, self.y-b/2))

    def draw_gun(self):
        mx , my = pygame.mouse.get_pos()
        if mx > self.x:
            self.an = -math.atan((my-self.y) / (mx-self.x))
        if mx < self.x:
            self.an = -math.atan((my-self.y) / (mx-self.x))+math.pi

        subsur = pygame.Surface((150,50), pygame.SRCALPHA)
        pygame.draw.polygon(subsur, DARK_GREEN,
                            ((50,6), (87,6), (100,18), (100,32), (87,44), (50,44)))
        pygame.draw.rect(subsur, (self.f2_power/100*255,(1-self.f2_power/100)*255,0),
                        (100,18,50/100*self.f2_power,14))
        pygame.draw.polygon(subsur, BLACK,
                            ((50,6), (87,6), (100,18), (100,32), (87,44), (50,44)),width=2)
        pygame.draw.rect(subsur, BLACK, (100,18,50,14),width=2)
        subsur = pygame.transform.rotate(subsur, self.an*180/math.pi)
        a,b = subsur.get_size()
        self.screen.blit(subsur, (self.x-a/2, self.y-b/2))

    def move(self):
        self.x += self.v * math.cos(self.body_an)
        self.y += self.v * math.sin(self.body_an)
        
    def speed_up(self):
        if self.v < self.MAX_V:
            self.v += self.dv
    def speed_down(self):
        if self.v > -self.MAX_V:
            self.v -= self.dv
    def turn_left(self):
        self.body_an -= self.dan
    def turn_right(self):
        self.body_an += self.dan
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self,screen):
        self.screen = screen
        self.color = random.choice(GAME_COLORS)
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(10, 50)
        self.vx = random.randint(-20,20)
        self.vy = random.randint(-20,20)
    
    def move(self, ay=0, ax=0, k=0.95):
        self.x += self.vx
        self.y += self.vy
        self.vx += ax
        self.vy += ay
        if self.x >= WIDTH-self.r:
            self.x = WIDTH-self.r
            self.vx *= -k
        if self.y >= HEIGHT-self.r:
            self.y = HEIGHT-self.r
            self.vy *= -k
        if self.x <= self.r:
            self.x = self.r
            self.vx *= -k
        if self.y <= self.r:
            self.y = self.r
            self.vy *= -k
            
    def draw(self):
        """Рисование цели в виде кружка"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullets = []
targets = []
points = 0
fw, fa, fs, fd = 0, 0, 0, 0
    
clock = pygame.time.Clock()
tank = Tank(screen)

finished = False

while not finished:
    #блок отрисовки
    screen.fill(WHITE)
    tank.draw_tank()
    tank.draw_gun()
    for t in targets:
        t.draw()
    for b in bullets:
        b.draw()
    f = pygame.font.Font(None, 36)
    text = f.render('Score:' + str(points), 1, (0, 0, 0))
    screen.blit(text, (0, 20))
    pygame.display.update()

    #блок обработки событий
    clock.tick(FPS)       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tank.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                tank.fire2_end(bullets)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                fw = 1
            if event.key == pygame.K_a:
                fa = 1
            if event.key == pygame.K_s:
                fs = 1
            if event.key == pygame.K_d:
                fd = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                fw = 0
            if event.key == pygame.K_a:
                fa = 0
            if event.key == pygame.K_s:
                fs = 0
            if event.key == pygame.K_d:
                fd = 0

    #блок обработки механики
    if fw == 1 and fs == 0:
        tank.speed_up()
    elif fs == 1 and fw == 0:
        tank.speed_down()
    if fa == 1 and fd == 0:
        tank.turn_left()
    elif fa == 0 and fd == 1:
        tank.turn_right()
    while len(targets)<TARGETS_ON_SCREEN:
        targets.append(Target(screen))
    for b in bullets:
        b.move()
        if b.check_death():
            bullets.remove(b)
        for t in targets:
            if b.hittest(t):
                points += 1
                targets.remove(t)
                
    for t in targets:
        t.move()
    tank.move()
    tank.power_up()

print("Your score:", points)
pygame.quit()
