import pygame,sys,os

pygame.init()

screen = pygame.display.set_mode((500,500),0,32)
pygame.display.set_caption("PETRIS")


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
            
    
    
    pygame.display.update()