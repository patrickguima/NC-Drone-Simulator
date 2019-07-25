# patrolling-algorithms




The test platform was built using the PyGame library. The scenario is a 50×50 grid containing four UAVs modeled as robot-agents. We present four types of scenarios, one free of obstacles and other three containing different compositions of no-fly zones  (NFZ). The aerial robots cannavigate through the scenario, interact with each other, and avoid the NFZ. The starting position of the UAVs is at thelower-left corner of the scenario.   
The primary goal of the NC-Drone is to reduce excessive NTM while keeping unpredictable behavior by solving the tie issue. NC-Drone checks the position of the cells with the same minimum-value. In the case of one of these cells is following the sweeping direction, this cell is picked as the next spot to be explored. In this way, the aerial vehicle maintains a straight trajectory. If there is no such cell, a random decision is made, and the UAV performs a turn to reach the selected side cell.

## NC Drone
For the UVAs moviments we implemented the NC Drone algorithm. The NC is an RTSM which guides biologically-inspired robots over a grid-discretized scenario by reading and writing pheromones for motion planning. 
## Simulation Scenario
<img src="Images/scenario.png" width="500" height="500">


## No Fly Zone Scenarios
<img src="Images/scenario-1.png" width="200" height="200"> <img src="Images/scenario-2.png" width="200" height="200"> <img src="Images/scenario-3.png" width="200" height="200">
