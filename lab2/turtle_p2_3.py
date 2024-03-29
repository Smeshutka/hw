import turtle as t

def check(a,i):
    if a[i] == 1:
        t.pendown()
    if a[i] == 0:
        t.penup()

def num(a,l):
    k=0
    for i in range(4):
        check(a,k)
        k+=1
        t.forward(l)
        t.left(90)
    t.left(45)
    check(a,k)
    k+=1
    t.forward(l*2**0.5)
    t.left(45)
    for i in range(3):
        check(a,k)
        k+=1
        t.forward(l)
        t.left(90)
    t.left(45)
    check(a,k)
    k+=1
    t.forward(l*2**0.5)
    t.penup()
    t.right(135)
    t.forward(2*l)
    t.left(90)

x = int(input())
y=[]
while x!=0:
    y.append(x%10)
    x = x//10

t.shape('turtle')
t.speed(10)

input = open('shrift.txt', 'r')
a = []
for i in range(10):
    a.append(list(map(int,input.readline().split(','))))

t.penup()
t.goto(-300,0)
for j in y[::-1]:
    num(a[j],50)
    t.forward(50)
input.close()