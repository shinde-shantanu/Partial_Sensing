import timeit

def dist(i, j, dim, heu): #function to measure heuristic values
    if heu == 1:
        return ( ((i-dim-1) ** 2) + ((j-dim-1) ** 2) ) ** 0.5 #Euclidean distance
    if heu == 2:
        return abs(dim-1-i)+abs(dim-1-j) #Manhattan distance
    if heu == 3:
        return max(abs(i-dim-1),abs(j-dim-1)) #Chebychev distance

def insert_fringe(i, j, fringe, f): #insertion into priority queue (Fringe)
    if len(fringe)==0:
        fringe.append((i,j))
    else:
        for x in range(len(fringe)):
            (I,J)=fringe[x]
            if f[I][J]>f[i][j]:
                fringe.insert(x, (i,j))
                return
        fringe.append((i,j))

def find_path(parent, dim, si, sj): #used to find the path from the parent data structure
    i,j = dim-1, dim-1
    path = [(dim-1, dim-1)]
    while (i, j) != (si, sj):
        path.insert(0, parent[i][j])
        (i, j) = parent[i][j]
    return(path)

def a_star(dim, P, grid, heu, si, sj):
    
    result=False
    
    g=[[-1 for i in range(dim)] for j in range(dim)] #data structure to store g(n) (list of lists). initialized with -1 for now
    g[si][sj]=0
    
    h=[[dist(i,j,dim,heu) for i in range(dim)] for j in range(dim)] #data structure to store h(n) (list of lists).
    
    f=[[-1 for i in range(dim)] for j in range(dim)] #data structure to store f(n) (list of lists). initialized with -1 for now
    f[si][sj]=g[si][sj]+h[si][sj]
    p=[[-1 for i in range(dim)] for j in range(dim)] #data structure to store pointers to parent (list of lists). initialized with -1 for now
    p[si][sj]=0
    
    fringe=[(si,sj)] #pushing the start node into the fringe
    
    while len(fringe)!=0:
        (i,j)=fringe.pop(0)
        if (i,j) == (dim-1,dim-1): #true if goal node is reached
            result=True
            break
        if i-1 >= 0 and grid[i-1][j] != 1 and p[i-1][j]==-1 and p[i][j] != (i-1,j): #checking the chilren of each node popped from fringe
            p[i-1][j]=(i,j)
            g[i-1][j]=g[i][j]+1
            f[i-1][j]=g[i-1][j]+h[i-1][j]
            insert_fringe(i-1,j,fringe,f)
            
        if j+1 < dim and grid[i][j+1] != 1 and p[i][j+1]==-1 and p[i][j] != (i,j+1):
            p[i][j+1]=(i,j)
            g[i][j+1]=g[i][j]+1
            f[i][j+1]=g[i][j+1]+h[i][j+1]
            insert_fringe(i,j+1,fringe,f)
            
        if i+1 < dim and grid[i+1][j] != 1 and p[i+1][j]==-1 and p[i][j] != (i+1,j):
            p[i+1][j]=(i,j)
            g[i+1][j]=g[i][j]+1
            f[i+1][j]=g[i+1][j]+h[i+1][j]
            insert_fringe(i+1,j,fringe,f)
            
        if j-1 >= 0 and grid[i][j-1] != 1 and p[i][j-1]==-1 and p[i][j] != (i,j-1):
            p[i][j-1]=(i,j)
            g[i][j-1]=g[i][j]+1
            f[i][j-1]=g[i][j-1]+h[i][j-1]
            insert_fringe(i,j-1,fringe,f)
    
    return(result, p)

def agent_2(grid, dim, P, heu):
    
    start = timeit.default_timer() #recording time stamp to measure run time
    
    dis = [[0 for i in range(dim)] for j in range(dim)] #used to represent the gridworld that has been discovered (list of lists)
    
    result = False
    done = False
    
    si = 0 #Co-ordinates of the start node
    sj = 0
    
    final = [] #Data structure to store final trajectory
    
    vis = 0
    plan_t = 0
    bumps = 0
    
    while done != True:

        ps = timeit.default_timer()
        result, parent =a_star(dim, P, dis, heu, si, sj) #planning stage of repeated A*
        plan_t = plan_t + (timeit.default_timer() - ps)
        
        if result == False: #true if grid not solvable
            break
        
        path = find_path(parent, dim, si, sj)
        
        flag = True
        for (i, j) in path: #agent traversing the planned path
            vis = vis + 1
            if grid[i][j] == 1: #only updating the grid knowledge after agent bumps into a blocked node
                bumps = bumps + 1
                dis[i][j] = 1
                (si, sj) = parent[i][j]
                final.pop(len(final)-1)
                flag = False
                break
            final.append((i, j))

        if flag:
            done = True
    
    stop = timeit.default_timer()
    
    return(result, final, dis, vis, start, stop, plan_t, bumps) #recording time stamp to measure run time
