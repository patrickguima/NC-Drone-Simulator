import pygame
from ncDrone import *
from pygame_run import *
import copy
import random
from dataxlsm import *



def valide_start_point(grid):
    valide = []
    for row in grid:
        aux = []
        
        aux = list(filter(lambda x:x.color !=3,row))
        for i in aux:
            valide.append((i.y,i.x))

    #print(valide)
    return valide

def generate_population(size):

    population = []
    for i in range(size):
        evap_time = random.randrange(1,1000)
        evap_factor = random.uniform(0,0.5)
        population.append([evap_time,evap_factor])

    return population

def go():
    evap_time = 627
    evap_factor = 0.1784375
    threshold = 266
    #evap_time = int(evap_time)
    grid_size = 50
    initial_grid = []

    for row in range(grid_size):
        initial_grid.append([])
        for column in range(grid_size):     
            aux_patch = patch(u_value = 0,x = row,y = column,color = 0,intervals = [ ],visites = 0,visita_anterior = 0)
            initial_grid[row].append(aux_patch)

                  # Append a cell


    ticks =10000
    metrics_results = []
    metrics_results2 = []

    simulation_on_screen = False

    #initial_population = generate_population(10)
    #print(initial_population)


    for i in range(30):
        grid = []
        grid = copy.deepcopy(initial_grid)
        drones  = []
        drone  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),time_base = True,time_threshold = threshold)
        drone2  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),time_base = True,time_threshold = threshold)
        drone3  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),time_base = True,time_threshold = threshold)
        drone4  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),time_base = True,time_threshold = threshold)
        drones.append(drone)
        drones.append(drone2)
        drones.append(drone3)
        drones.append(drone4)
       # grid = select_initial_state(drones = drones,grid = grid ,ticks = ticks, run = False)
        #grid = select_initial_state(drones = drones,grid = grid ,ticks = ticks, run = False)

        #select_initial_state(drones = drones, grid = grid, ticks = ticks, run = True)
        if simulation_on_screen:
            select_initial_state(drones = drones, grid = grid, ticks = ticks, run = True)
        else:    
            for tick in range(ticks):
                grid = drones[0].move(grid,tick)
                        #simulation(drones[0],grid,tick)
                if tick != 0 :
                    grid = drones[1].move(grid,tick)
                        
                if tick != 0 and tick != 1 :
                    grid = drones[2].move(grid,tick) 

                if tick != 0 and tick != 1 and tick != 2 :
                    grid = drones[3].move(grid,tick)


                #if tick%evap_time == 0:
                 #   grid = decrase_uvalue(grid = grid,feromone_value = evap_factor)

        #print("numero de manobras")
        #print("drone 1 - ",drones[0].manouvers)
        #print("drone 2 - ",drones[1].manouvers)
        #print("drone 3 - ",drones[2].manouvers)
       # print("drone 4 - ",drones[3].manouvers)
        soma_manobras = drones[0].manouvers + drones[1].manouvers + drones[2].manouvers+ drones[3].manouvers
        qmi,sdf,ncc =  metrics(grid,ticks)
        print("qmi: ",qmi)
        print("sdf: ",sdf)
        print("ncc: ",ncc)
        #num = 0
        metrics_results.append([i,qmi,sdf,ncc,soma_manobras])
    ##print(fitness(drone,grid,ticks))
        #print(metrics_results)


        

    write_xlsm(metrics_results)


#numero de agentes, tempo entre evaporaçoes, posiçao inicial e taxa de evaporaçao
#começar tempo entre evaporaçao e taxa de evaporação. testar tempos no time base strategy na escolha de empate  

#cromossomo []





if '__main__' == __name__:
    go()