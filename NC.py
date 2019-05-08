

import pygame
import util
import random
class Drone:
    x = 0
    y = 0
    posBoard = [(x*37) +5,(y*37) +5] 
    direction = "right"
    manouvers = 0
    def moveRight(self):
        if(self.x <14):
            self.x+=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
    def moveLeft(self):
        if(self.x >0):
            self.x-=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
    def moveUp(self):
        if(self.y >0):
            self.y-=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
    def moveDown(self):
        if(self.y <14):
            self.y+=1
            self.posBoard = [(self.x*37) +5,(self.y*37) +5]

    def move(self,grid):
        grid[self.y][self.x].color=1
        grid[self.y][self.x].u_value+=1
        sucessor = random.choice(getSucessor(self.y,self.x,grid))
        self.x = sucessor.y
        self.y = sucessor.x
        self.posBoard = [(self.x*37) +5,(self.y*37) +5] 
      

class patch ():
    def __init__(self,u_value = 0,x = None , y=None,color = 0):
        self.u_value = u_value
        self.x = x
        self.y = y
        self.color = color




def valide(x,y,grid):
    if (x <0 or x >14 or y <0 or y> 14):
        return False
    if grid[x][y].color==3:
       # print("grid ",grid[x][y])
       # print("HERE")
        return False

    return True 
def getSucessor(x,y,grid):
    sucessors = []
    new_sucessors = []
    if  valide(x+1,y,grid):
        sucessors.append(grid[x+1][y])
    if valide(x-1,y,grid):
        sucessors.append(grid[x-1][y])
    if valide(x,y+1,grid):
        sucessors.append(grid[x][y+1])
    if valide(x,y-1,grid):
        sucessors.append(grid[x][y-1])
    #print(sucessors)    
    sucessors = sorted(sucessors,key = lambda x: x.u_value)
    minimo = sucessors[0].u_value
    #print("minimo",minimo)
    new_sucessors = list(filter(lambda x : x.u_value <= minimo,sucessors))
    #print(sucessors[0].x)
    #print(sucessors[1].u_value)
    return new_sucessors



queue = []
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 

WIDTH = 32
HEIGHT = 32
 

MARGIN = 5

grid = []
for row in range(15):
    grid.append([])
    for column in range(15):
        aux_patch = patch(0,row,column,0)
        grid[row].append(aux_patch)  # Append a cell
 
print(grid[0][0].color)

pygame.init()
 
WINDOW_SIZE = [560, 560]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("A star")
image = pygame.image.load('falcon.png')
# Loop until the user clicks the close button.
done = False
image = pygame.transform.scale(image,[32,32])
image = pygame.transform.rotate(image,-90)
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
drone = Drone()



beginNC = False
print (queue)
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

            if event.key == pygame.K_d:
                drone.moveRight()
            elif event.key == pygame.K_s:
                drone.moveDown()
            elif event.key == pygame.K_w:
                drone.moveUp()
            elif event.key == pygame.K_a:
                drone.moveLeft()
            elif event.key == pygame.K_p:
                drone.move(grid)
    if(beginNC):
        drone.move(grid)



    font = pygame.font.Font(None, 30)
    #text = font.render("1", True, BLACK)

    
    screen.fill(BLACK)
    # Draw the grid
    for row in range(15):
        for column in range(15):
            color = WHITE
            text = font.render(str(grid[row][column].u_value), True, BLACK)
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