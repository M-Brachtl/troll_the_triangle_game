# from collections import deque
from queue import Queue
from random import choice as r_choice

def find_path(start, goal, grid):
    queue = Queue()
    visited = set()
    came_from = dict()
    path = []

    ROWS = len(grid)
    COLUMNS = len(grid[0])

    # inicializace
    queue.put(start)
    visited.add(start)
    came_from[start] = (-1,-1)

    while not queue.empty():
        current = queue.get()
        if current == goal:
            path.append(goal)
            break
        neighbours = [ # všechna sousední políčka, na která se lze teoreticky dostat
            (current[0]+1, current[1]),
            (current[0]-1, current[1]),
            (current[0], current[1]+1),
            (current[0], current[1]-1)
        ]
        # filtrace a umisťování do queue
        while len(neighbours) > 0:
            next_cell = r_choice(neighbours) # náhodné, pro promělivější chování Enemy
            neighbours.remove(next_cell)
            if 0 <= next_cell[0] < ROWS and 0 <= next_cell[1] < COLUMNS and next_cell not in visited and grid[next_cell[1]][next_cell[0]] in (0, 7, 11):
                queue.put(next_cell)
                visited.add(next_cell)
                came_from[next_cell] = current
    
    if not len(path) == 0:
        step_back = came_from[goal]
        while step_back != start:
            path.append(came_from[step_back])
            step_back = came_from[step_back]
        path.reverse()
    return path

