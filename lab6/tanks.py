import math
import random
import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREEN = (0, 155, 0)
LIGHT = (255, 204, 102)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1500
HEIGHT = 900
TARGETS_ON_SCREEN = 2
HARD_TARGETS_ON_SCREEN = 2
TIME_OF_LIFE = FPS * 2


class Elastic_Bullet:
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
        self.color = BLACK
        self.time = 0
        

    def move(self, ay=0):
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
            self.vx *= -1
        if self.y >= HEIGHT-self.r:
            self.y = HEIGHT-self.r
            self.vy *= -1
        if self.x <= self.r:
            self.x = self.r
            self.vx *= -1
        if self.y <= self.r:
            self.y = self.r
            self.vy *= -1
        

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

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


class Bullet:
    def __init__(self, screen, x,y ,an):
        self.screen = screen
        self.x = x
        self.y = y
        self.an = an
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        
    def draw(self):
        subsur = pygame.Surface((10,3),pygame.SRCALPHA)
        pygame.draw.ellipse(subsur, BLACK, (-10,0,20,3))
        subsur = pygame.transform.rotate(subsur, self.an*180/math.pi)
        self.screen.blit(subsur,(self.x,self.y))
        
    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2+(self.y-obj.y)**2 <= (obj.r)**2:
            return True
        else:
            return False
    
    def check_boards(self):
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            return True
        else:
            return False
 

