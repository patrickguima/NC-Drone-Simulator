import pygame
import util
import math
import random
import numpy as np
from functools import reduce
class Drone:
    def __init__(self,x = 0 , y=1,manouvers = 0,direction = (0,0),feromone_value = 0):
        self.x = x
        self.y = y
        self.posBoard = ((x*19) +5,(y*19) +5)
        self.direction = direction
        self.manouvers = manouvers
        self.feromone_value = feromone_value
        self.fitness = 0
    def moveRight(self):
        if(self.x <14):
            self.x+=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
    def moveLeft(self):
        if(self.x >0):
            self.x-=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
    def moveUp(self):
        if(self.y >0):
            self.y-=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
    def moveDown(self):
        if(self.y <14):
            self.y+=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5]
    def getBoardPos(self):

        return self.posBoard
    def move(self,grid,tick):
        if(self.y != -1 and self.x!= -1):
            grid[self.y][self.x].color=1
            #grid[self.y][self.x].visites+=1
            #grid[self.y][self.x].u_value +=1
        
            grid[self.y][self.x].intervals.append(tick -grid[self.y][self.x].visita_anterior)
            grid[self.y][self.x].visita_anterior = tick
        sucessor = random.choice(self.getSucessor(grid))
        sucessor.u_value+=1
        sucessor.visites+=1
        self.manouvers+=sucessor.cost
        self.direction = sucessor.dir_from_drone
        self.x = sucessor.y
        self.y = sucessor.x
        self.posBoard = [(self.x*19) +5,(self.y*19) +5] 
        #decrase_uvalue(grid,self.feromone_value)
        return grid
    def getSucessor(self,grid):
        x = self.y
        y = self.x
        sucessors = []
        new_sucessors = []
        if  valide(x+1,y,grid):
            grid[x+1][y].dir_from_drone = (1,0)
            sucessors.append(grid[x+1][y])
        if valide(x-1,y,grid):
            grid[x-1][y].dir_from_drone = (0,1)
            sucessors.append(grid[x-1][y])
        if valide(x,y+1,grid):
            grid[x][y+1].dir_from_drone = (1,1)
            sucessors.append(grid[x][y+1])
        if valide(x,y-1,grid):
            grid[x][y-1].dir_from_drone = (0,0)
            sucessors.append(grid[x][y-1])
   
        minimum_uvalue = min(sucessors,key = lambda x: x.u_value).u_value
        new_sucessors = list(filter(lambda x : x.u_value <= minimum_uvalue,sucessors))
        for suc in new_sucessors:
            suc.cost = abs((self.direction[0]-suc.dir_from_drone[0]) + (self.direction[1]-suc.dir_from_drone[1]))

        cost =  min(new_sucessors, key = lambda x: x.cost).cost
        new_sucessors = list(filter(lambda x : x.cost <= cost,new_sucessors))
        return new_sucessors

class patch (): 
    
    def __init__(self,u_value = 0,x = None , y=None,color = 0,dir_from_drone = (0,0),cost = 0,intervals = [],visites = 0,visita_anterior = 0):
        self.u_value = u_value
        self.x = x
        self.y = y
        self.color = color
        self.dir_from_drone = dir_from_drone
        self.cost = cost
        self.intervals = intervals
        self.visites = visites
        self.visita_anterior = visita_anterior
      


def decrase_uvalue(grid,feromone_value):
    for row in grid:
        for column in row:
            if column.u_value >0:
                column.u_value -= 0.0   
    return grid
   # print("u_value ",grid[0][0].u_value)

    return
def valide(x,y,grid):
    
    if (x <0 or x >49 or y <0 or y> 49):
        return False
    if grid[x][y].color==3:
       # print("grid ",grid[x][y])
       # print("HERE")
        return False

    return True 


def sdf(grid):
    sdf = 0
    frequencies = []
    for row in grid:
        aux  =list(filter(lambda x: x.color != 3 ,row))   
        for column in aux:
            frequencies.append(column.visites)

    f_avg = np.mean(frequencies)
    for freq in frequencies:
        sdf += (freq - f_avg)**2

    sdf = math.sqrt(sdf / len(frequencies))
    #print("SDF") 
    #print(sdf)
    #print("media",np.mean(f_avg))
    return sdf
    
def qmi(grid,tick):
    qmi = 0
    interval =0 
    #print("MQI: ")
    total_intervals = 0

    total_cells= 0
    for row in grid:
        aux  =list(filter(lambda x: x.color != 3 ,row))     
        for column in aux:
            interval = 0
            total_intervals+= len(column.intervals)
            for i in column.intervals:
                interval+= (i**2)
            total_cells+=interval
                
            #interval += (reduce((lambda x,y: y-x),column.intervals))**2
                   
    qmi = math.sqrt(total_cells/total_intervals)
    #print(qmi)
    return qmi

def ncc (grid):
    #print("ncc: ")
    min_ncc = []
    aux = []
    minimo = 0
    for row in grid:
        aux = []
        aux  =list(filter(lambda x: x.color != 3 ,row))            
        minimo = min(aux, key = lambda x : x.visites ).visites
        min_ncc.append(minimo)
   # print(min(min_ncc))
    ncc = min(min_ncc)
    return ncc
def metrics(grid,tick):
    print("### MATRICS ###")
    sdf_ = sdf(grid)
    qmi_ = qmi(grid,tick)
    ncc_ = ncc(grid)
    return qmi_,sdf_,ncc_

def simulation(drone,grid,tick):
    drone.move(grid,tick)

    

    