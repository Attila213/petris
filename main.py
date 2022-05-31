from dis import dis
import pygame,sys,os,time

import functions as fun
import FONT
from FONT import Font as myfont
pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = [700,700]
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((150,150))

pygame.display.set_caption("PETRIS")

map = fun.map_generation((50,10),8)
blocks = []
connections = []

normal_font = myfont('fonts/small_font.png',(0,0,200))
big_font = myfont('fonts/large_font.png',(255,0,0))


aim = pygame.image.load("images/aim.png")
imgs = fun.image_loader("images/pets")
# background = fun.image_loader("images/backround")
 
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

speed = 60
rotate_counter = 0

level = 1
petlength = 2
GAMEOVER = False
GAMEOVER_circle_radius = 0


frame = 0
while True:
    frame += 1
    display.fill((30,100,150))
    
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
            if event.key == pygame.K_SPACE:                
                if fun.under_the_current(current_block,blocks,map) is not None:
                    current_block["index"] = [current_block["index"][0],current_block["index"][1]+fun.under_the_current(current_block,blocks,map)-1]
                else:
                    current_block["index"] = [current_block["index"][0],len(map[0])-1]
                
                frame = speed-1
    

    if falling:
        if frame % speed==0:
            if current_block["index"][1] < len(map[0])-1 and fun.collide([current_block["index"][0],current_block["index"][1]+1],blocks) == False: 
                current_block["index"][1] += 1
            elif falling:
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
        
        if GAMEOVER == False:
            current_block["rect"],current_block["img"],current_block["type"],current_block["index"],current_block["directions"] = fun.draw_part(map,imgs)
        
        if fun.collide(current_block["index"],blocks):
            GAMEOVER = True
            falling = None
        else:
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
    

    # aim megrajzolása
    if fun.under_the_current(current_block,blocks,map) != 1 and current_block["index"][1] != len(map[0])-1:
        if fun.under_the_current(current_block,blocks,map) is not None:
            display.blit(aim,(map[current_block["index"][0]][len(map[0])-1].x,map[current_block["index"][0]][current_block["index"][1]+fun.under_the_current(current_block,blocks,map)-1].y))
        else:
            display.blit(aim,(map[current_block["index"][0]][len(map[0])-1].x,map[current_block["index"][0]][len(map[0])-1].y))

    #endregion

    normal_font.render("LEVEL: "+ str(level),display,(10,10),10)
    normal_font.render("LENGTH: "+ str(petlength),display,(10,20),10)

    
    

    if GAMEOVER:
        # valami baszó animációt.pl amikor a közeéétőle egy fekete kör egyre nagyobb lesz
        if frame % 1 == 0 and GAMEOVER_circle_radius < 150:
            GAMEOVER_circle_radius += 1
            level = 1
            petlength = 2
            
            
        pygame.draw.circle(display,(0,0,0),(75,75),GAMEOVER_circle_radius)
        big_font.render("GAME OVER",display,(45,60),10)
        
    clock.tick(120)    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    