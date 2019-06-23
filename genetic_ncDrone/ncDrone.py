import pygame
import util
import math
import random
import numpy as np
from functools import reduce
import statistics
import copy
class Drone:
    def __init__(self,x = 0 , y=0,manouvers = 0,direction = (0,0),time_base = False, time_threshold = 0,communication_strategy = False):
        self.x = x
        self.y = y
        self.posBoard = ((x*19) +5,(y*19) +5)
        self.direction = direction
        self.manouvers = manouvers
        self.time_base = time_base
        self.time_threshold = time_threshold
        self.communication_strategy = communication_strategy
        self.path_water = []
        self.watershed_mode = False
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
    def move(self,grid,tick,grid_aux):
        if(self.y != -1 and self.x!= -1):
            grid[self.y][self.x].color=1
        if len(self.path_water)>0:
            #for i in self.path_water:
             #   grid[i.x][i.y].color = 1
            #self.getSucessor(grid = grid,grid_aux = [])
            if self.path_water[-1].occupied== False:
                path = self.path_water.pop(-1)
                x = self.y
                y = self.x
                if x+1 == path.x:
                    path.dir_from_drone = (1,0)
                if x-1 == path.x:
                    path.dir_from_drone = (0,1)
                if y+1 == path.y:
                    path.dir_from_drone = (1,1)
                if y-1 == path.y:
                    path.dir_from_drone = (1,0)
                path.cost = abs((self.direction[0]-path.dir_from_drone[0]) + (self.direction[1]-path.dir_from_drone[1]))
               # print('cost',path.cost)
                sucessors = [path]
            else:
                sucessors = []

        else:
            self.watershed_mode = False
            if self.time_base == True:
                sucessors = self.get_sucessor_time_base(grid,grid_aux)
            
            else :
                if self.communication_strategy:
                    sucessors = self.getSucessor(grid = grid_aux,grid_aux = grid)
                else : 
                    sucessors = self.getSucessor(grid = grid,grid_aux = grid_aux)
        if len(sucessors)==0:
            return grid,grid_aux

      
        sucessor = random.choice(sucessors)
        sucessor.occupied = True
        sucessor.visites+=1
        sucessor.u_value = sucessor.visites

        if self.communication_strategy:
            grid_aux[self.y][self.x].occupied = False
            grid[self.y][self.x].occupied = False
            grid[sucessor.x][sucessor.y].occupied = True
        else:
           
            grid[self.y][self.x].occupied = False

        self.manouvers+=sucessor.cost
        self.direction = sucessor.dir_from_drone
        self.x = sucessor.y
        self.y = sucessor.x
        grid[self.y][self.x].intervals.append(tick -grid[self.y][self.x].visita_anterior)
        grid[self.y][self.x].visita_anterior = tick
        self.posBoard = [(self.x*19) +5,(self.y*19) +5] 
        #decrase_uvalue(grid,self.feromone_value)
        return grid,grid_aux
    def getSucessor(self,grid,grid_aux):
        x = self.y
        y = self.x
        sucessors = []
        new_sucessors = []
        if  valide(x+1,y,grid,grid_aux):
            grid[x+1][y].dir_from_drone = (1,0)
            sucessors.append(grid[x+1][y])
        if valide(x-1,y,grid,grid_aux):
            grid[x-1][y].dir_from_drone = (0,1)
            sucessors.append(grid[x-1][y])
        if valide(x,y+1,grid,grid_aux):
            grid[x][y+1].dir_from_drone = (1,1)
            sucessors.append(grid[x][y+1])
        if valide(x,y-1,grid,grid_aux):
            grid[x][y-1].dir_from_drone = (0,0)
            sucessors.append(grid[x][y-1])
        if len(sucessors)==0:
            return []
        minimum_uvalue = min(sucessors,key = lambda x: x.u_value).u_value
        new_sucessors = list(filter(lambda x : x.u_value <= minimum_uvalue,sucessors))
        for suc in new_sucessors:
            suc.cost = abs((self.direction[0]-suc.dir_from_drone[0]) + (self.direction[1]-suc.dir_from_drone[1]))

        cost =  min(new_sucessors, key = lambda x: x.cost).cost
        new_sucessors = list(filter(lambda x : x.cost <= cost,new_sucessors))
        return new_sucessors
        
    def get_sucessor_time_base(self,grid,grid_aux):
        sucessors = self.getSucessor(grid,grid_aux)
        if len(sucessors)>1:
            if(abs(sucessors[0].visita_anterior - sucessors[1].visita_anterior)>=self.time_threshold ):
                
                min_visita = min(sucessors,key = lambda x: x.visita_anterior).visita_anterior
                   # sucessor = min(sucessors,key = lambda x: x.visita_anterior)
                sucessors = list(filter(lambda x : x.visita_anterior <= min_visita,sucessors))
            
        return (sucessors)
        
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
        self.occupied = False
        
