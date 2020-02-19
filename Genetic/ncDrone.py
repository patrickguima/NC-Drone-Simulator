import pygame
import util
import math
import random
import numpy as np
from functools import reduce
import statistics
import copy
class Drone:
    def __init__(self,x = 0 , y=0,manouvers = 0,direction = (0,0),time_base = False, time_threshold = 0,communication_strategy = False,label = None):
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
        self.label = label
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
        if(self.y != -1 and self.x!= -1 and self.x<50):
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
               path.cost = abs((self.direction[0]-path.dir_from_drone[0]) + abs(self.direction[1]-path.dir_from_drone[1])
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
            if self.x<50:
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
        if  valide(x+1,y,grid,grid_aux,label = self.label):
            grid[x+1][y].dir_from_drone = (1,0)
            sucessors.append(grid[x+1][y])
        if valide(x-1,y,grid,grid_aux,label = self.label):
            grid[x-1][y].dir_from_drone = (0,1)
            sucessors.append(grid[x-1][y])
        if valide(x,y+1,grid,grid_aux,label = self.label):
            grid[x][y+1].dir_from_drone = (1,1)
            sucessors.append(grid[x][y+1])
        if valide(x,y-1,grid,grid_aux,label = self.label):
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

    def __init__(self, checked = [],to_visited = [],chosen_drone = None, water_threshold = 0,communication_strategy = False):
        self.checked = checked
        self.to_visited = to_visited
        self.done = True
        self.cluster = []
        self.chosen_drone = chosen_drone
        self.water_threshold = water_threshold
        self.communication_strategy =communication_strategy
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
        if self.communication_strategy == False:
            myDrones = list(filter(lambda x: x.watershed_mode == False,drones))
            if len(myDrones)== 0 :
                return grid
            chosen_drone = min(myDrones,key = lambda drone: euclidian_distance(drone.y,drone.x,clus.x,clus.y))
        else:
            chosen_drone = drones
        
        grid = self.get_path_to_cluster(drone = chosen_drone,cluster = clus,grid = grid)
        for c in self.cluster:
           grid[c.x][c.y].color = 2
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
def get_path_to_cluster(drone,cluster,grid):
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

def valide(x,y,grid,grid_aux,label = 0):
    
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
    if label == 1:
        if (x<24 or y>24):
            return False

    if label == 2:
        if (x >=24 or y >24):
            return False

    if label == 3:
        if (x >=24 or y <=24):
            return False

    if label == 4:
        if (x <24 or y <=24):
            return False
    #if len(in_cluster)>0:
     #   if grid[x][y] not in in_cluster:
      #      return False

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
    #print(len(frequencies))
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
    #print(total_cells)
    #print(total_intervals)
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

def size_obstacles(grid):
    obs = []
    for row in grid:
        for column in row:
            if column.color ==3:
                obs.append((column.x,column.y))

    
    print(len(obs))
    return
def get_obstacles(grid):
    obs = []
    for row in grid:
        for column in row:
            if column.color ==3:
                obs.append((column.x,column.y))

    
    #print(obs)
    #print(len(obs))
    return
def make_obstacles1(grid):
    obs = [(0, 26), (0, 27), (0, 28), (0, 29), (0, 30), (0, 31), (0, 32), (0, 33), (0, 34), (0, 35), (0, 36), (0, 37), (0, 38), (1, 26), (1, 27), (1, 28), (1, 29), (1, 30), (1, 31), (1, 32), (1, 33), (1, 34), (1, 35), (1, 36), (1, 37), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 26), (2, 27), (2, 28), (2, 29), (2, 30), (2, 31), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 26), (3, 27), (3, 28), (3, 29), (3, 30), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 26), (4, 27), (4, 28), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 26), (5, 27), (5, 28), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 26), (6, 27), (6, 28), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (15, 39), (15, 40), (15, 41), (15, 42), (15, 43), (15, 44), (16, 39), (16, 40), (16, 41), (16, 42), (16, 43), (16, 44), (17, 39), (17, 40), (17, 41), (17, 42), (17, 43), (17, 44), (17, 45), (18, 40), (18, 41), (18, 42), (18, 43), (18, 44), (18, 45), (19, 41), (19, 42), (19, 43), (19, 44), (19, 45), (20, 41), (20, 42), (20, 43), (20, 44), (20, 45), (21, 43), (21, 44), (21, 45), (22, 43), (22, 44), (22, 45), (23, 43), (23, 44), (23, 45), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 43), (24, 44), (25, 9), (25, 10), (25, 11), (25, 12), (25, 13), (25, 14), (25, 43), (25, 44), (26, 9), (26, 10), (26, 11), (26, 12), (26, 13), (26, 14), (27, 9), (27, 10), (27, 11), (27, 12), (27, 13), (27, 14), (28, 9), (28, 10), (28, 11), (29, 9), (29, 10), (29, 11), (30, 9), (30, 10), (30, 11), (31, 10), (31, 11), (41, 15), (41, 16), (41, 17), (41, 18), (41, 19), (41, 20), (41, 21), (41, 22), (41, 23), (41, 24), (41, 25), (41, 26), (41, 27), (41, 28), (42, 12), (42, 13), (42, 14), (42, 15), (42, 16), (42, 17), (42, 18), (42, 19), (42, 20), (42, 21), (42, 22), (42, 23), (42, 24), (42, 25), (42, 26), (42, 27), (42, 28), (43, 11), (43, 12), (43, 13), (43, 14), (43, 15), (43, 16), (43, 17), (43, 18), (43, 19), (43, 20), (43, 21), (43, 22), (43, 23), (43, 24), (43, 25), (43, 26), (43, 27), (43, 28), (44, 12), (44, 13), (44, 14), (44, 15), (44, 16), (44, 17), (44, 18), (44, 19), (44, 20), (44, 21), (44, 22), (44, 23), (44, 24), (44, 25), (44, 26), (44, 27)]
    for ob in obs:
        grid[ob[0]][ob[1]].color=3
    return




