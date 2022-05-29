import math
from multiprocessing import connection
from tkinter.tix import Tree
import pygame,sys,os,time
import functions as fun
pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = [700,700]
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((150,150))

pygame.display.set_caption("PETRIS")

aim = pygame.image.load("images/aim.png")

map = fun.map_generation((50,10),8)
blocks = []
connections = []

imgs = fun.image_loader()

falling = False

directions = ["down","left","up","right"]
current_block = {
    "pos":[[],[]],
    "img":any,
    "type":any,
    "rect":any,
    "index":any,
    "directions":any
}


rotate_counter = 0

frame = 0
run = True
while run:
    frame += 1
    display.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_block["index"][0] > 0:
                if fun.collide([current_block["index"][0]-1,current_block["index"][1]],blocks) == False:
                    current_block["index"][0] -= 1
            if event.key == pygame.K_RIGHT and current_block["index"][0] < len(map)-1:
                if fun.collide([current_block["index"][0]+1,current_block["index"][1]],blocks) == False:
                    current_block["index"][0] += 1
            if event.key == pygame.K_UP:
                rotate_counter +=1
                current_block["img"] = pygame.transform.rotate(current_block["img"],-90)
                
                #ha ezekből az eggyik és fejjel lefelé van akkor megfordítja       
                if rotate_counter%2==0 and (current_block["type"][1] == "tail" or current_block["type"][1] == "tail2" or current_block["type"][1] == "head" or current_block["type"][1] == "body"): 
                    current_block["img"] = pygame.transform.flip(current_block["img"],False,True)

                for i in current_block["directions"]:
                    if i[0] <= 2:
                        i[0] +=1
                    else:
                        i[0] = 0                                                    
            if event.key == pygame.K_DOWN and fun.collide([current_block["index"][0],current_block["index"][1]+1],blocks) == False and current_block["index"][1] < len(map[0])-1:
                current_block["index"][1] += 1

    if falling:
        if frame % 50==0:
            if current_block["index"][1] < len(map[0])-1 and fun.collide([current_block["index"][0],current_block["index"][1]+1],blocks) == False: 
                current_block["index"][1] += 1
            else:
                arr = [current_block["type"],current_block["img"],current_block["index"],current_block["rect"],current_block["directions"]]

                #hát ezzzzzgecironda
                
                # ha alatta van valami
                if fun.collide([current_block["index"][0],current_block["index"][1]+1],blocks):
                    r = fun.collideOBJ([current_block["index"][0],current_block["index"][1]+1],blocks)
                    connections = fun.filling_connections(connections,r,arr,current_block,directions,["up","down"])
                
                # ha felette van valami
                if fun.collide([current_block["index"][0],current_block["index"][1]-1],blocks):
                    r = fun.collideOBJ([current_block["index"][0],current_block["index"][1]-1],blocks)
                    connections = fun.filling_connections(connections,r,arr,current_block,directions,["down","up"])
                
                # ha balra van valami
                if fun.collide([current_block["index"][0]+1,current_block["index"][1]],blocks):
                    r = fun.collideOBJ([current_block["index"][0]+1,current_block["index"][1]],blocks)
                    connections = fun.filling_connections(connections,r,arr,current_block,directions,["left","right"])
                
                # ha jobbra van valami
                if fun.collide([current_block["index"][0]-1,current_block["index"][1]],blocks):
                    r = fun.collideOBJ([current_block["index"][0]-1,current_block["index"][1]],blocks)
                    connections = fun.filling_connections(connections,r,arr,current_block,directions,["right","left"])
                
                blocks.append(arr)
                
                # ellenőrizzük hogy meg van e már egy teljes pet
                
                # végigmegyünk a kapcsolatokon
                for i in connections:
                    
                    # létrehozunk egy változót amit akkor állítunk hamisra ha valami befejezetlen
                    done = True
                    
                    # végigmegyünk a kapcsolódott objekteken egyesével
                    for j in i:
                        
                        #végigmegyünk azoknak az irányoknak az igazságértékein
                        for dirbool in j[4]:
                            if dirbool[1] == False:
                                done = False
                    
                    # kivesszük a tömbökből
                    if done:
                        for j in i:
                            for d in blocks:
                                if d==j:
                                    blocks.remove(j)
                        connections.remove(i)

                falling = False   
    else:
        rotate_counter = 0
        current_block["rect"],current_block["img"],current_block["type"],current_block["index"],current_block["directions"] = fun.draw_part(map,imgs)
        falling = True
     
    #region draw some stuff
    # a játékteret rajzolja meg
    for i in map:
        for j in i:
            pygame.draw.rect(display,(255,255,255),j)
    
    # a megrajzolja a bockban található rectet és a hozzá tartozó részt
    for i in blocks:
        display.blit(i[1],(map[i[2][0]][i[2][1]].x,map[i[2][0]][i[2][1]].y))
    
    current_block["pos"] = [map[current_block["index"][0]][current_block["index"][1]].x,map[current_block["index"][0]][current_block["index"][1]].y]
    current_block["rect"] = pygame.Rect(current_block["pos"][0],current_block["pos"][1],8,8)

    # megrajzolj a formát valós időben
    display.blit(current_block["img"],(current_block["pos"][0],current_block["pos"][1]))
    
    # a jelenlegi elem oszlopába és a map utolsó sorába
    
    # ki kell deríteni hogy mi a jelenlegi block alatti block ha van ha nincs akkor map utolsó sora
    aim_rect = pygame.Rect(map[current_block["index"][0]][len(map[0])-1].x,map[current_block["index"][0]][len(map[0])-1].y,8,8)
    
    if fun.under_the_current(current_block,blocks,map) is not None:
        display.blit(aim,(map[current_block["index"][0]][len(map[0])-1].x,map[current_block["index"][0]][current_block["index"][1]+fun.under_the_current(current_block,blocks,map)-1].y))
    else:
        display.blit(aim,(map[current_block["index"][0]][len(map[0])-1].x,map[current_block["index"][0]][len(map[0])-1].y))

    
    #endregion
    
    
    
    clock.tick(120)    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    