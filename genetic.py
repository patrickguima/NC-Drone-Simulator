import pygame
from ncDrone import *
from pygame_run import *
import copy
import random

def fitness(drone,grid,ticks):
    fitness_value = 0
    manouvers,sdf, mqi,ncc = metrics(drone, grid,ticks)
    print(manouvers)
    print(mqi)
    print(sdf)
    print(ncc)
    fitness_value = float(ticks*10/manouvers) + float(ticks/sdf) + float(ticks/sdf) + float(ncc/ticks)
    return fitness_value
def valide_start_point(grid):
    valide = []
    for row in grid:
        aux = []
        
        aux = list(filter(lambda x:x.color !=3,row))
        for i in aux:
            valide.append((i.y,i.x))

    #print(valide)
    return valide







grid_size = 15
grid = []

grid_aux = []
start_points = []
for row in range(grid_size):
    grid.append([])
    for column in range(grid_size):
       
        aux_patch = patch(u_value = 0,x = row,y = column,color = 0,intervals = [0,0],visites = 0)
        grid[row].append(aux_patch)

              # Append a cell

drone  = Drone()
ticks = 1000
grid = select_initial_state(drone,grid,100, run = False)

start_points = valide_start_point(grid)

grid_1 = copy.deepcopy(grid)
grid_2 = copy.deepcopy(grid)
grid_3 = copy.deepcopy(grid)

initial_pos = random.choice(start_points)
initial_direction = random.choice([(0,0),(0,1),(1,0),(1,1)])

print("initial pos: ",initial_pos)

drone  = Drone(x = initial_pos[0],y = initial_pos[1],manouvers = 0, direction =initial_direction,feromone_value = 0.0)

select_initial_state(drone,grid_1,ticks, run = True)
print(fitness(drone,grid_1,ticks -1))





drone  = Drone(x = 0,y = 0,manouvers = 0, direction =(1,1),feromone_value = 0.0)
select_initial_state(drone,grid_2 ,ticks, run = True)
print(fitness(drone,grid_2,ticks -1))
drone  = Drone(x = 0,y = 0,manouvers = 0, direction =(0,0),feromone_value = 0.001)

select_initial_state(drone,grid_3,1000, run = True)

print(fitness(drone,grid_3,ticks -1))