def make_obstacles2(grid):
    obs = [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 31), (5, 32), (5, 33), (5, 34), (5, 35), (5, 36), (5, 37), (5, 38), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 31), (6, 32), (6, 33), (6, 34), (6, 35), (6, 36), (6, 37), (6, 38), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 38), (7, 39), (7, 40), (7, 41), (7, 42), (7, 43), (7, 44), (7, 45), (7, 46), (7, 47), (7, 48), (7, 49), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 38), (8, 39), (8, 40), (8, 41), (8, 42), (8, 43), (8, 44), (8, 45), (8, 46), (8, 47), (8, 48), (8, 49), (9, 38), (9, 39), (9, 40), (9, 41), (9, 42), (9, 43), (9, 44), (9, 45), (9, 46), (9, 47), (9, 48), (9, 49), (10, 38), (10, 39), (10, 40), (10, 41), (10, 42), (10, 43), (10, 44), (10, 45), (10, 46), (10, 47), (10, 48), (10, 49), (11, 38), (11, 39), (11, 40), (11, 41), (11, 42), (11, 43), (11, 44), (11, 45), (11, 46), (11, 47), (11, 48), (11, 49), (12, 38), (12, 39), (12, 40), (12, 41), (12, 42), (12, 43), (12, 44), (12, 45), (12, 46), (12, 47), (12, 48), (12, 49), (13, 38), (13, 39), (13, 40), (13, 41), (13, 42), (13, 43), (13, 44), (13, 45), (13, 46), (13, 47), (13, 48), (13, 49), (26, 5), (26, 6), (26, 7), (26, 8), (26, 9), (26, 10), (26, 30), (26, 31), (26, 32), (27, 5), (27, 6), (27, 7), (27, 8), (27, 9), (27, 10), (27, 30), (27, 31), (27, 32), (28, 5), (28, 6), (28, 7), (28, 8), (28, 9), (28, 10), (28, 30), (28, 31), (28, 32), (29, 5), (29, 6), (29, 7), (29, 8), (29, 9), (29, 10), (29, 30), (29, 31), (29, 32), (30, 5), (30, 6), (30, 7), (30, 8), (30, 9), (30, 10), (30, 25), (30, 26), (30, 27), (30, 28), (30, 29), (30, 30), (30, 31), (30, 32), (31, 5), (31, 6), (31, 7), (31, 8), (31, 9), (31, 10), (31, 25), (31, 26), (31, 27), (31, 28), (31, 29), (31, 30), (31, 31), (31, 32), (31, 33), (31, 34), (32, 25), (32, 26), (32, 27), (32, 28), (32, 29), (32, 30), (32, 31), (32, 32), (32, 33), (32, 34), (33, 25), (33, 26), (33, 27), (33, 28), (33, 29), (33, 30), (33, 31), (33, 32), (33, 33), (33, 34), (34, 25), (34, 26), (34, 27), (34, 28), (34, 29), (34, 30), (34, 31), (34, 32), (34, 33), (34, 34)]
    for ob in obs:
        grid[ob[0]][ob[1]].color=3
    return