class watershed:

    def __init__(self, checked = [],to_visited = [],chosen_drone = None):
        self.checked = checked
        self.to_visited = to_visited
        self.done = True
        self.cluster = []
        self.chosen_drone = chosen_drone
        self.water_threshold = 0
    def check_empty(self,grid):
        grid_size = 50
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j].color == 2:
                    return True

        return False

    def check(self,grid,grid_aux,drones):
        f_avg = 0
        frequencies = []
        below_avg = []
        cluster = []
        found = False
     
        if self.check_empty(grid):

            return grid
      
        self.cluster.clear()

        for row in grid:
            for column in row:
                frequencies.append(column.visites)
                #frequencies.append(column.visita_anterior)

        f_avg = int(statistics.mean(frequencies))
        #print('f_avg',f_avg)
        for row in grid:
            for column in row:
                if column.visites+self.water_threshold < f_avg:
                #if column.visita_anterior+ self.water_threshold < f_avg:
                   below_avg.append(column)
                   found = True

        if found == False:
            return grid
        all_clusters = []
       
        for below in below_avg:
            self.to_visited = []
            if below not in self.checked:
                self.to_visited.append(below)
                cluster = []
                while len(self.to_visited)>0:
                    next_patch = self.to_visited.pop(0)
                    cluster.append(next_patch)
                    self.get_neighbours(next_patch = next_patch,grid = grid,cluster = cluster,f_avg = f_avg,grid_aux = grid_aux)

            
                all_clusters.append(cluster)


        self.to_visited.clear()
        self.checked.clear()

        
       # self.cluster = list(filter(lambda x: len(x)<=50,all_clusters))
        self.cluster =  max(all_clusters,key = len)
        if len(self.cluster)==0:
           # self.cluster =  max(self.cluster,key = len)
            return grid        
       # self.cluster =  max(self.cluster,key = len)
        #print(len(self.cluster))
        clus = random.choice(self.cluster)

        myDrones = list(filter(lambda x: x.watershed_mode == False,drones))
        if len(myDrones)== 0 :
           return grid
        for c in self.cluster:
           grid[c.x][c.y].color = 2
             
        chosen_drone = min(myDrones,key = lambda drone: euclidian_distance(drone.y,drone.x,clus.x,clus.y))
        grid = self.get_path_to_cluster(drone = chosen_drone,cluster = clus,grid = grid)
       
        self.done = False
    
        return grid
    def get_path_to_cluster(self,drone,cluster,grid):
        x_total=  cluster.x - drone.y 
        y_total = cluster.y - drone.x
       # path_water = [] 
        for i in range(abs(x_total)):
            if(x_total)<0:
                k = i
            else:
                k = -i 
            drone.path_water.append(grid[cluster.x+k][cluster.y])
        for i in range(abs(y_total)):
            if y_total <0:
                k = i
            else :
                k= -i
            drone.path_water.append(grid[drone.y][cluster.y+k])
        return grid



    def get_neighbours(self,next_patch,grid,cluster,f_avg,grid_aux):
        neighbours = []
        x = next_patch.x
        y = next_patch.y 
        if next_patch in self.checked:
            return

        self.checked.append(next_patch)

        if  valide(x+1,y,grid,grid_aux) and grid[x+1][y] not in self.to_visited and grid[x+1][y] not in cluster and grid[x+1][y].visites+self.water_threshold<f_avg  :
            self.to_visited.append(grid[x+1][y])
        if  valide(x-1,y,grid,grid_aux) and grid[x-1][y] not in self.to_visited and grid[x-1][y] not in cluster and grid[x-1][y].visites+self.water_threshold<f_avg:
            self.to_visited.append(grid[x-1][y])
        if  valide(x+1,y+1,grid,grid_aux) and grid[x+1][y+1] not in self.to_visited and grid[x+1][y+1] not in cluster and grid[x+1][y+1].visites+self.water_threshold<f_avg:
            self.to_visited.append(grid[x+1][y+1])
        if  valide(x-1,y-1,grid,grid_aux) and grid[x-1][y-1] not in self.to_visited and grid[x-1][y-1] not in cluster and grid[x-1][y-1].visites+self.water_threshold<f_avg:
            self.to_visited.append(grid[x-1][y-1])
        if  valide(x+1,y-1,grid,grid_aux) and grid[x+1][y-1] not in self.to_visited and grid[x+1][y-1] not in cluster and grid[x+1][y-1].visites+self.water_threshold<f_avg:   
            self.to_visited.append(grid[x+1][y-1])
        if  valide(x-1,y+1,grid,grid_aux) and grid[x-1][y+1] not in self.to_visited and grid[x-1][y+1] not in cluster and grid[x-1][y+1].visites+self.water_threshold<f_avg:
            self.to_visited.append(grid[x-1][y+1])
        if  valide(x,y+1,grid,grid_aux) and grid[x][y+1] not in self.to_visited and grid[x][y+1] not in cluster and grid[x][y+1].visites+self.water_threshold<f_avg:    
            self.to_visited.append(grid[x][y+1])
        if  valide(x,y-1,grid,grid_aux) and grid[x][y-1] not in self.to_visited and grid[x][y-1] not in cluster and grid[x][y-1].visites+self.water_threshold<f_avg:
            self.to_visited.append(grid[x][y-1])

               

        return


