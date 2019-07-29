import pygame
from ncDrone import *
from pygame_run import *
import copy
import random
from dataxlsm import *
import numpy as np
import time

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
    simulation_on_screen = True
    time_strategy =False
    evaporation_strategy = False
    quandrant_strategy = False

    #PARAMETROS DE SIMULAÇAO
    evap_time = 1
    evap_factor =  0.83
    threshold_time = 0
    num_simulations = 30
    #NUMERO DE VANTs
    number_drones = 4

    #TRUE PARA RODAR E FALSE PARA RODAR PASSO A PASSO 
    run = True


    #OUTRAS ESTRATEGIAS QUE FORAM DESCARTADAS
    communication_strategy = False
    watershed_strategy = False
    type_A = True
    watershed_time = 0
    communication_time = 0
    water_threshold =0

   
    #INICIALIZAÇAO
    #water = watershed(water_threshold = water_threshold,communication_strategy = communication_strategy)
    #water.water_threshold = 0
    #water.communication_strategy = communication_strategy
    metrics_results = []
    grid_size = 50
    initial_grid = []

    for row in range(grid_size):
        initial_grid.append([])
        for column in range(grid_size):     
            aux_patch = patch(u_value = 0,x = row,y = column,color = 0,intervals = [],visites = 0,visita_anterior = 0)
            initial_grid[row].append(aux_patch)


    for i in range(num_simulations):
        grid = []
        grids = []
        grid = copy.deepcopy(initial_grid)


        #ADCIONAR OBSTACULOS (BASTA DESCOMENTAR)

        #make_obstacles1(grid)
        #make_obstacles2(grid)
        #make_obstacles3(grid)
        if communication_strategy == True:    
            for j in range(number_drones):
                grids.append(copy.deepcopy(initial_grid))
            
        drones  = []
        if quandrant_strategy:
            if type_A:
                drone  = Drone(x = -1,y = 49,label = 1,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drone1  = Drone(x = -1,y = 49,label = 2,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drone2  = Drone(x = -1,y = 49,label = 3,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drone3  = Drone(x = -1,y = 49,label = 4,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                grid = get_path_to_cluster(drone1,grid[20][0],grid)
                grid  = get_path_to_cluster(drone2,grid[24][49],grid)
                grid = get_path_to_cluster(drone3,grid[24][49],grid)
            else:
                drone  = Drone(x = -1,y = 49,label = 1,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drone1  = Drone(x = -1,y = 0,label = 2,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drone2  = Drone(x = 50,y = 0,label = 3,manouvers = 0, direction =(0,0),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drone3  = Drone(x = 50,y = 49,label = 4,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
            
            
            drones.append(drone)
            drones.append(drone1)
            drones.append(drone2)
            drones.append(drone3)
        else:
            for num in range(number_drones):
                drone  = Drone(x = -1,y = 49,label = None,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drones.append(drone)

        

        if simulation_on_screen:
            select_initial_state(drones = drones, grid = grid,grids = grids,ticks = ticks, run  =run   ,communication_strategy = communication_strategy, evap_strategy = evaporation_strategy, et = evap_time, ef = evap_factor)

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
                        if communication_strategy:
                            for j in range(number_drones):
                                grids[j] = water.check(grid = grids[i],grid_aux = [],drones = drones[j])
                        else:
                            grid = water.check(grid = grid,grid_aux = [],drones = drones)

        #size_obstacles(grid)
        soma_manobras = 0      
        for drone in drones:
            soma_manobras += drone.manouvers
        qmi,sdf,ncc =  metrics(grid,ticks)
        print("qmi: ",qmi)
        print("sdf: ",sdf)
        print("ncc: ",ncc)
        print("manobras",soma_manobras)
        metrics_results.append([i,qmi,sdf,ncc,soma_manobras])
        grid.clear()
        drones.clear()
        if communication_strategy:
            for i in range(number_drones):
                grids[i].clear()
        

    write_xlsm(metrics_results)
    return








if '__main__' == __name__:
    inicio = time.time()
    go()
    fim = time.time()
    print('tempo de execução = ',fim - inicio)