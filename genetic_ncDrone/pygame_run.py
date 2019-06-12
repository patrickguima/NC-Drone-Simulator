import pygame
from ncDrone import *
def select_initial_state(drones,grid,ticks,run):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    WIDTH =14
    HEIGHT = 14
 
    grid_size = 50
    MARGIN = 5
    
 
    pygame.init()
 
    WINDOW_SIZE = [1100, 1100]
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

                    grid = drones[0].move(grid,tick)
                    #simulation(drones[0],grid,tick)
                    if tick != 0 :
                        grid = drones[1].move(grid,tick)
                    
                    if tick != 0 and tick != 1 :
                        grid = drones[2].move(grid,tick) 

                    if tick != 0 and tick != 1 and tick != 2 :
                        grid = drones[3].move(grid,tick) 

                    tick+=1     



        if(tick >= ticks):
            done = True
        if(beginNC ):
            done = True

       
        if(run):
            #if tick % 100 == 0:
              #  grid =  decrase_uvalue(grid,0.1)
            grid = drones[0].move(grid,tick)
                    #simulation(drones[0],grid,tick)
            if tick != 0 :
                grid = drones[1].move(grid,tick)
                    
            if tick != 0 and tick != 1 :
                grid = drones[2].move(grid,tick) 

            if tick != 0 and tick != 1 and tick != 2 :
                grid = drones[3].move(grid,tick) 

            tick+=1   
            
            if(tick % 400 ==0):
                print("ticks ",tick)
                
                grid = water.check(grid = grid)
          

        font = pygame.font.Font(None, 20)
    #text = font.render("1", True, BLACK)

    
        screen.fill(BLACK)
        # Draw the grid
        for row in range(grid_size):
            for column in range(grid_size):
                color = WHITE
                text = font.render(str(grid[row][column].u_value), True, BLACK)
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
                screen.blit(text,((10+(19* grid[row][column].y )) - text.get_width()//2 ,(12 + (19 * grid[row][column].x )) -text.get_height()//2))
 
    # Limit to 60 frames per second
       # DRONE = drone[0]
        #x = drones[0]
        #screen.blit(image, (x,y))
        for i in range(len(drones)):
            screen.blit(image, (drones[i].posBoard[0], drones[i].posBoard[1]))
        #screen.blit(image, (drone2.posBoard[0], drone2.posBoard[1]))

        clock.tick(60)

        pygame.display.flip()
 

    pygame.quit()
    if(beginNC ):
        return grid

   

