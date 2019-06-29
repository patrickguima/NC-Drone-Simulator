import pygame
from ncDrone import *
from pygame_run import *
import copy
import random
from dataxlsm import *

from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import DecimalIndividual
from gaft.components import Population
from gaft.operators import RouletteWheelSelection
from gaft.operators import TournamentSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitBigMutation
from gaft.operators import FlipBitMutation
# Built-in best fitness analysis.
from gaft.analysis.fitness_store import FitnessStore
from gaft.analysis.console_output import ConsoleOutput
import time
# Define population.
indv_template = BinaryIndividual(ranges=[(1,1000)], eps=1)
#indv_template = DecimalIndividual(ranges=[(1, 1000),(0.0,0.5)], eps=0.001)
population = Population(indv_template=indv_template, size=70).init()

# Create genetic operators.
selection = RouletteWheelSelection()
#selection = TournamentSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitBigMutation(pm=0.1, pbm=0.55, alpha=0.6)
#mutation = FlipBitMutation(pm=0.1)
# Create genetic algorithm engine.
# Here we pass all built-in analysis to engine constructor.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation,
                  analysis=[ConsoleOutput, FitnessStore])






@engine.fitness_register
@engine.minimize
def fitness(indv):
 
    #NUMERO DE TICKS
    ticks =10000
    #ESTRATEGIAS ADOTADAS
    time_strategy = False
    communication_strategy = False
    evaporation_strategy = False
    watershed_strategy =   True

    

    #PARAMETROS DE SIMULAÇAO
    #print(indv.solution)   
    evap_time = 0 
    evap_factor = 0
    threshold_time = 0
    watershed_time =  1
    communication_time = 0 
    water_threshold =  int(indv.solution[0])

    number_drones = 4
     #INICIALIZAÇAO
    water = watershed(water_threshold = water_threshold,communication_strategy = communication_strategy)
    grid_size = 50
    initial_grid = []

    for row in range(grid_size):
        initial_grid.append([])
        for column in range(grid_size):     
            aux_patch = patch(u_value = 0,x = row,y = column,color = 0,intervals = [ ],visites = 0,visita_anterior = 0)
            initial_grid[row].append(aux_patch)

                  # Append a cell


   

  
    grid = []
    grids = []
    grid = copy.deepcopy(initial_grid)
    if communication_strategy == True:  
        for j in range(4):
            grids.append(copy.deepcopy(initial_grid))
            
    drones  = []  
    for num in range(number_drones):        
        drone  = Drone(x = -1,y = 49,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
        drones.append(drone)
        
    
    for tick in range(ticks):
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
                   #water.check(grid)
        if watershed_strategy:   
            if tick%watershed_time==0:
                if communication_strategy:
                    for j in range(number_drones):
                        grids[j] = water.check(grid = grids[i],grid_aux = [],drones = drones[j])
                else:
                    grid = water.check(grid = grid,grid_aux = [],drones = drones)

    soma_manobras = 0      
    for drone in drones:
        soma_manobras += drone.manouvers
    qmi,sdf,ncc =  metrics(grid,ticks)
        
       
   

    grid.clear()
    initial_grid.clear()
    drones.clear()
    if communication_strategy:
        for i in range(number_drones):
            grids[i].clear()
    return qmi





if '__main__' == __name__:
    inicio = time.time()
    engine.run(ng=100)
    best_indv = engine.population.best_indv(engine.fitness)
    print('best individual = ',best_indv.solution)
    fim = time.time()
    print('tempo de execução = ',fim - inicio)
 # WS treshold =  media , variar numero de celulas abaixo e tempo de verificaçao