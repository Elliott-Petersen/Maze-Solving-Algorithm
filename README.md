# Maze-Solving-Algorithm
Allows you to draw a maze, then shows it being automatically solved.

This file contains 2 main functions:
maze_maker(size)
which allows you to create a maze of the given size, complete with a start and finish square, on a grid.
It prints the list form of the maze so it can be used again.

maze_solver(maze, distance)
which animates my algorithm solving the maze, using the given distance function.
It returns the list of nodes that the found path traverses, in order, along with its length.

At each node, it checks to see if any neighbours are closer to the end. If any are, then immediately go to it.
If not, it then looks at each node that it could have gone to earlier and reads a value for each; it then chooses the node with the smallest such value.
This value is defined by taking the distance from that node to the end using the given distance function, and adding the path length to get to that node from the start.

The distance function can be passed as anything, subject to a few constraints.
The default is a variation of the "best first" searth algorithm, that tries to get as close to the end as possible, as quickly as possible.


These are the constraints that a custom function has to adhere to:
The first 2 parameters must be the positions of the start and end nodes, respectively.
It must return a float; a number.
It can contain start; the position of the start node, also given as a tuple of 2 integers.
It can also contain walls; the numerical form of the maze itself, comprised of a list of lists of integers.
Within it, a 0 represents an open space, a 1 represents a wall, the 2 represents the start node, and the 3 represents the finish node.



Here are some example functions that can be used:

def func(a,end):
  return ((a[0]-end[0])**2+(a[1]-end[1])**2)

the default function; it works similarly to the "best first" algorithm.

def func(a,end,k=5): 
  x=abs(a[0]-end[0])
  y=abs(a[1]-end[1])
  return (x+y)*k
k=5 can be replaced with any positive number. 
Larger numbers find a path faster (acting closer to the "best first" algorithm), but can be sub-obtimal.
Smaller numbers are more likely to find a shorter path, but usually take more time to do so.

k=1 judges the current distance to the start node and the end node equally

k=0 is "breadth first"; inefficient but guaranteed to find the shortest path by expanding a diamond out from the start.

k=1000 works identically to the greedy "best first" algorithm.

def func(a,end):
    return(a[0]-start[0])**2+(a[1]-start[1])**2

Builds a circle strating from the centre; included to show how you can
use the start node as part of your custom distance function.
 
 
def func(a,end):
    l = len(walls)/4
    a=(a[0]//l*l,a[1]//l*l)
    return abs(a[0]-end[0])+abs(a[1]-end[1])

This splits the map into 16 sections, and the distance function for each square calculates from the top left corner of each section.


If the window becomes unresponsive, just wait for it to respond again. It soon will.
