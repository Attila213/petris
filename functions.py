from calendar import c
import pygame,sys,os,random,re

def map_generation(startpos,size):
    map = []
    x= startpos[0]
    y= startpos[1]
    
    for i in range(10):
        arr = []
        for j in range(15):
            r = pygame.Rect(x+ i*(size),y+j*(size),size,size)
            arr.append(r)
        map.append(arr)
    return map

def image_loader():
    
    imgs = []
    path = "images"
    for i in os.listdir(path):
        imgs2 =[]
        imgs2.append(i)
        
        for j in os.listdir(path+"/"+i):
            x = re.search("/*.png",j)       
            if x:
                arr2 = [pygame.image.load(path+"/"+i+"/"+j),j.split('.')[0]]
                imgs2.append(arr2)
            else:
                arr = []
                for dir in os.listdir(path+"/"+i+"/"+j):
                    arr2 = [pygame.image.load(path+"/"+i+"/"+j+"/"+dir),dir.split('.')[0]]
                    arr.append(arr2)
                imgs2.append(arr)
            
        
        imgs.append(imgs2)
    
    return imgs

def draw_part(map,imgs):
    
    x = random.randint(0,len(map)-1)
    img = any
    imgtype = [[],[]]
    
    # sorsol egy random típust
    randomType = random.randint(0,len(imgs)-1)
    # eltárolja a típus nevég
    imgtype[0] = imgs[randomType][0]
    
    # sorsol egy random képet (body,head,tail,corner)
    randomImg = random.randint(1,len(imgs))
    #ha tail akkor az elsőt vegye
    if randomImg == 4:
        img = imgs[randomType][randomImg][0][0]
        imgtype[1] = imgs[randomType][randomImg][0][1]
    else:
        img = imgs[randomType][randomImg][0]
        imgtype[1] = imgs[randomType][randomImg][1]
        
    
    rect = pygame.Rect(map[x][0].x,map[0][0].y,8,8)
    
    #kiszámolja az indexeket
    index = any
    for i in range(len(map)):
        for j in range(len(map[i])):
            if rect.colliderect(map[i][j]):
                index = [i,j]
    
    directions= any
    if imgtype == "body":
        directions = [1,3]
    if imgtype == "corner":
        directions = [0,3]
    if imgtype == "head":
        directions = [3]
    if imgtype == "tail":
        directions = [1]
    
    return rect,img,imgtype,index,directions

def collide(index,blocks):
    collide = False
    for i in blocks:        
        if i[2] == index:
            collide = True
    return collide