def euclidian_distance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2) +((y1-y2)**2))
def decrase_uvalue(grid,feromone_value):
    for row in grid:
        for column in row:
           #print("u_value", column.u_value)
            column.u_value -= feromone_value   
    return grid


    return
def valide(x,y,grid,grid_aux):
    
    if (x <0 or x >49 or y <0 or y> 49):
        return False
    if grid[x][y].color==3:
        return False
    #if grid[x][y] in in_cluster:
     #   return True
    if grid[x][y].occupied:
        return False
    if len(grid_aux)>0:
        if grid_aux[x][y].occupied:
            return False
    #if len(in_cluster)>0:
     #   if grid[x][y] not in in_cluster:
      #      return False

    return True 


def sdf(grid):
    sdf = 0
    frequencies = []
    for row in grid:
        #aux  =list(filter(lambda x: x.color != 3 ,row))   
        for column in row:
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
        #aux  =list(filter(lambda x: x.color != 3 ,row))     
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
        #aux  =list(filter(lambda x: x.color != 3 ,row))            
        minimo = min(row, key = lambda x : x.visites ).visites
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
def tick_to_go(tick,k):
    if tick>=k:
        return True
    return False


def update_grid(grid,grids):
    grid_size = 50
    u_value_total =  0 
    visites_total = 0
   # grid = []
    grid1 = grids[0]
    grid2 = grids[1]
    grid3 = grids[2]
    grid4 = grids[3]
    for i in range(grid_size):
        for j in range(grid_size):
            grid[i][j].visites += (grid1[i][j].visites - grid[i][j].visites) + (grid2[i][j].visites - grid[i][j].visites) + (grid3[i][j].visites-grid[i][j].visites) + (grid4[i][j].visites - grid[i][j].visites) 
            grid[i][j].u_value += (grid1[i][j].u_value - grid[i][j].u_value) + (grid2[i][j].u_value - grid[i][j].u_value) + (grid3[i][j].u_value-grid[i][j].u_value) + (grid4[i][j].u_value - grid[i][j].u_value)
            if grid[i][j].visites >0:
                grid[i][j].color = 1
            #print(grid[i][j].visites)
    #grids.clear()        
    #grids = []
    for i in range(grid_size):
        for j in range(grid_size):
            grids[0][i][j].visites = grid[i][j].visites
            grids[1][i][j].visites = grid[i][j].visites
            grids[2][i][j].visites = grid[i][j].visites
            grids[3][i][j].visites = grid[i][j].visites

            grids[0][i][j].u_value = grid[i][j].u_value
            grids[1][i][j].u_value = grid[i][j].u_value
            grids[2][i][j].u_value = grid[i][j].u_value
            grids[3][i][j].u_value = grid[i][j].u_value
        #grids.append(grid)

    return grid,grids

    

    