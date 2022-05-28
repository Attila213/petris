from cgi import print_arguments
from dis import dis
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
    "rect":any
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
            if event.key == pygame.K_LEFT:
                current_block["pos"][0] -= 8
                last_move = "left"
            if event.key == pygame.K_RIGHT:
                current_block["pos"][0] += 8
                last_move = "right"
    
    if falling:
        # ha 60-al osztható a frame akkor
        if frame % 20==0:
            
            collide = fun.collide_block_rects(current_block["rect"],blocks)

            # ha a rect y poziciója egyenlő a legalsó rect y poziciójával akkor
            if current_block["pos"][1] == map[0][len(map[0])-1].y or collide:
                
                # eltárolja a block tömbben
                blocks.append([pygame.Rect(current_block["pos"][0],current_block["pos"][1],8,8),current_block["type"],current_block["img"]])
                falling = False
            else:
                # növeli az y 8-al
                current_block["pos"][1] += 8

    else:
        rect,current_block["img"],current_block["type"] = fun.draw_part(map,imgs)
        current_block["pos"][0] = rect.x
        current_block["pos"][1] = rect.y
        current_block["rect"] = pygame.Rect(current_block["pos"][0],current_block["pos"][1],8,8)
        
        falling= True
        
        
    # a játékteret rajzolja meg
    for i in map:
        for j in i:
            pygame.draw.rect(display,(255,255,255),j)
    
    # a megrajzolja a bockban található rectet és a hozzá tartozó részt
    for i in blocks:
        pygame.draw.rect(display,(0,0,0),i[0])   
        display.blit(i[2],(i[0].x,i[0].y))
    
    
    current_block["rect"] = pygame.Rect(current_block["pos"][0],current_block["pos"][1],8,8)
    collide = fun.collide_block_rects(current_block["rect"],blocks)
    
    if collide and last_move == "right":
        current_block["pos"][0] -= 8
    if collide and last_move == "left":
        current_block["pos"][0] += 8
    
    # megrajzolj a formát valós időben
    pygame.draw.rect(display,(0,0,0),current_block["rect"])
    display.blit(current_block["img"],(current_block["pos"][0],current_block["pos"][1]))

    clock.tick(120)    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    