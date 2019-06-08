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
from mpi4py import MPI
# Built-in best fitness analysis.
from gaft.analysis.fitness_store import FitnessStore
from gaft.analysis.console_output import ConsoleOutput

# Define population.
indv_template = BinaryIndividual(ranges=[(1, 1000),(0.0,0.5),(0, 1000)], eps=0.01)
#indv_template = DecimalIndividual(ranges=[(0, 1000)], eps=0.001)
population = Population(indv_template=indv_template, size=50).init()

# Create genetic operators.
selection = RouletteWheelSelection()
#selection = TournamentSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitBigMutation(pm=0.1, pbm=0.55, alpha=0.6)

# Create genetic algorithm engine.
# Here we pass all built-in analysis to engine constructor.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation,
                  analysis=[ConsoleOutput, FitnessStore])






@engine.fitness_register

def fitness(indv):
    evap_time,evap_factor,threshold = indv.solution
   # print(threshold)
  #  evap_factor  =  0.140696875
    evap_time = int(evap_time)
    threshold = int(threshold)
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


    for i in range(1):
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

        
        for tick in range(ticks):
            grid = drones[0].move(grid,tick)
            if tick != 0 :
                grid = drones[1].move(grid,tick)
                        
            if tick != 0 and tick != 1 :
                grid = drones[2].move(grid,tick) 

            if tick != 0 and tick != 1 and tick != 2 :
                grid = drones[3].move(grid,tick)


            if tick%evap_time == 0:
                grid = decrase_uvalue(grid = grid,feromone_value = evap_factor)

        soma_manobras = drones[0].manouvers + drones[1].manouvers + drones[2].manouvers+ drones[3].manouvers
        qmi,sdf,ncc =  metrics(grid,ticks)
        
        #metrics_results.append([i,qmi,sdf,ncc,soma_manobras])
   


    return 30000 - ((qmi*20))





if '__main__' == __name__:
    engine.run(ng=100)
    best_indv = engine.population.best_indv(engine.fitness)
    print(best_indv.solution)

 # WS treshold =  media , variar numero de celulas abaixo e tempo de verificaçao