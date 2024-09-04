import pygame as pg
import sys
import time

RUN = True
WIDTH = 800
PixelsPerCM = 57.14
HEIGHT = 800 #800 px is 14 cm

physicsRectColor = "white"

METRE = 100 * PixelsPerCM
TICKS = 100
GRAVITY = 1 * METRE / TICKS**2 #metres per second sq

pg.init()
clock = pg.time.Clock() 
window = pg.display.set_mode((WIDTH,HEIGHT))

class PhysicsRect():
    def __init__(self,topLeft,bottomRight) -> None:
        self.pos = [topLeft,[abs(bottomRight[0]-topLeft[0]),abs(bottomRight[1]-topLeft[1])]]
        print(self.pos)
        self.centreOfMass = [(bottomRight[0]-topLeft[0])/2,(bottomRight[1]-topLeft[1])/2]
        self.vel = 0
        self.timeIstantiated = time.time()
        self.rectobj = pg.Rect(self.pos)
        self.rectobj.normalize()
        self.color = physicsRectColor
        self.clicked = False
    def draw(self):
        pg.draw.rect(window,self.color,self.rectobj)


    def move(self):
        
        self.vel += GRAVITY
        self.rectobj.move_ip(0,self.vel)

    def drag(self,mousePos):
        if self.clicked:
            self.rectobj.update((mousePos[0]-self.centreOfMass[0],mousePos[1]-self.centreOfMass[1]),self.pos[1])

    def contactWithStationaryBlock(self,stationaryObj):
        if self.rectobj.clip(stationaryObj):
            self.vel = -self.vel

class StationaryBlock():
    def __init__(self,topLeft,bottomRight) -> None:
        self.coords = [topLeft,[abs(bottomRight[0]-topLeft[0]),abs(bottomRight[1]-topLeft[1])]]
        self.rectobj = pg.Rect(self.coords)
    def draw(self):
        pg.draw.rect(window,"white",self.rectobj)


physicsObjects = []
physicsObjectsCoords = []
StationaryObjects = []
times = []

# STATES
BUILDING = False

# INITIAL OBJECTS 
floor = StationaryBlock([0,HEIGHT-1],[WIDTH,HEIGHT])
StationaryObjects.append(floor)

while RUN:
    events = pg.event.get()
    mousePos = pg.mouse.get_pos()

    for event in events:
        if event.type == pg.KEYDOWN:
            key = event.unicode
            if key == 'q':
                RUN = False
            if key == 'b':
                BUILDING = not BUILDING
                if BUILDING:
                    physicsRectColor = "green"
                else:
                    physicsObjectsCoords = []
                    physicsRectColor = "white"

        if event.type == pg.QUIT:
            RUN = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if BUILDING:
                
                physicsObjectsCoords.append([mousePos[0],mousePos[1]])

                if len(physicsObjectsCoords) == 2:
                    physicsObjects.append(PhysicsRect(physicsObjectsCoords[0],physicsObjectsCoords[1]))
                    physicsObjectsCoords = []
            else:
                for i in physicsObjects:
                    if i.rectobj.collidepoint(mousePos):
                        i.color = "red"
                        i.clicked = True
                        print('clicked')
        if event.type == pg.MOUSEBUTTONUP:
            if not BUILDING:
                for i in physicsObjects:
                    if i.clicked:
                        i.clicked = False


    if BUILDING:
        mousePos = pg.mouse.get_pos()
        pg.draw.circle(window,'green',mousePos,2)
        if len(physicsObjectsCoords) == 1:
            pg.draw.rect(window,"darkgreen",pg.Rect([physicsObjectsCoords[0],[abs(mousePos[0]-physicsObjectsCoords[0][0]),abs(mousePos[1]-physicsObjectsCoords[0][1])]]))

    for i in physicsObjects:
        mousePos = pg.mouse.get_pos()
        if BUILDING:
            i.color = "green"
        elif not i.clicked:
            i.color = "white"


        if i.pos[0][1] > HEIGHT:
            # to check when object has gone off screen

                # TIME OF FALLING
            # print(time.time() - i.timeIstantiated)
            # times.append(time.time()-i.timeIstantiated)

            physicsObjects.remove(i)
        
        for j in StationaryObjects:
            i.contactWithStationaryBlock(j.rectobj)
        for k in physicsObjects:
            if k is not i:
                i.contactWithStationaryBlock(k.rectobj)

        i.draw()
        if(i.clicked):
            i.drag(mousePos)
        else: 
            i.move()

    for i in StationaryObjects:
        i.draw()

    pg.display.update()
    window.fill('black')
    clock.tick(TICKS)

pg.quit()
sys.exit()