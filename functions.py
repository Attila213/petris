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

def draw_part(surface,map,imgs):
    print(len(map))