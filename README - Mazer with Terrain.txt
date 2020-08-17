Allows you to draw a maze, then shows it being automatically solved.

This file contains 2 main functions:

maze_maker(size)

which allows you to create a maze of the given size (given as an (x,y) tuple), complete with a start and finish square, on a grid. It then saves the maze for you to use again.


maze_solver(maze, distance) which animates my algorithm solving the maze, using the given distance function. It returns the list of nodes that the found path traverses, in order, along with its length.

At each iteration, it looks at each square in the perimeter and reads a value for each; it then chooses the node with the smallest such value, removes it from the perimeter, and adds its neighbours. 
The value is defined by taking the distance from that node to the end using the given distance function, and adding the path length to get to that node from the start.

The distance function can be passed as anything, subject to a few constraints. The default is a variation of the "best first" searth algorithm, that tries to get as close to the end as possible, as quickly as possible.

These are the constraints that a custom function has to adhere to:

The first 2 parameters must be the positions of the current and end nodes, respectively.

It must return a float; a number.

It can contain start; the position of the start node, also given as a tuple of 2 integers.

It can also contain mp; the numerical form of the maze itself, comprised of a list of lists of mostly integers, with each list being a row.

Within it, the strings 'start' and 'end' represent the start and end nodes, respectively. The other elements are a number that represents how harsh the terrain is on that tile; from 0 to 10, and infinity.


The distance function can be customized to add more weighting to harsh terrain, make the distance travelled so far less important, and change the general shape of the area explored.

def func(a, f=1.01,w=1.5,h=2):
    dx = abs(a[0]-end[0]) # the horizontal distance between the current and end points
    dy = abs(a[1]-end[1]) # the vertical distance
    w = mp[a[0]][a[1]]    # the value of the terrain at that point
    return ((dx**f+dy**f)**(1/f) + w*g)*h

f makes a general shape from the end:
    0.1 < 1 < 2 < 10
    plus to diamond to circle to square, stretched by 1/h towards the start
g puts more weighting on harsh terrain.
h takes weighting away from the distance travelled so far.

Setting h = 0 is equal to the breadth first algorithm; it always chooses the point on the perimeter with the shortest travelled distance.
Setting h = 2 or more makes the algorithm find a path quicker, but no longer guarantees the shortest path

Keeping h<=1 and f>=1 means that the heuristic function is admissable, and guarantees the shortest path as in the A* algorithm.

If the window becomes unresponsive, just wait for it to respond again. It soon will.