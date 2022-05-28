import pygame,sys,os

def map_generation(surface,startpos,size):
    map = []
    x= startpos[0]
    y= startpos[1]
    for i in range(10):
        for j in range(15):
            r = pygame.Rect(x+ i*(size),y+j*(size),size,size)
            map.append(r)
    return map