import pygame
from ncDrone import *
from pygame_run import *
import copy
import random
from dataxlsm import *
import numpy as np


def valide_start_point(grid):
    valide = []
    for row in grid:
        aux = []
        
        aux = list(filter(lambda x:x.color !=3,row))
        for i in aux:
            valide.append((i.y,i.x))

    #print(valide)
    return valide





def go():
  

    #NUMERO DE TICKS
    ticks =10000
    #ESTRATEGIAS ADOTADAS
    simulation_on_screen = False
    time_strategy = False
    communication_strategy = True
    evaporation_strategy = False
    watershed_strategy = False
    

    #PARAMETROS DE SIMULAÇAO
    evap_time = 1
    evap_factor =  0.328
    threshold_time = 34
    watershed_time = 1
    communication_time = 50
    number_drones = 4
    #INICIALIZAÇAO
    water = watershed()
    water.water_threshold = 895
    metrics_results = []
    grid_size = 50
    initial_grid = []

    for row in range(grid_size):
        initial_grid.append([])
        for column in range(grid_size):     
            aux_patch = patch(u_value = 0,x = row,y = column,color = 0,intervals = [ ],visites = 0,visita_anterior = 0)
            initial_grid[row].append(aux_patch)

                  


    for i in range(30):
        water = watershed()
        grid = []
        grids = []
        grid = copy.deepcopy(initial_grid)
        if communication_strategy == True:    
            for j in range(number_drones):
                grids.append(copy.deepcopy(initial_grid))
            
        drones  = []
        for num in range(number_drones):
            drone  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
            drones.append(drone)

        if simulation_on_screen:
            select_initial_state(drones = drones, grid = grid,grids = grids,ticks = ticks, run  = True ,communication_strategy = communication_strategy)
        else:    
            for tick in range(ticks):
               # print(tick)
                if communication_strategy == True:
                   

                    for k,drone in enumerate(drones):
                        if tick_to_go(tick,k):
                            grid,grids[k] = drone.move(grid = grid,tick = tick,grid_aux = grids[k])

                    if tick %communication_time ==0:       
                        grid,grids = update_grid(grid,grids) 
                else:
                    for k,drone in enumerate(drones):
                        if tick_to_go(tick,k):
                            grid,_ = drone.move(grid = grid,tick = tick,grid_aux = [])
                   
                if evaporation_strategy:
                    if tick%evap_time == 0:
                        grid = decrase_uvalue(grid = grid,feromone_value = evap_factor)
                
                if watershed_strategy:   
                    if tick%watershed_time==0:
                        grid = water.check(grid = grid,grid_aux = [],drones = drones)

        soma_manobras = 0      
        for drone in drones:
            soma_manobras += drone.manouvers
        qmi,sdf,ncc =  metrics(grid,ticks)
        print("qmi: ",qmi)
        print("sdf: ",sdf)
        print("ncc: ",ncc)
        print("manobras",soma_manobras)
        metrics_results.append([i,qmi,sdf,ncc,soma_manobras])


        

    write_xlsm(metrics_results)
    return


#numero de agentes, tempo entre evaporaçoes, posiçao inicial e taxa de evaporaçao
#começar tempo entre evaporaçao e taxa de evaporação. testar tempos no time base strategy na escolha de empate  

#cromossomo []





if '__main__' == __name__:
    go()