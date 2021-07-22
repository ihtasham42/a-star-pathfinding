import pygame, random, math, queue, pdb
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 800

COLUMNS = 100
ROWS = 100

CELL_WIDTH = 8

CELL_COLOURS = {
    "empty" : (128, 128, 128),
    "wall" : (0, 0, 0),
    "start" : (0, 255, 0),
    "goal" : (255, 0, 0),
    "path" : (255, 255, 255),
    "explored" : (0, 0, 255),
}

DIRECTIONS = {
    "R" : pygame.math.Vector2(1, 0),
    "L" : pygame.math.Vector2(-1, 0),
    "D" : pygame.math.Vector2(0, 1),
    "U" : pygame.math.Vector2(0, -1)
}

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

size = (SCREEN_WIDTH, SCREEN_WIDTH)
screen = pygame.display.set_mode(size)

grid = []
for column in range(COLUMNS):
    grid.append([])
    for row in range(ROWS):
        grid[column].append("empty")

for i in range(2500):
    x = random.randint(2, ROWS - 3)
    y = random.randint(2, COLUMNS - 3)
    if grid[y][x] == "empty":
        grid[y][x] = "wall"

class Node:
    global nodes, grid, CELL_COLOURS
    def __init__(self, nodeType, position):
        nodes.append(self)
        
        self.position =  position
        self.nodeType = nodeType
        self.colour = CELL_COLOURS[nodeType]

        grid[int(position.y)][int(position.x)] = nodeType

def getNeighbours(position):
    global DIRECTIONS

    neighbours = []
    for key, direction in DIRECTIONS.items():
        neighbourPosition = position + direction
        neighbours.append(neighbourPosition)

    return neighbours

def getKey(position):
    key = str(int(position.x)) + "_" + str(int(position.y))
    return key


def pathfind(startPosition, goalPosition):
    global grid

    frontier = queue.PriorityQueue()
    frontier.put(PrioritizedItem(0, startPosition))
    cameFrom = dict()
    costSoFar = dict()
    startPositionKey = getKey(startPosition)
    cameFrom[startPositionKey] = None
    costSoFar[startPositionKey] = 0
    
    while not frontier.empty():
        current = frontier.get().item
        currentKey = getKey(current)
        for neighbour in getNeighbours(current):
            cell = grid[int(neighbour.y)][int(neighbour.x)]
            neighbourKey = getKey(neighbour)

            if cell == "goal":
                return currentKey, cameFrom
    
            if cell == "wall" or cell == "start":
                continue

            newCost = costSoFar[currentKey] + 0.01
            if neighbourKey not in costSoFar or newCost < costSoFar[neighbourKey]:
                costSoFar[neighbourKey] = newCost
                distance = neighbour.distance_to(goalPosition)
                priority = costSoFar[neighbourKey] + distance
                frontier.put(PrioritizedItem(priority, neighbour))
                cameFrom[neighbourKey] = current
                grid[int(neighbour.y)][int(neighbour.x)] = "explored"
        

def drawCell(colour, position):
    global CELL_WIDTH
    
    pygame.draw.rect(screen,
                     colour,
                     (int(position.x * CELL_WIDTH),
                      int(position.y * CELL_WIDTH),
                      CELL_WIDTH,
                      CELL_WIDTH))

def drawGrid():
    global grid, COLUMNS, ROWS, CELL_COLOURS
    
    for column in range(COLUMNS):
        for row in range(ROWS):
            cell = grid[column][row]
            colour = CELL_COLOURS[cell]
            position = pygame.math.Vector2(row, column)
            drawCell(colour, position)

def createWalls():
    global grid, COLUMNS, ROWS

    for column in range(COLUMNS):
        grid[column][0] = "wall"
        grid[column][ROWS - 1] = "wall"

    for row in range(ROWS):
        grid[0][row] = "wall"
        grid[COLUMNS - 1][row] = "wall"


createWalls()

nodes = []
start = Node("start", pygame.math.Vector2(1, 1))
goal = Node("goal", pygame.math.Vector2(98, 98))

currentKey, cameFrom = pathfind(start.position, goal.position)
while cameFrom[currentKey]:
    position = cameFrom[currentKey]
    grid[int(position.y)][int(position.x)] = "path"
    currentKey = getKey(position)

drawGrid()
                
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #screen.fill((0, 0, 0))
    pygame.display.update()

pygame.quit()
