from cgi import print_arguments, print_directory
from dis import dis
from doctest import FAIL_FAST
import pygame,sys,os,time
import functions as fun
pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = [700,700]
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((150,150))

pygame.display.set_caption("PETRIS")


map = fun.map_generation((50,10),8)
blocks = []
imgs = fun.image_loader()

falling = False
current_block = {
    "pos":[[],[]],
    "img":any,
    "type":any,
    "rect":any,
    "index":any
}


frame = 0
run = True
while run:
    last_move = any


    frame += 1
    display.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_block["index"][0] > 0:
                # meg kell nézni hogy ahova ez a move vezet, ott van-e már valami
                current_block["index"][0] -= 1
            if event.key == pygame.K_RIGHT and current_block["index"][0] < len(map)-1:
                current_block["index"][0] += 1

    
    if falling:
        
        collide = False
        for i in blocks:
            #ha a következő esés indexe szerepel valahol a block listában akkor ütközés igaz
            nextpos = [current_block["index"][0],current_block["index"][1]+1]
            if i[2] == nextpos:
                collide = True
        
        # ha 120-al osztható a frame akkor
        if frame % 30==0:
            if current_block["index"][1] < len(map[0])-1 and collide == False: 
                current_block["index"][1] += 1
            else:
                arr = [current_block["type"],current_block["img"],current_block["index"],current_block["rect"]]
                blocks.append(arr)
                falling = False

        
    else:
        current_block["rect"],current_block["img"],current_block["type"],current_block["index"] = fun.draw_part(map,imgs)
        falling = True
        
    
    

                
    
        
    
    # a játékteret rajzolja meg
    for i in map:
        for j in i:
            pygame.draw.rect(display,(255,255,255),j)
    
    # a megrajzolja a bockban található rectet és a hozzá tartozó részt
    for i in blocks:
        display.blit(i[1],(map[i[2][0]][i[2][1]].x,map[i[2][0]][i[2][1]].y))
    
    current_block["pos"] = [map[current_block["index"][0]][current_block["index"][1]].x,map[current_block["index"][0]][current_block["index"][1]].y]
    current_block["rect"] = pygame.Rect(current_block["pos"][0],current_block["pos"][1],8,8)
    pygame.draw.rect(display,(0,0,0),current_block["rect"])    

    # megrajzolj a formát valós időben
    display.blit(current_block["img"],(current_block["pos"][0],current_block["pos"][1]))

    clock.tick(120)    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    