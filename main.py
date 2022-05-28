from cgi import print_arguments
import pygame,sys,os
import functions as fun
pygame.init()

WINDOW_SIZE = [700,700]
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((150,150))

pygame.display.set_caption("PETRIS")

imgs = fun.image_loader()

map = fun.map_generation((50,10),8)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    

        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()