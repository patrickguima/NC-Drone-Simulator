

import pygame
import util

class Drone:
    x = 0
    y = 0
    posBoard = [(x*37) +5,(y*37) +5] 
    
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
def isGoal(x,y,grid):
    if grid[x][y] == 1:
        return True
    return False

def valide(x,y):
    if (x <0 or x >14 or y <0 or y> 14):
        return False
    return True 
def getSucessor(x,y,grid):
    sucessors = []
    if  valide(x+1,y):
        if grid[x+1][y]!= 3 :
            sucessors.append((x+1,y))
    if valide(x-1,y):
        if grid[x-1][y]!= 3 :
            sucessors.append((x-1,y))
    if valide(x,y+1):
        if grid[x][y+1]!= 3 :
            sucessors.append((x,y+1))
    if valide(x,y-1):
        if grid[x][y-1]!= 3:
            sucessors.append((x,y-1))

    return sucessors

class Node():
    def __init__(self, parent =None,position=None):
        self.parent = parent
        self.position = position


def aStar(startPos,grid):
    queue = util.PriorityQueue();
    done = set()
    startNode = Node(None,startPos)
    queue.push(startNode,0)
    i=0
    while not queue.isEmpty():
        node = queue.pop()
       # print("node", node.position)
        #return
        if  isGoal(node.position[0],node.position[1],grid):
            current = node
            path = []
            while current is not None:
                path.append(current.position)
                current = current.parent
                print(path[::-1])
            return path[::-1]
        if node.position not in done:
            done.add(node.position)
            
            for k in getSucessor(node.position[0],node.position[1],grid):
                if k not in done:
                    #print("sucessor ",k)
                    i+=1
                    queue.push(Node(node,k),i)

        #print("DONE ")
    #print(queue)                


queue = []

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 32
HEIGHT = 32
 
# This sets the margin between each cell
MARGIN = 5
 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(15):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(15):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)#
#grid[1][5] = 1
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
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
#sucessors = getSucessor(0,0,grid)
#print(sucessors)




print (queue)
# -------- Main Program Loop -----------
while not done:


    path = []

    for event in pygame.event.get():  # User did something

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif pygame.mouse.get_pressed()[0]:  
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            
            grid[row][column] = 1
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            grid[row][column] = 3
            #print("Click ", pos, "Grid coordinates: ", row, column)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                drone.moveRight()
            if event.key == pygame.K_a:
                drone.moveLeft()
            if event.key == pygame.K_w:
                drone.moveUp()
            if event.key == pygame.K_s:
                path = aStar((drone.x,drone.y),grid)
    # Set the screen background
    if len(path)>0:
        for x,y in path:
            grid[x][y] = 1



    screen.fill(BLACK)
    
    # Draw the grid
    for row in range(15):
        for column in range(15):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            if grid[row][column] == 3:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
 
    # Limit to 60 frames per second
    screen.blit(image, (drone.posBoard[0], drone.posBoard[1]))

    clock.tick(60)
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()