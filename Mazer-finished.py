from math import inf
from collections import OrderedDict as odict
import pygame
import numpy
pygame.init()

def keep_open():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
def maze_maker(size):
    '''

    Parameters
    ----------
    size : int, optional
        DESCRIPTION. The default is 15
        Choose how big a square you want your maze in.
    
    Allows you to create a map on a square with start and finish squares
    Then shows my algorithm solving it using the given distance function.
    Returns the path taken and the length.
    Prints the list form of a map so it can be used again.
    If the window becomes unresponsive, just wait for it to respond again.
    
    RETURNS
    -------
    A map of the maze you created.
    '''
    
    print('''
    Instructions:
    Click the red square, then anywhere on the grid to place a starting point.
    Click the green square, then anywhere on the grid to place a destination.
    Click the black square, then hold the mouse button down on the grid to draw walls.
    Click on the white square, then hold the mouse button down on the grid to erase.
    When you're done, click the blue rectangle and watch
    as my algorithm finds a near-optimal path towards the destination in an efficient manner,
    using the given distance function.
        ''')
        
    if size>500:
        print('Too big. Please try a smaller number')
        return None
    elif size<2:
        print('Too small. Please try a larger number')
        return None
    
    size=(size,size)
    mp=[[0 for j in range(size[0])] for i in range(size[1])] #makes a square of zeroes
    
    size=(size[0]+2,size[1]+2)
        
    #calculates the width and height
    x=0
    while (500+x)%size[0]:
        x+=1
    xw=int((500+x)/size[0])
    y=0
    while (500+y)%size[1]:
        y+=1
    yw=int((500+y)/size[1])
    
    window = pygame.display.set_mode((500+x,580+y))
    pygame.display.set_caption('mapper')
    running=True
    window.fill((255,255,255))
    
    
    
     #creates a border
    for i in range(len(mp)):
        mp[i]=[1]+mp[i]+[1]
    mp = [[1 for i in mp[0]]]+mp+[[1 for i in mp[0]]]
    pygame.draw.rect(window,(0,0,0),(0,0,xw,500+y))
    pygame.draw.rect(window,(0,0,0),(0,0,500+x,yw))
    pygame.draw.rect(window,(0,0,0),(500+x,500+y,-xw+1,-500-y))
    pygame.draw.rect(window,(0,0,0),(500+x,500+y,-500-x,-yw+1))
    
    
    #creates the grid and the buttonr
    pygame.draw.rect(window,(128,128,128),(0,500+x,580+y,100))
    pygame.draw.rect(window,(0,0,0),(30,530+y,20,20))
    pygame.draw.rect(window,(255,255,255),(70,530+y,20,20))
    pygame.draw.rect(window,(255,0,0),(110,530+y,20,20))
    pygame.draw.rect(window,(0,255,0),(150,530+y,20,20))
    pygame.draw.rect(window,(0,0,255),(200,530+y,100,20))
    
    for i in range(size[1]):
        pygame.draw.line(window,(123,123,123),(0,yw*i),(500+x,yw*i))
    for j in range(size[0]):
        pygame.draw.line(window,(123,123,123),(xw*j,0),(xw*j,500+y))
    
    
    colour = (0,0,0)
    held=False
    while running:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                held=True
                p = list(event.dict['pos'])
                #determines which button is pressed
                if 530<=p[1]-y<=550:
                    if 30<=p[0]<=50:
                        colour = (0,0,0)
                    elif 70<=p[0]<=90:
                        colour = (255,255,255)
                    elif 110<=p[0]<=130:
                        colour = (255,0,0)
                    elif 150<=p[0]<=170:
                        colour = (0,255,0)
                    elif 200<=p[0]<=300:
                        #you cannot start solving without a start or end point
                        if all([2 not in i for i in mp]):
                            print('please add a start point')
                        elif all([3 not in i for i in mp]):
                            print('please add an end point')
                        else:
                            print(mp)
                            return mp,start,end

            elif event.type == pygame.MOUSEBUTTONUP:
                held=False
            elif event.type == pygame.MOUSEMOTION:
                p=list(event.dict['pos'])
                
            if held and xw<p[0]<500+x-xw and yw<p[1]<500+y-yw:
                if not(colour==(255,0,0) and any([2 in i for i in mp])):
                    if not(colour==(0,255,0) and any([3 in i for i in mp])):
                        pygame.draw.rect(window,colour, ( p[0]//xw*xw+1, p[1]//yw*yw+1, xw-1,yw-1))
                        #draws on the grid; maximum of 1 start and end node
                
                #creates a numerical map of the grid
                if colour==(0,0,0):
                    mp[p[1]//xw][p[0]//yw]=1
                    
                elif colour==(255,0,0) and all([2 not in i for i in mp]):
                    mp[p[1]//xw][p[0]//yw]=2
                    start=[p[1]//xw,p[0]//yw]
                    
                elif colour==(0,255,0) and all([3 not in i for i in mp]):
                    mp[p[1]//xw][p[0]//yw]=3
                    end=[p[1]//xw,p[0]//yw]
                    
                elif colour==(255,255,255):
                    mp[p[1]//xw][p[0]//yw]=0
    return 

def find_end(walls):
    for i in range(len(walls)):
        if 3 in walls[i]:
            return(i,walls[i].index(3))

def find_start(walls):
    for i in range(len(walls)):
        if 2 in walls[i]:
            return (i, walls[i].index(2))


def maze_solver(mp, distance= lambda a,b: ((a[0]-b[0])**2+(a[1]-b[1])**2)):
    '''
    

    Parameters
    ----------
    mp : the map of the maze you created.
    
    distance : function, optional
        DESCRIPTION. The default is the "best first" searth algorithm.
            function Parameters: (a,b)
            a=(int,int)
            b=(int,int)
            returns int
            Any function can be passed that has the right inputs and output.
            Example functions are given in the README.

    Returns
    -------
    the list of nodes that the found path traverses, in order
    the distance traversed.

    '''
    if not mp:
        return None
    size=(len(mp),len(mp[0]))
    
    end,start = find_end(mp),find_start(mp)
    
    def dist(a,end=end):
        return distance(a,end)
    
    x=0
    while (500+x)%size[0]:
        x+=1
    xw=int((500+x)/size[0])
    y=0
    while (500+y)%size[1]:
        y+=1
    yw=int((500+y)/size[1])
    #calculates width and height of each rectangle in the grid

    #creates the window
    window = pygame.display.set_mode((500+x,500+y))
    pygame.display.set_caption('mazer')
    window.fill((255,255,255))
    
    #creates the grid
    for i in range(size[1]):
        pygame.draw.line(window,(123,123,123),(0,yw*i),(500+x,yw*i))
    for i in range(size[0]):
        pygame.draw.line(window,(123,123,123),(xw*i,0),(xw*i,500+y))
    pygame.draw.rect(window,(255,0,0),(start[1]*xw+1,start[0]*yw+1,xw-1,yw-1))
    pygame.draw.rect(window,(0,255,0),(  end[1]*xw+1,  end[0]*yw+1,xw-1,yw-1))
    for i in range(len(mp)):
        for j in range(len(mp[i])):
            if mp[i][j]==1:
                pygame.draw.rect(window,(0,0,0),(j*xw+1,i*yw+1,xw-1,yw-1))
    
    #explored[node] = (distance from start to node, estimated distance from node to end)
    #canexplore[node] = estimated distance from node to end
    #P[node] = the predecessor; the cell that you reach the current node from
    explored=odict()
    explored[start]=(0,dist(start))
    canexplore=dict()
    P=odict()
    now=start
    mp[start[0]][start[1]]=1
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        pygame.time.delay(int(250/size[0]))
        pygame.display.update()
        
        #builds the list of the options that the latest node can reach
        nxt=[]
        
        new=(now[0]-1,now[1]) #look left
        if mp[new[0]][new[1]]!=1: #check if free
            canexplore[new]=(explored[now][0]+1,dist(new))
            P[new]=now
            mp[new[0]][new[1]]=1
            nxt.append(new)
            pygame.draw.rect(window,(100,255,255),(new[1]*xw+1,new[0]*yw+1,xw-1,yw-1))
            
        new=(now[0]+1,now[1]) #look right
        if mp[new[0]][new[1]]!=1:
            canexplore[new]=(explored[now][0]+1,dist(new))
            P[new]=now
            mp[new[0]][new[1]]=1
            nxt.append(new)
            pygame.draw.rect(window,(100,255,255),(new[1]*xw+1,new[0]*yw+1,xw-1,yw-1))
            
        new=(now[0],now[1]+1) #look down
        if mp[new[0]][new[1]]!=1:
            canexplore[new]=(explored[now][0]+1,dist(new))
            P[new]=now
            mp[new[0]][new[1]]=1
            nxt.append(new)
            pygame.draw.rect(window,(100,255,255),(new[1]*xw+1,new[0]*yw+1,xw-1,yw-1))
            
        new=(now[0],now[1]-1) #look up
        if mp[new[0]][new[1]]!=1:
            canexplore[new]=(explored[now][0]+1,dist(new))
            P[new]=now
            mp[new[0]][new[1]]=1
            nxt.append(new)
            pygame.draw.rect(window,(100,255,255),(new[1]*xw+1,new[0]*yw+1,xw-1,yw-1))
            
        mn=explored[now][1]
        n=False
        for node in nxt:
            if node == end: #we have reached the destination. Animate the path.
                explored[node]=canexplore[node]
                pygame.draw.rect(window,(0,255,0),(  end[1]*xw+1,  end[0]*yw+1,xw-1,yw-1))
                c=node
                path=[end]
                while P[c]!=start:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return False
                    c=P[c]
                    path.append(c)
                    pygame.draw.rect(window,(0,0,255),(c[1]*xw+1,c[0]*yw+1,xw-1,yw-1))
                    pygame.time.delay(int(150/size[0]**.5))
                    pygame.display.update()
                path.append(start)
                path.reverse()
                keep_open()
                return path, explored[node][0]
            
            #see which of the 5 nodes (up, down, left, right, centre) is the closest to the end
            if canexplore[node][1]<mn: 
                mn=canexplore[node][1]
                n=node
        if n:
            #if one it can reach is closer, go to it immediately.
            node=n
            explored[node]=canexplore[node]
            del canexplore[node]
            mp[node[0]][node[1]]=1
        elif canexplore:
            #if not; find the cell we can reach but haven't looked at yet that may give
            #the shortest total distance from the start to the end.
            mn=inf
            for node in list(canexplore.keys()):
                if canexplore[node][0]+canexplore[node][1]<mn:
                    mn=canexplore[node][0]+canexplore[node][1]
                    n=node
            explored[n]=canexplore[n]
            del canexplore[n]
            mp[n[0]][n[1]]=1
        else:
            pygame.quit()
            return 'no path exists'
        
        now=list(explored.keys())[-1] #go to the node that is best.
        pygame.draw.rect(window,(255,255,100),(now[1]*xw+1,now[0]*yw+1,xw-1,yw-1))
    return
        

# def func(a,b):
#     return (a[0]-b[0])**2+(a[1]-b[1])**2

# def func(a,b):
#     l = len(walls)/4
#     a=(a[0]//l*l,a[1]//l*l)
#     b=(b[0]//l*l,b[1]//l*l)
#     return abs(a[0]-b[0])+abs(a[1]-b[1])

# def func(a,b):
#     return max(abs(a[0]-end[0]),abs(a[1]-end[1]))

# def func(a,b,k=-1): 
#     x=abs(a[0]-end[0])
#     y=abs(a[1]-end[1])
#     return (x+y)*k


# def func(a,b):
#     l = len(walls)/4
#     a=(a[0]//l*l,a[1]//l*l)
#     return abs(a[0]-b[0])+abs(a[1]-b[1])


walls,start,end=maze_maker(50)

start,end=find_start(walls),find_end(walls)

saved_maze = [[e for e in i ]for i in walls]


maze_solver(walls)





