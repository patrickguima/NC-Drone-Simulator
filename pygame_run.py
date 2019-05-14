import pygame
from ncDrone import *
def select_initial_state(drone,grid,ticks,run):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
 

    WIDTH = 32
    HEIGHT = 32
 
    grid_size = 15
    MARGIN = 5
    
 
    pygame.init()
 
    WINDOW_SIZE = [560, 560]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("NC drone")
    image = pygame.image.load('falcon.png')
# Loop until the user clicks the close button.
    done = False
    image = pygame.transform.scale(image,[32,32])
    image = pygame.transform.rotate(image,-90)
# Used to manage how fast the screen updates
    clock = pygame.time.Clock()

 

    tick = 1
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
                

        if(tick >= ticks):
            done = True
        if(beginNC ):
            done = True

       
        if(run):
            tick+=1
            if(tick % 100 ==0):
                print("ticks ",tick)
            simulation(drone,grid,tick)

        font = pygame.font.Font(None, 30)
    #text = font.render("1", True, BLACK)

    
        screen.fill(BLACK)
        # Draw the grid
        for row in range(grid_size):
            for column in range(grid_size):
                color = WHITE
                text = font.render(str(grid[row][column].visites), True, BLACK)
                if grid[row][column].color == 1:
                    color = GREEN
                if grid[row][column].color == 3:
                    color = RED
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
                screen.blit(text,((20+(37* grid[row][column].y )) - text.get_width()//2 ,(20 + (37 * grid[row][column].x )) -text.get_height()//2))
 
    # Limit to 60 frames per second
        screen.blit(image, (drone.posBoard[0], drone.posBoard[1]))

        clock.tick(60)
    
    # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
    pygame.quit()
    if(beginNC ):
        return grid

   

