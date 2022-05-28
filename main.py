import pygame,sys,os,time
import functions as fun
pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = [700,700]
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((150,150))

pygame.display.set_caption("PETRIS")

imgs = fun.image_loader()
map = fun.map_generation((50,10),8)

falling = False
current_block_pos = []
current_block_img = any

frame = 0
run = True
while run:
    frame += 1
    display.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    if falling:
        if frame % 120==0:
            current_block_pos[1] += 8
    else:   
        current_block_pos,current_block_img = fun.draw_part(map,imgs)
        current_block_pos[0] = current_block_pos.x
        current_block_pos[1] = current_block_pos.y

        falling= True
        
        
        

    display.blit(current_block_img,(current_block_pos[0],current_block_pos[1]))

    clock.tick(120)    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    