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
        self.posBoard = [(x*37) +5,(y*37) +5] 
        self.direction = direction
        self.manouvers = manouvers
        self.feromone_value = feromone_value
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

    def move(self,grid,tick):
        grid[self.y][self.x].color=1
        grid[self.y][self.x].visites+=1
        grid[self.y][self.x].u_value = grid[self.y][self.x].visites
        
        grid[self.y][self.x].intervals.append(tick)
       # print(grid[self.y][self.x].intervals)
        sucessor = random.choice(self.getSucessor(grid))
        self.manouvers+=sucessor.cost
        self.direction = sucessor.dir_from_drone
        self.x = sucessor.y
        self.y = sucessor.x
        self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
        decrase_uvalue(grid,self.feromone_value)

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
    
    def __init__(self,u_value = 0,x = None , y=None,color = 0,dir_from_drone = (0,0),cost = 0,intervals = [],visites = 0):
        self.u_value = u_value
        self.x = x
        self.y = y
        self.color = color
        self.dir_from_drone = dir_from_drone
        self.cost = cost
        self.intervals = intervals
        self.visites = visites
      


def decrase_uvalue(grid,feromone_value):
    for row in grid:
        for column in row:
            if column.u_value >0:
                column.u_value -= feromone_value

   # print("u_value ",grid[0][0].u_value)

    return
def valide(x,y,grid):
    if (x <0 or x >14 or y <0 or y> 14):
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
    print("SDF") 
    print(sdf)
    print("media",np.mean(f_avg))
    return sdf
    
def mqi(grid,tick):
    mqi = 0
    interval =0 
    print("MQI: ")

    for row in grid:
        aux  =list(filter(lambda x: x.color != 3 ,row))     
        for column in aux:
            interval += (reduce((lambda x,y: y-x),column.intervals))**2        
    mqi = math.sqrt(interval/tick)
    print(mqi)
    return mqi

def ncc (grid):
    print("ncc: ")
    min_ncc = []
    aux = []
    minimo = 0
    for row in grid:
        aux = []
        aux  =list(filter(lambda x: x.color != 3 ,row))            
        minimo = min(aux, key = lambda x : x.visites ).visites
        min_ncc.append(minimo)
    print(min(min_ncc))
    ncc = min(min_ncc)
    return ncc
def metrics(drone,grid,tick):
    print("### MATRICS ###")
    print("drone info: ", drone.feromone_value)
    print("number of manouvers :",drone.manouvers)
    sdf_ = sdf(grid)
    mqi_ = mqi(grid,tick)
    ncc_ = ncc(grid)
    return drone.manouvers,sdf_,mqi_,ncc_
def simulation(drone,grid,tick):
    drone.move(grid,tick)

    

    