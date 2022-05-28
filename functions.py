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
                imgs2.append(pygame.image.load(path+"/"+i+"/"+j))
            else:
                arr = []
                for dir in os.listdir(path+"/"+i+"/"+j):
                    arr.append(pygame.image.load(path+"/"+i+"/"+j+"/"+dir))
                imgs2.append(arr)

        imgs.append(imgs2)
    
    return imgs

def draw_part(map,imgs):
    
    x = random.randint(0,len(map)-1)
    img = any
    
    randomType = random.randint(0,len(imgs)-1)
    randomImg = random.randint(1,len(imgs)-1)
    
    if randomImg == 4:
        img = imgs[randomType][randomImg][0]
    else:
        img = imgs[randomType][randomImg]
    
    
    return map[x][0],img