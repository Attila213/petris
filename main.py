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

directions = ["down","left","up","right"]
current_block = {
    "pos":[[],[]],
    "img":any,
    "type":any,
    "rect":any,
    "index":any,
    "directions":any
}


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
                current_block["img"] = pygame.transform.rotate(current_block["img"],-90)

                for i in current_block["directions"]:     
                    if i[0] <= 2:
                        i[0] +=1
                    else:
                        i[0] = 0
                                        
            if event.key == pygame.K_DOWN and fun.collide([current_block["index"][0],current_block["index"][1]+1],blocks) == False and current_block["index"][1] < len(map[0])-1:
                current_block["index"][1] += 1

    if falling:
        if frame % 120==0:
            if current_block["index"][1] < len(map[0])-1 and fun.collide([current_block["index"][0],current_block["index"][1]+1],blocks) == False: 
                current_block["index"][1] += 1
            else:
                arr = [current_block["type"],current_block["img"],current_block["index"],current_block["rect"],current_block["directions"]]
                blocks.append(arr)
                falling = False   
    else:
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
    #endregion
    
    clock.tick(120)    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    