class Bomb:
    def __init__(self,screen,x,y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10 
        self.boom_r = 70
        self.activ = False
        self.timer = FPS*0.1
        self.boom_time = FPS*0.6
        self.boom_started = False
        self.n = random.randint(10,40)
        self.vy = 0
        self.pairs = []
        
    def make_pairs(self):
        for i in range(self.n):
            r1 = random.randint(55,65)
            r2 = random.randint(75,85)
            alpha = i*2*math.pi/self.n + (random.random()-0.5)/5
            x1 = r1*math.cos(alpha)+self.x
            y1 = r1*math.sin(alpha)+self.y
            x2 = r2*math.cos(alpha+math.pi/self.n)+self.x
            y2 = r2*math.sin(alpha+math.pi/self.n)+self.y
            self.pairs.append([x1,y1])
            self.pairs.append([x2,y2])
    
    def check_dang_zone(self,obj):
        if (self.x-obj.x)**2+(self.y-obj.y)**2 <= (self.boom_r)**2:
            return True
        else:
            return False
    
    def draw_boom(self):
        
        pygame.draw.polygon(self.screen, (255,137,25),self.pairs)
        self.boom_time -= 1
        
    def check_activ(self):
        if self.timer == 0:
            self.activ = True
        
    def draw_dang_zone(self):
        k = 0.003
        for i in range(20):
            pygame.draw.arc(self.screen, BLACK, (self.x-self.boom_r,self.y-self.boom_r,
                                                 2*self.boom_r,2*self.boom_r),
                            i*math.pi/10-self.timer*k, i*math.pi/10+math.pi/20-self.timer*k)
        
    def draw(self):
        r = self.r
        a = 8
        pygame.draw.circle(self.screen, (205,172,0), (self.x,self.y), r)
        pygame.draw.circle(self.screen, RED, (self.x,self.y), 4)
        pygame.draw.rect(self.screen, BLACK, (self.x-a/2,self.y-r-2,a,4))
        pygame.draw.rect(self.screen, BLACK, (self.x-a/2,self.y+r-2,a,4))
        pygame.draw.rect(self.screen, BLACK, (self.x+r-2,self.y-a/2,4,a))
        pygame.draw.rect(self.screen, BLACK, (self.x-r-2,self.y-a/2,4,a))
        
    def move(self):
        self.y += self.vy
        self.vy += 0.1


class Tank:
    def __init__(self, screen, color, x, y):
        self.screen = screen
        self.color = color
        self.f2_power = 10
        self.f2_on = 0
        self.an = math.pi/2
        self.x = x
        self.y = y
        self.v = 0
        self.MAX_V = 2.5*k
        self.body_an = -math.pi/2
        self.dan = 0.05
        self.dv = 0.1
        self.hp = 5
        self.box_size = [100, 50]
        self.center_pos = [self.x + self.box_size[0]/2, self.y + self.box_size[1]/2]
        self.cooldawn = 0
        self.mg_cd = 0
    
    def use_mg(self, ar):
        if self.mg_cd == 0:
            dx = 40*math.cos(-self.body_an) + 15*math.sin(-self.body_an)
            dy = -40*math.sin(-self.body_an) + 15*math.cos(-self.body_an)
            new_bullet = Bullet(self.screen, self.x+dx, self.y+dy, -self.body_an)
            new_bullet.vx = 20 * math.cos(-self.body_an)*k
            new_bullet.vy = - 20 * math.sin(-self.body_an)*k
            ar.append(new_bullet)
            self.mg_cd = 20
            
    def fire2_start(self):
        if self.cooldawn == 0:
            self.f2_on = 1

    def fire2_end(self, ar):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от поворота башни.
        """
        if self.f2_on == 1:
            dx = 75*math.cos(-self.body_an)
            dy = -75*math.sin(-self.body_an)
            new_ball = Elastic_Bullet(self.screen, self.x+dx, self.y+dy)
            new_ball.vx = self.f2_power/4 * math.cos(-self.body_an) *k
            new_ball.vy = - self.f2_power/4 * math.sin(-self.body_an)*k
            ar.append(new_ball)
            self.f2_on = 0
            self.f2_power = 10
            self.cooldawn = FPS
        
    def draw_tank(self):
        
        subsur = pygame.Surface((100,50), pygame.SRCALPHA)
        pygame.draw.rect(subsur, self.color, (0,0,100,50))
        pygame.draw.rect(subsur, BLACK, (0,0,100,5))
        pygame.draw.rect(subsur, BLACK, (0,45,100,5))
        pygame.draw.rect(subsur, WHITE, (97,10,3,30))
        pygame.draw.rect(subsur, WHITE, (0,10,1,30))
        pygame.draw.rect(subsur, BLACK, (5,0,5,50))
        pygame.draw.polygon(subsur, BLACK,
                            ((85,5),(95,25),(85,45),(82,45),(92,25),(82,5)))        
        subsur = pygame.transform.rotate(subsur, -self.body_an*180/math.pi)
        a,b = subsur.get_size()
        self.box_size = [a, b]
        #pygame.draw.rect(subsur, BLACK, (0,0,a,b),width=2)
        self.screen.blit(subsur, (self.x-a/2, self.y-b/2))
        pygame.draw.arc(self.screen, BLACK,
                        (self.x+a/2,self.y+b/2,20,20),0,self.cooldawn/FPS*2*math.pi, width =6)
        
        sub = pygame.Surface((20,20), pygame.SRCALPHA)
        dots = ((0,5),(5,0),(10,5),(15,0),(20,5),(10,20))
        pygame.draw.polygon(sub, (255,0,0), dots)
        for i in range(self.hp):
            self.screen.blit(sub, (self.x-50+25*i, self.y-b/2-30))

    def draw_gun(self):

        subsur = pygame.Surface((150,50), pygame.SRCALPHA)
        
        pygame.draw.rect(subsur, BLACK, (75,40,40,3))
        pygame.draw.polygon(subsur, self.color,
                            ((50,6), (87,6), (100,18), (100,32), (87,44), (50,44)))
        pygame.draw.rect(subsur, (self.f2_power/100*255,(1-self.f2_power/100)*255,0),
                        (100,18,50/100*self.f2_power,14))
        pygame.draw.polygon(subsur, BLACK,
                            ((50,6), (87,6), (100,18), (100,32), (87,44), (50,44)),width=2)
        pygame.draw.circle(subsur, BLACK, (75,20), 10, width=2)
        pygame.draw.rect(subsur, BLACK, (100,18,50,14),width=2)
        subsur = pygame.transform.rotate(subsur, -self.body_an*180/math.pi)
        a,b = subsur.get_size()
        #pygame.draw.rect(subsur, BLACK, (0,0,a,b),width=2)
        self.screen.blit(subsur, (self.x-a/2, self.y-b/2))
        

    def move(self):
        dx = self.v * math.cos(self.body_an)
        dy = self.v * math.sin(self.body_an)
        x = self.x
        y = self.y
        a = self.box_size[0]
        b = self.box_size[1]
        if x+dx<a/2 or x+dx>WIDTH-a/2 or y+dy<b/2 or y+dy>HEIGHT-b/2:
            self.v = 0
            dx = 0
            dy = 0
        self.x += dx
        self.y += dy
        
    def speed_up(self):
        if self.v < self.MAX_V:
            self.v += self.dv
    def speed_down(self):
        if self.v > -self.MAX_V:
            self.v -= self.dv
    def turn_left(self):
        sub = pygame.Surface((100,50))
        sub = pygame.transform.rotate(sub, (-self.body_an+self.dan)*180/math.pi)
        a,b = sub.get_size()
        
        if self.x-a/2 > 0 and self.x+a/2 < WIDTH and self.y-b/2 > 0 and self.y+b/2 < HEIGHT:
            self.body_an -= self.dan
    def turn_right(self):
        sub = pygame.Surface((100,50))
        sub = pygame.transform.rotate(sub, (-self.body_an-self.dan)*180/math.pi)
        a,b = sub.get_size()
        if self.x-a/2 > 0 and self.x+a/2 < WIDTH and self.y-b/2 > 0 and self.y+b/2 < HEIGHT:
            self.body_an += self.dan
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                
    def hittest(self, bul):
        al = -self.body_an
        while al >= math.pi *2:
            al -= 2*math.pi
        while al < 0:
            al += 2*math.pi
        y = bul.y
        x = bul.x
        x1, y1 = 50*math.cos(al)-25*math.sin(al)+self.x,  50*math.sin(al)+25*math.cos(al)+self.y
        x2, y2 = 50*math.cos(al)+25*math.sin(al)+self.x,  50*math.sin(al)-25*math.cos(al)+self.y
        x3, y3 = -50*math.cos(al)+25*math.sin(al)+self.x, -50*math.sin(al)-25*math.cos(al)+self.y
        x4, y4 = -50*math.cos(al)-25*math.sin(al)+self.x, -50*math.sin(al)+25*math.cos(al)+self.y
        S12 = abs((x1-x)*(y2-y)-(x2-x)*(y1-y))
        S23 = abs((x2-x)*(y3-y)-(x3-x)*(y2-y))
        S34 = abs((x3-x)*(y4-y)-(x4-x)*(y3-y))
        S41 = abs((x4-x)*(y1-y)-(x1-x)*(y4-y))
        
        if abs(S12+S23+S34+S41 - 2*100*50)<0.00001:
            return True
        else:
            return False


class Target:
    def __init__(self,screen):
        self.screen = screen
        self.color = random.choice(GAME_COLORS)
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(10, 50)
        self.vx = random.randint(-10,10)*k
        self.vy = random.randint(-10,10)*k
        self.hp = 3
    
    def move(self, ay=0, ax=0):
        self.x += self.vx
        self.y += self.vy
        self.vx += ax
        self.vy += ay
        if self.x >= WIDTH-self.r:
            self.x = WIDTH-self.r
            self.vx *= -1
        if self.y >= HEIGHT-self.r:
            self.y = HEIGHT-self.r
            self.vy *= -1
        if self.x <= self.r:
            self.x = self.r
            self.vx *= -1
        if self.y <= self.r:
            self.y = self.r
            self.vy *= -1
            
    def draw(self):
        """Рисование цели в виде кружка"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class Hard_Target:
    def __init__(self, screen):
        self.screen = screen
        self.color = random.choice(GAME_COLORS)
        self.r = random.randint(20,30)
        self.an = random.random()*2*math.pi
        self.vbx = random.randint(-10,10)
        self.vby = random.randint(-10,10)
        self.br = random.randint(50,100)
        self.bx = random.randint(300,700)
        self.by = random.randint(300,700)
        self.x = self.bx+self.br*math.cos(self.an)
        self.y = self.by-self.br*math.sin(self.an)
        self.an_speed = (random.random()-0.5)*0.2
        self.hp = 1
            
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.line(self.screen, BLACK, (self.x-self.r, self.y), (self.x+self.r, self.y))
        pygame.draw.line(self.screen, BLACK, (self.x, self.y-self.r), (self.x, self.y+self.r))
            
    def move(self):
        self.bx += self.vbx
        self.by += self.vby
        self.an += self.an_speed
        self.x = self.bx+self.br*math.cos(self.an)
        self.y = self.by-self.br*math.sin(self.an)
        if self.x >= WIDTH-self.r:
            self.x = WIDTH-self.r
            self.vbx *= -1
        if self.y >= HEIGHT-self.r:
            self.y = HEIGHT-self.r
            self.vby *= -1
        if self.x <= self.r:
            self.x = self.r
            self.vbx *= -1
        if self.y <= self.r:
            self.y = self.r
            self.vby *= -1
    
    def drop_bomb(self,ar):
        ar.append(Bomb(self.screen, self.x, self.y))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
elastic_bullets = []
bullets = []
targets = []
bombs = []
hard_targets = []
points = 0
w_press, a_press, s_press, d_press = 0, 0, 0, 0
up_press, left_press, down_press, right_press = 0, 0, 0, 0
mg_start1, mg_start2 = 0, 0
k = 0.7

clock = pygame.time.Clock()
tank1 = Tank(screen,DARK_GREEN, 60, HEIGHT - 60)
tank2 = Tank(screen,LIGHT, WIDTH-60, HEIGHT - 60)

finished = False

while not finished:
    #блок отрисовки
    screen.fill(WHITE)
    tank1.draw_tank()
    tank1.draw_gun()
    tank2.draw_tank()
    tank2.draw_gun()
    for ht in hard_targets:
        ht.draw()
        
    for t in targets:
        t.draw()
        
    for eb in elastic_bullets:
        eb.draw()
        
    for b in bullets:
        b.draw()
        
    for bomb in bombs:
        if bomb.boom_started and bomb.boom_time > 0:
            bomb.draw_boom()
        else:
            bomb.draw()
            if bomb.activ: 
                bomb.draw_dang_zone()
        
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
                tank1.fire2_start()
            elif event.button == 3:
                mg_start1 = 1
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                tank1.fire2_end(elastic_bullets)
            elif event.button == 3:
                mg_start1 = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                tank1.fire2_start()
            if event.key == pygame.K_g:
                mg_start1 = 1
            if event.key == pygame.K_o:
                tank2.fire2_start()
            if event.key == pygame.K_p:
                mg_start2 = 1
            if event.key == pygame.K_w:
                w_press = 1
            if event.key == pygame.K_a:
                a_press = 1
            if event.key == pygame.K_s:
                s_press = 1
            if event.key == pygame.K_d:
                d_press = 1
            if event.key == pygame.K_UP:
                up_press = 1
            if event.key == pygame.K_LEFT:
                left_press = 1
            if event.key == pygame.K_DOWN:
                down_press = 1
            if event.key == pygame.K_RIGHT:
                right_press = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                tank1.fire2_end(elastic_bullets)
            if event.key == pygame.K_g:
                mg_start1 = 0
            if event.key == pygame.K_o:
                tank2.fire2_end(elastic_bullets)
            if event.key == pygame.K_p:
                mg_start2 = 0
            if event.key == pygame.K_w:
                w_press = 0
            if event.key == pygame.K_a:
                a_press = 0
            if event.key == pygame.K_s:
                s_press = 0
            if event.key == pygame.K_d:
                d_press = 0
            if event.key == pygame.K_UP:
                up_press = 0
            if event.key == pygame.K_LEFT:
                left_press = 0
            if event.key == pygame.K_DOWN:
                down_press = 0
            if event.key == pygame.K_RIGHT:
                right_press = 0

    #блок обработки механики
    
    if w_press == 1 and s_press == 0:
        tank1.speed_up()
    elif s_press == 1 and w_press == 0:
        tank1.speed_down()
    if a_press and d_press == 0:
        tank1.turn_left()
    elif a_press == 0 and d_press == 1:
        tank1.turn_right()
    if up_press == 1 and down_press == 0:
        tank2.speed_up()
    elif down_press == 1 and up_press == 0:
        tank2.speed_down()
    if left_press == 1 and right_press == 0:
        tank2.turn_left()
    elif left_press == 0 and right_press == 1:
        tank2.turn_right()
        
    while len(targets)<TARGETS_ON_SCREEN:
        targets.append(Target(screen))
    while len(hard_targets)<HARD_TARGETS_ON_SCREEN:
        hard_targets.append(Hard_Target(screen))

    for eb in elastic_bullets:
        eb.time += 1
        eb.move()
        if eb.check_death():
            elastic_bullets.remove(eb)
        for t in targets:
            if eb.hittest(t):
                t.hp -= 3
                elastic_bullets.remove(eb)
        for ht in hard_targets:
            if eb.hittest(ht):
                elastic_bullets.remove(eb)
                ht.hp -= 1
        for bomb in bombs:
            if eb.hittest(bomb):
                bomb.make_pairs()
                bomb.boom_started = True
        if tank1.hittest(eb):
            tank1.hp -= 1
            elastic_bullets.remove(eb)
        if tank2.hittest(eb):
            tank2.hp -= 1
            elastic_bullets.remove(eb)
            
    
    for b in bullets:
        b.move()
        if b.check_boards():
            bullets.remove(b)
        for t in targets:
            if b.hittest(t):
                t.hp -= 1
                bullets.remove(b)
        for ht in hard_targets:
            if b.hittest(ht):
                bullets.remove(b)
                ht.hp -= 1
        for bomb in bombs:
            if b.hittest(bomb):
                bomb.make_pairs()
                bomb.boom_started = True
        if tank1.hittest(b):
            tank1.hp -= 1
            bullets.remove(ab)
        if tank2.hittest(b):
            tank2.hp -= 1
            bullets.remove(b)
                    
    for bomb in bombs:
        bomb.move()
        bomb.timer -= 1
        if bomb.boom_started:
            bomb.boom_time -= 1
        bomb.check_activ()
        if bomb.activ  :
            if bomb.check_dang_zone(tank1) and not(bomb.boom_started):
                tank1.hp -= 1
                bomb.make_pairs()
                bomb.boom_started = True
            if bomb.check_dang_zone(tank2) and not(bomb.boom_started):
                tank2.hp -= 1
                bomb.make_pairs()
                bomb.boom_started = True
        if bomb.boom_time <= 0 or bomb.y >= HEIGHT+bomb.boom_r:
            bombs.remove(bomb)
    
    for ht in hard_targets:
        ht.move()
        if random.random() < 0.01:
            ht.drop_bomb(bombs)
        if ht.hp <= 0:
            hard_targets.remove(ht)
            points += 2
        
    for t in targets:
        t.move()
        if t.hp <= 0:
            targets.remove(t)
            points += 1
            
    if tank1.cooldawn > 0:
        tank1.cooldawn -= 1
    if tank1.mg_cd > 0:
        tank1.mg_cd -= 1
    if tank2.cooldawn > 0:
        tank2.cooldawn -= 1
    if tank2.mg_cd > 0:
        tank2.mg_cd -= 1
    tank1.move()
    tank1.power_up()
    tank2.move()
    tank2.power_up()
    if mg_start1 == 1:
        tank1.use_mg(bullets)
    if mg_start2 == 1:
        tank2.use_mg(bullets)
    if tank1.hp <= 0:
        print("Player 2 win!")
        finished = True
    if tank2.hp <= 0:
        print("Player 1 win!")
        finished = True
print("Your score:", points)
pygame.quit()

