
import pygame,math,random,sys,os
from pygame.locals import *
import json

class Background:
    poli_array = []
    frame = 0
    window = any
    screen = any
    
    
    def __init__(self,window,screen):
        self.window = window
        self.screen = screen
    
    def updatePoli(self,x):
        x["angle"] += x["rotate_speed"]
        if x["angle"] == 360:
            x["angle"]=0;
        
        points = []
        
        for i in range(0,4):
            temp = []
            temp.append(x["pos"][0] + math.cos(math.radians(x["angle"]+i*90)) * x["size"])
            temp.append(x["pos"][1] + math.sin(math.radians(x["angle"]+i*90)) * x["size"])
            points.append(temp);
        
        x["points"] = points
        x["pos"][1] += x["falling_speed"]/10
        x["size"] -= 0.1
        
        return x;
    
    def addPoli(self):
        if len(self.poli_array) < 15:
                x = {
                    "pos":[random.randint(0,self.window[1]),-100],
                    "size":random.randint(6,20),
                    "angle":random.randint(0,360),
                    "falling_speed":random.randint(50,51),
                    "rotate_speed":random.randint(4,15)/10,
                    "points":any
                    }
                
                self.poli_array.append(x)

        for i in self.poli_array:
            i = self.updatePoli(i)             
    
    def drawPoli(self):
        for i in self.poli_array:
            try:
                pygame.draw.polygon(self.screen,(100,100,100),(i["points"][0],i["points"][1],i["points"][2],i["points"][3]),1)
                if i["pos"][1] > self.window[1]+i["size"] or i["size"] < 0:
                    self.poli_array.remove(i)
            except:
                continue   
    
    def tick(self):
        self.drawPoli()

        self.frame +=1
        if self.frame ==20:
            self.addPoli()
            self.frame  = 0