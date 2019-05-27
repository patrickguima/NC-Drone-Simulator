import pygame
from ncDrone import *
from pygame_run import *
import copy
import random
from dataxlsm import *

def fitness(drone,grid,ticks):
    fitness_value = 0
    manouvers,sdf, mqi,ncc = metrics(drone, grid,ticks)
    #print(manouvers)
    #print(mqi)
    #print(sdf)
    #print(ncc)
    fitness_value = float(ticks/manouvers*10) + float(ticks/sdf) + float(ticks/sdf) + float(ncc/ticks)
    return [manouvers,sdf,mqi,ncc, fitness_value]




def valide_start_point(grid):
    valide = []
    for row in grid:
        aux = []
        
        aux = list(filter(lambda x:x.color !=3,row))
        for i in aux:
            valide.append((i.y,i.x))

    #print(valide)
    return valide







grid_size = 50
initial_grid = []

for row in range(grid_size):
    initial_grid.append([])
    for column in range(grid_size):     
        aux_patch = patch(u_value = 0,x = row,y = column,color = 0,intervals = [0,0],visites = 0)
        initial_grid[row].append(aux_patch)

              # Append a cell


ticks =10000
metrics_results = []
metrics_results2 = []

#for i in range(10):
 #   grids.append(copy.deepcopy(grid))
#grids.append(copy.deepcopy(grid))
#grids.append(copy.deepcopy(grid))
    


for i in range(30):
    grid = []
    grid = copy.deepcopy(initial_grid)
    drones  = []
    drone  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),feromone_value = 0.0)
    drone2  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),feromone_value = 0.0)
    drone3  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),feromone_value = 0.0)
    drone4  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),feromone_value = 0.0)



    drones.append(drone)
    drones.append(drone2)
    drones.append(drone3)
    drones.append(drone4)
#grid = select_initial_state(drones = drones,grid = grid ,ticks = ticks, run = False)

    #select_initial_state(drones = drones, grid = grid, ticks = ticks, run = True)
    for tick in range(ticks):
        grid = drones[0].move(grid,tick)
                    #simulation(drones[0],grid,tick)
        if tick != 0 :
            grid = drones[1].move(grid,tick)
                    
        if tick != 0 and tick != 1 :
            grid = drones[2].move(grid,tick) 

        if tick != 0 and tick != 1 and tick != 2 :
            grid = drones[3].move(grid,tick)


    print("numero de manobras")
    print("drone 1 - ",drones[0].manouvers)
    print("drone 2 - ",drones[1].manouvers)
    print("drone 3 - ",drones[2].manouvers)
    print("drone 4 - ",drones[3].manouvers)
    soma_manobras = drones[0].manouvers + drones[1].manouvers + drones[2].manouvers+ drones[3].manouvers
    qmi,sdf,ncc =  metrics(grid,ticks)
    print("qmi: ",qmi)
    print("sdf: ",sdf)
    print("ncc: ",ncc)
    #num = 0
    metrics_results.append([i,qmi,sdf,ncc,soma_manobras])
##print(fitness(drone,grid,ticks))
    print(metrics_results)


write_xlsm(metrics_results)


#numero de agentes, tempo entre evaporaçoes, posiçao inicial e taxa de evaporaçao