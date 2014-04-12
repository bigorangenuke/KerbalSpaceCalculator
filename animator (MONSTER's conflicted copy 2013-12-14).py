from pygame.locals import *
import pygame as pg
import ksp
import orbit
import numpy as np


def setup():
    kerbin=ksp.Body('kerbin')
    sma = kerbin.semiMajorAxisForOrbitalPeriod(kerbin.siderealDay*0.5)
    sat = orbit.Satellite(kerbin,1)
    sat.mass = 1
    sat.set_position(np.array([100000.,0.]))
    sat.velocity= np.array([0.,-3000.])
    return kerbin,sat#     sat.orbit.simulate()

def centerOfWindow():
    info = pg.display.Info()
    return [int(info.current_w*0.5),int(info.current_h*0.5)]

def sizeOfWindow():
    info = pg.display.Info()
    return [info.current_w,info.current_h]

def posToPix(pos):
    
    sz = sizeOfWindow()
    ctr = centerOfWindow()
    pix = [int(p/1000.)+ctr[i] for i,p in enumerate(pos)]
    
    print pix
    return pix

kerbin,sat=setup()

pg.init()
screen = pg.display.set_mode((500,500))
inf=pg.display.Info()
print inf.current_w

white = 255,255,255
black =0,0,0
blue = 0,0,255
done = False
clock = pg.time.Clock()




while done == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pg.event.get(): # User did something
        
        if event.type == pg.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    pos = sat.step()
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    screen.fill(black)
    pg.draw.circle(screen,blue,centerOfWindow(),10)
    pg.draw.circle(screen, white, posToPix(pos), 2)
    pg.display.flip()
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Limit to 20 frames per second
    clock.tick(20)