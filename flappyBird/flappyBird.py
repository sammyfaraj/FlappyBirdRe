#imports
import pygame
import random

#general values
red = (123,59,62)
blue = (0,0,205)
green = (62,123,59)
black = (0,0,0)

#game values
pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
screenw = 600
screenh = 800
screen = [screenw,screenh]
win = pygame.display.set_mode(screen)
lives = 3
points = 0
highpoints = 0 

#the "bird"
class Circle:
    def __init__(self,size):
        self.size = size
        self.y = 250
        self.x = 150
        self.speed = 0
        self.gravity = 1
    def move(self):
        self.y += self.speed
        self.speed += self.gravity
        
#the "pipes"
class Pipe:
    def __init__(self):
        self.w = screenw
        self.h = screenh
        self.pipet = random.randint(100,int(2*screenh/3) - 30)
        self.pipeb = random.randint(50,screenh - self.pipet - 30)
        self.pipew = 50
        self.speed = 5
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    def move(self):
        self.w -= self.speed
        self.h -= self.speed

class Reset():
    def __init__(self,circle):
        npc.y = 250
        npc.x = 150
        npc.speed = 0
        self.gravity = 0

#object initialization
npc = Circle(15)
pipe = Pipe()
pipes = [pipe]
marked = []
bird = pygame.image.load('bird.png')
birdo = pygame.image.load('birdo.png')
bg = pygame.image.load('backd2.png')
reset = False

#game loop
run = True
while run:
    points += .1
    pygame.time.delay(30)

    #font rendering
    textlive = myfont.render('Lives: ' + str(lives), 1, blue)
    textpoint = myfont.render('Score: ' + str(int(points)), 1, blue)
    textdead = myfont.render('Press space to continue', 1, blue)
    textdeads = myfont.render('Current Score: ' + str(int(points)), 1, blue)
    

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:          
                npc.speed -= 10
            if event.key == pygame.K_q:
                run = False
                exit()
    #death loop
    while reset:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset = False

    #generate pipes
    if pipes[-1].w == 2*(screenw/3):
        pipe = Pipe()
        pipes.append(pipe)
    if pipes[0].w == 0:
        del pipes[0]
        
    #speed logic        
    npc.move()
    for pipe in pipes:
        pipe.move()
        
    #collision logic
    for pipe in pipes:
        if pipe not in marked:
            if pipe.w < npc.x < pipe.w+pipe.pipew and (npc.y > screenh-pipe.pipeb or npc.y < pipe.pipet):
                marked.append(pipe)
                pipe.color = red
                lives -= 1
                #upon death
                if lives == 0:
                    if points > highpoints:
                        highpoints = points
                    lives = 3
                    points = 0
                    Reset(npc)
                    reset = True
                    pipe = Pipe()
                    pipes = [pipe]
                    textdeadh = myfont.render('High Score: ' + str(int(highpoints)), 1, blue)
                    
                
    #update/draw
    win.blit(bg,(0,0))
    if reset == False:
        win.blit(textlive,(5,0))
        win.blit(textpoint,(5,23))
    if reset == True:
        win.blit(textdead,(200,150))
        win.blit(textdeads,(200,175))
        win.blit(textdeadh,(200,200))
    if npc.speed >= 0:
        win.blit(bird,(npc.x,npc.y))
    elif npc.speed < 0:
        win.blit(birdo,(npc.x,npc.y))
    for pipe in pipes:
        pygame.draw.rect(win,pipe.color,(pipe.w,0,pipe.pipew,pipe.pipet))
        pygame.draw.rect(win,pipe.color,(pipe.w,screenh-pipe.pipeb,pipe.pipew,pipe.pipeb))
    pygame.display.flip()

    #bounds
    if npc.y > screenh:
        npc.speed = 0
        npc.y = screenh - 1
    elif npc.y < 0:
        npc.speed = 0
        npc.y = 1
    




    
    
