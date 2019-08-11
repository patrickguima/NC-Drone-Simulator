import pygame
from ncDrone import *
import copy
def select_initial_state(drones,grid,grids,ticks,run,communication_strategy,evap_strategy, et,ef):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (150, 255, 150)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    WIDTH =14
    HEIGHT = 14
 
    grid_size = 50
    MARGIN = 1
    
 
    pygame.init()
 
    WINDOW_SIZE = [752, 751]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("NC drone")
    image = pygame.image.load('falcon.png')
# Loop until the user clicks the close button.
    done = False
    image = pygame.transform.scale(image,[12,12])
    image = pygame.transform.rotate(image,-90)
# Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    water = watershed()

    tick = 0
    beginNC = False
    communication_time = 1
    water.water_threshold = 2


# -------- Main Program Loop -----------
    while not done:


        path = []

        for event in pygame.event.get():  

            if event.type == pygame.QUIT:  
                done = True  
            elif pygame.mouse.get_pressed()[0]:  
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
            
                grid[row][column].color = 1
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                grid[row][column].color = 3
           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE  and beginNC == False:
                    beginNC = True
                elif event.key == pygame.K_SPACE  and beginNC == True:
                    beginNC = False
                elif event.key == pygame.K_RIGHT:
                    run = False
                    if communication_strategy == True:
                        for k,drone in enumerate(drones):
                            if tick_to_go(tick,k):
                                grid,grids[k] = drone.move(grid = grid,tick = tick,grid_aux = grids[k])
                        if tick %communication_time ==0:       
                            grid,grids = update_grid(grid,grids)
                    else:
                       for k,drone in enumerate(drones):
                            #print(k)
                            if tick_to_go(tick,k):
                                grid,_ = drone.move(grid = grid,tick = tick,grid_aux = [])
                                #print(drones[].x,' ',drones[1].y )
                            if evap_strategy:
                                if  tick%et ==0:
                                    grid = decrase_uvalue(grid = grid,feromone_value = ef)
                    tick+=1     



        if(tick >= ticks):
            done = True
        if(beginNC ):
            done = True

        
        if(run):
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
                if evap_strategy:
                    #print('here')
                    if  tick%et ==0:
                        grid = decrase_uvalue(grid = grid,feromone_value = ef)
              
                
            tick+=1

        font = pygame.font.Font(None, 10)
    #text = font.render("1", True, BLACK)
        #size_obstacles(grid)
       
        screen.fill(BLACK)
        # Draw the grid
        for row in range(grid_size):
            for column in range(grid_size):
                color = WHITE
                text = font.render(str(grid[row][column].visites), True, BLACK)
                if grid[row][column].color == 1:
                    color = GREEN
                if grid[row][column].color == 2:
                    color = BLUE
                if grid[row][column].color == 3:
                    color = RED
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
                screen.blit(text,((8+(15* grid[row][column].y )) - text.get_width()//2 ,(10 + (15 * grid[row][column].x )) -text.get_height()//2))
                
    # Limit to 60 frames per second
       # DRONE = drone[0]
        #x = drones[0]
        #screen.blit(image, (x,y))
        for i in range(len(drones)):
            screen.blit(image, (drones[i].posBoard[0], drones[i].posBoard[1]))
        #screen.blit(image, (drone2.posBoard[0], drone2.posBoard[1]))

        clock.tick(30)

        pygame.display.flip()
 

    pygame.quit()
    if(beginNC ):
        return grid

   

