#OOP way of creating the snake game with pygame

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.display.set_caption("Snake Game")  # file title


class cube (object):
    rows = 20
    w = 500
    def __init__ (self,start, xdir =1 , ydir = 0, color = (255,0,0)):
        self.pos = start
        self.xdir = 1 #x direction is 1 so that the snake already starts moving when the game starts
        self.ydir = 0
        self.color = color

    def move (self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir
        self.pos = (self.pos[0] + self.xdir, self.pos[1] + self.ydir) #grid structure

    def draw (self,surface,eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]#rows
        j = self.pos[1]#columns

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))#to make the snake traverse through the grid
        if eyes:
            center = dis // 2 #middle of the cube
            radius = 3
            circleMiddle = (i*dis + center-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake (object): #snake object contains cube objects
    body = []
    turns = {}
    def __init__ (self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append (self.head) #self.body is made up of cube objects
        self.xdir = 0
        self.ydir = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys [pygame.K_LEFT]:
                    self.xdir = -1
                    self.ydir = 0
                    self.turns [self.head.pos[:]] = [self.xdir , self.ydir]

                elif keys [pygame.K_RIGHT]:
                    self.xdir = 1
                    self.ydir = 0
                    self.turns[self.head.pos[:]] = [self.xdir, self.ydir]

                elif keys [pygame.K_UP]:
                    self.xdir = 0
                    self.ydir = -1
                    self.turns[self.head.pos[:]] = [self.xdir, self.ydir]

                elif keys [pygame.K_DOWN]:
                    self.xdir = 0
                    self.ydir = 1
                    self.turns[self.head.pos[:]] = [self.xdir, self.ydir]

        for i, c in enumerate (self.body): # i = index, c = cube object
            p = c.pos[:] # the [:] makes a copy
            if p in self.turns: #grabbing each cube position and checking if they are in the turn list
                turn = self.turns[p]
                c.move (turn[0], turn [1])
                if i == len (self.body)-1:
                    self.turns.pop(p) #so that the snake does not automatically change directions
            else: #checking if end of screen is reached
                if c.xdir == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.xdir == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.ydir == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.ydir == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.xdir, c.ydir)#continue moving
            

    def reset (self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.xdir = 0
        self.ydir = 1

    def addCube (self):
        tail = self.body[-1]
        dx, dy = tail.xdir, tail.ydir

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1]))) # moving to the right, 1 less than x position of the tail
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1]))) # moving left, add 1 to the right
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].xdir = dx
        self.body[-1].ydir = dy


    def draw (self,surface):
        for i, c in enumerate (self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))  # start position x, y = 0 line drawn down
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))  # horizontal white lines

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y),positions))) > 0:  # The snack does not get randomized on the snake body - list of a filtered list
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)  # 10 FPS
        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):  # collision detection
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redrawWindow(win)

main ()