def make_obstacles3(grid):
    obs = [(0, 0), (0, 1), (0, 2), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 44), (0, 45), (0, 46), (0, 47), (1, 0), (1, 1), (1, 2), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (1, 24), (1, 25), (1, 44), (1, 45), (1, 46), (1, 47), (2, 0), (2, 1), (2, 2), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 23), (2, 24), (2, 25), (2, 45), (2, 46), (2, 47), (3, 0), (3, 1), (3, 2), (3, 14), (3, 15), (3, 16), (3, 17), (3, 23), (3, 24), (3, 25), (3, 45), (3, 46), (3, 47), (4, 0), (4, 1), (4, 2), (4, 14), (4, 15), (4, 16), (4, 17), (4, 23), (4, 24), (4, 25), (4, 45), (4, 46), (4, 47), (5, 0), (5, 1), (5, 2), (5, 14), (5, 15), (5, 16), (5, 17), (5, 23), (5, 24), (5, 25), (6, 14), (6, 15), (6, 16), (6, 17), (6, 23), (6, 24), (6, 25), (7, 14), (7, 15), (7, 16), (7, 17), (7, 23), (7, 24), (7, 25), (22, 21), (22, 22), (22, 23), (22, 24), (22, 25), (23, 17), (23, 18), (23, 19), (23, 20), (23, 21), (23, 22), (23, 23), (23, 24), (23, 25), (23, 26), (24, 17), (24, 18), (24, 19), (24, 20), (24, 21), (24, 22), (24, 23), (24, 24), (24, 25), (24, 26), (25, 17), (25, 18), (25, 19), (25, 20), (25, 21), (25, 22), (25, 23), (25, 24), (25, 25), (25, 26), (25, 27), (26, 18), (26, 19), (26, 20), (26, 21), (26, 22), (26, 23), (26, 24), (26, 25), (26, 26), (26, 27), (27, 19), (27, 20), (27, 21), (27, 22), (27, 23), (27, 24), (27, 25), (27, 26), (36, 37), (36, 38), (36, 39), (37, 37), (37, 38), (37, 39), (38, 7), (38, 8), (38, 9), (38, 10), (38, 11), (38, 12), (38, 13), (38, 37), (38, 38), (38, 39), (39, 6), (39, 7), (39, 8), (39, 9), (39, 10), (39, 11), (39, 12), (39, 13), (39, 37), (39, 38), (39, 39), (40, 6), (40, 7), (40, 8), (40, 9), (40, 10), (40, 11), (40, 12), (40, 13), (40, 37), (40, 38), (40, 39), (40, 40), (40, 41), (40, 42), (40, 43), (40, 44), (40, 45), (41, 6), (41, 7), (41, 8), (41, 9), (41, 10), (41, 11), (41, 12), (41, 13), (41, 37), (41, 38), (41, 39), (41, 40), (41, 41), (41, 42), (41, 43), (41, 44), (41, 45), (42, 6), (42, 7), (42, 8), (42, 9), (42, 10), (42, 11), (42, 12), (42, 13), (42, 37), (42, 38), (42, 39), (42, 40), (42, 41), (42, 42), (42, 43), (42, 44), (42, 45), (43, 7), (43, 8), (43, 9), (43, 10), (43, 11), (43, 12), (43, 13), (43, 37), (43, 38), (43, 39), (43, 40), (43, 41), (43, 42), (43, 43), (43, 44), (43, 45)]
    for ob in obs:
        grid[ob[0]][ob[1]].color=3
    return
