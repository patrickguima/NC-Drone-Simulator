import pygame
import util
import math
import random
import numpy as np
from functools import reduce
import statistics
class Drone:
    def __init__(self,x = 0 , y=0,manouvers = 0,direction = (0,0),time_base = False, time_threshold = 0):
        self.x = x
        self.y = y
        self.posBoard = ((x*19) +5,(y*19) +5)
        self.direction = direction
        self.manouvers = manouvers
        self.time_base = time_base
        self.time_threshold = time_threshold
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
            grid[self.y][self.x].intervals.append(tick -grid[self.y][self.x].visita_anterior)
            grid[self.y][self.x].visita_anterior = tick

        if self.time_base == True:
            sucessor = self.get_sucessor_time_base(grid)
            
        else :
            sucessor = random.choice(self.getSucessor(grid))

        sucessor.visites+=1
        #sucessor.u_value+=1
        sucessor.u_value = sucessor.visites
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
        
    def get_sucessor_time_base(self,grid):
        sucessors = self.getSucessor(grid)
        if len(sucessors)>1:
            if(abs(sucessors[0].visita_anterior - sucessors[1].visita_anterior)>=self.time_threshold ):
                
                min_visita = min(sucessors,key = lambda x: x.visita_anterior).visita_anterior
                   # sucessor = min(sucessors,key = lambda x: x.visita_anterior)
                sucessors = list(filter(lambda x : x.visita_anterior <= min_visita,sucessors))
            
        return (random.choice(sucessors))
        
class patch: 
    
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
      
class watershed:

    def __init__(self, checked = [],to_visited = []):
        self.checked = checked
        self.to_visited = to_visited

    def check(self,grid):
        f_avg = 0
        frequencies = []
        below_avg = []
        cluster = []
        found = False

        for row in grid:
            for column in row:
                frequencies.append(column.visites)

        f_avg = int(statistics.mean(frequencies))
        for row in grid:
            for column in row:
                if column.visites < f_avg:
                   below_avg.append(column)
                   found = True

        if found == False:
            return grid
        all_clusters = []
        #print(below_avg.x,below_avg.y)
        for below in below_avg:
            self.to_visited = []
            if below not in self.checked:
                self.to_visited.append(below)
                cluster = []
                while len(self.to_visited)>0:
                    next_patch = self.to_visited.pop(0)
                    cluster.append(next_patch)
                    self.get_neighbours(next_patch = next_patch,grid = grid,cluster = cluster,f_avg = f_avg)

            
                all_clusters.append(cluster)
        cluster = max(all_clusters,key=len)        
        for c in cluster:
            grid[c.x][c.y].color = 2


        self.to_visited = []
        self.checked = []
       
        print(f_avg)
        return grid

    def get_neighbours(self,next_patch,grid,cluster,f_avg):
        neighbours = []
        x = next_patch.x
        y = next_patch.y 
        if next_patch in self.checked:
            return

        self.checked.append(next_patch)

        if  valide(x+1,y,grid) and grid[x+1][y] not in self.to_visited and grid[x+1][y] not in cluster and grid[x+1][y].u_value<f_avg  :
           self.to_visited.append(grid[x+1][y])
        if  valide(x-1,y,grid) and grid[x-1][y] not in self.to_visited and grid[x-1][y] not in cluster and grid[x-1][y].u_value<f_avg:
             self.to_visited.append(grid[x-1][y])
        if  valide(x+1,y+1,grid) and grid[x+1][y+1] not in self.to_visited and grid[x+1][y+1] not in cluster and grid[x+1][y+1].u_value<f_avg:
             self.to_visited.append(grid[x+1][y+1])
        if  valide(x-1,y-1,grid) and grid[x-1][y-1] not in self.to_visited and grid[x-1][y-1] not in cluster and grid[x-1][y-1].u_value<f_avg:
            self.to_visited.append(grid[x-1][y-1])
        if  valide(x+1,y-1,grid) and grid[x+1][y-1] not in self.to_visited and grid[x+1][y-1] not in cluster and grid[x+1][y-1].u_value<f_avg:   
            self.to_visited.append(grid[x+1][y-1])
        if  valide(x-1,y+1,grid) and grid[x-1][y+1] not in self.to_visited and grid[x-1][y+1] not in cluster and grid[x-1][y+1].u_value<f_avg:
            self.to_visited.append(grid[x-1][y+1])
        if  valide(x,y+1,grid) and grid[x][y+1] not in self.to_visited and grid[x][y+1] not in cluster and grid[x][y+1].u_value<f_avg:    
            self.to_visited.append(grid[x][y+1])
        if  valide(x,y-1,grid) and grid[x][y-1] not in self.to_visited and grid[x][y-1] not in cluster and grid[x][y-1].u_value<f_avg:
            self.to_visited.append(grid[x][y-1])

               

        return

def decrase_uvalue(grid,feromone_value):
    for row in grid:
        for column in row:
           #print("u_value", column.u_value)
            column.u_value -= feromone_value   
    return grid


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

    #f_avg = np.mean(frequencies)
    f_avg = statistics.mean(frequencies)
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
        for column in row:
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
#    print("### MATRICS ###")
    sdf_ = sdf(grid)
    qmi_ = qmi(grid,tick)
    ncc_ = ncc(grid)
    return qmi_,sdf_,ncc_

def simulation(drone,grid,tick):
    drone.move(grid,tick)

    

    