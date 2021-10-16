from Grid_Generator import gen_grid
from A_Star import a_star
import timeit
import pandas as pd

def test(C, B, E, H, N, dim, visited):
    for i in range(dim):
        for j in range(dim):
            #if visited[i][j] != 1:
                #continue
            if (B[i][j] + E[i][j] + H[i][j]) != N[i][j]:
                print("ERROR ERROR ERROR", i, j, B[i][j], E[i][j], H[i][j], N[i][j])
            if B[i][j] > sense(i,j,grid):#C[i][j]:
                print("ERROR 2 ERROR 2 ERROR 2", i, j, B[i][j], E[i][j], H[i][j], N[i][j], sense(i,j,grid))
    print("DONE DONE DONE")

def sense(i, j, grid):
    ans=0
    for I in [i-1,i,i+1]:
        for J in [j-1,j,j+1]:
            if (I,J) == (i,j) or I>=dim or J>=dim or I<0 or J<0:
                continue
            if grid[I][J]==1:
                ans = ans + 1
    return ans

def count_neighbors(i, j, dim):
    if (i==0 and j==0) or (i==dim-1 and j==0) or (i==dim-1 and j==dim-1) or (i==0 and j==dim-1):
        return 3
    elif i==0 or j==0 or i==dim-1 or j==dim-1:
        return 5
    return 8

def find_path(parent, dim, si, sj): #used to find the path from the parent data structure
    i,j = dim-1, dim-1
    path = [(dim-1, dim-1)]
    while (i, j) != (si, sj):
        path.insert(0, parent[i][j])
        (i, j) = parent[i][j]
    return(path)

def search_size(parent, dim): #used to find the size of the search tree that was discovered
    ans = 0
    for i in parent:
        for j in i:
            if j == -1:
                ans = ans + 1
    return ((dim * dim) - ans)

def inference(dis, N, C, B, E, H, visited, con, dim):
    total = 0
    flag = 1
    while flag != 0:
        flag = 0
        for i in range(dim):
            for j in range(dim):
                if visited[i][j]==1 and dis[i][j]!=1:
                    if H[i][j]==0:
                        continue
                    if C[i][j]==B[i][j]:
                        for I in [i-1,i,i+1]:
                            for J in [j-1,j,j+1]:
                                if (I,J) == (i,j) or I>=dim or J>=dim or I<0 or J<0:
                                    continue
                                if con[I][J]==-1:
                                    con[I][J] = 0
                                    for L in [I-1,I,I+1]:
                                        for M in [J-1,J,J+1]:
                                            if (L,M)==(I,J) or L>=dim or M>=dim or L<0 or M<0:
                                                continue
                                            E[L][M] = E[L][M] + 1
                                            H[L][M] = H[L][M] - 1
                                    flag = flag + 1
                    if N[i][j] - C[i][j] == E[i][j]:
                        for I in [i-1,i,i+1]:
                            for J in [j-1,j,j+1]:
                                if (I,J) == (i,j) or I>=dim or J>=dim or I<0 or J<0:
                                    continue
                                if con[I][J]==-1:
                                    con[I][J] = 1
                                    dis[I][J] = 1
                                    for L in [I-1,I,I+1]:
                                        for M in [J-1,J,J+1]:
                                            if (L,M)==(I,J) or L>=dim or M>=dim or L<0 or M<0:
                                                continue
                                            B[L][M] = B[L][M] + 1
                                            H[L][M] = H[L][M] - 1
                                    flag = flag + 1
        total = total + flag
    return total

def check_path(path, dis):
    for (i, j) in path:
        if dis[i][j] == 1:
            return False
    return True

def agent_3(grid, dim, P, heu):
    
    start = timeit.default_timer() #recording time stamp to measure run time

    s = [[sense(j,i,grid) for i in range(dim)] for j in range(dim)] #used to represent the gridworld that has been discovered (list of lists)
    print("s")
    for x in s:
        print(x)
    
    dis = [[0 for i in range(dim)] for j in range(dim)] #used to represent the gridworld that has been discovered (list of lists)
    
    N = [[count_neighbors(i,j,dim) for j in range(dim)] for i in range(dim)] #Data Structure to store number of neighbors each cells has
    #print("N")
    #for x in N:
        #print(x)
    
    visited = [[0 for i in range(dim)] for j in range(dim)] #Data Structure to store whether or not cell has been visited
    visited[0][0] = 1
    
    con = [[-1 for i in range(dim)] for j in range(dim)] #Data Structure to store whether or not cell has been confirmed empty(0), blocked(1) or unconfirmed(-1)
    con[0][0] = 0
    con[dim-1][dim-1] = 0
    
    C = [[0 for i in range(dim)] for j in range(dim)] #Data Structure to store number of neighbors of a cell that are sensed to be blocked
    C[0][0] = sense(0, 0, grid)
    #print("C")
    #for x in C:
        #print(x)
    
    B = [[0 for i in range(dim)] for j in range(dim)] #Data Structure to store number of neighbors of a cell that are confirmed to be blocked
    #print("B")
    #for x in B:
        #print(x)
    
    E = [[0 for i in range(dim)] for j in range(dim)] #Data Structure to store number of neighbors of a cell that are confirmed to be empty
    E[0][1]=E[1][0]=E[1][1]=E[dim-1][dim-2]=E[dim-2][dim-2]=E[dim-2][dim-1]=1
    #print("E")
    #for x in E:
        #print(x)
    
    H = [[N[i][j] for j in range(dim)]for i in range(dim)] #Data Structure to store number of neighbors of a cell that are unconfirmed
    H[0][1], H[1][0], H[1][1], H[dim-1][dim-2], H[dim-2][dim-2], H[dim-2][dim-1]= 4,4,7,4,7,4
    #print("H")
    #for x in H:
        #print(x)
    
    result = False
    done = False
    
    si = 0 #Co-ordinates of the start node
    sj = 0
    
    final = [] #Data structure to store final trajectory
    
    cells = 0

    c_in = inference(dis, N, C, B, E, H, visited, con, dim)
    
    while done != True:
        print("final: ",final)
        print("con:")
        for x in con:
            print(x)
        print("H:")
        for x in H:
            print(x)
        print("visited:")
        for x in visited:
            print(x)
        result, parent =a_star(dim, P, dis, heu, si, sj) #planning stage of repeated A*
        if result == False: #true if grid not solvable
            break
        
        path = find_path(parent, dim, si, sj)
        cells = cells + search_size(parent, dim) #used to record total number of cells processed
        print("Path: ", path)
        flag = True
        for (i, j) in path: #agent traversing the planned path
            if visited[i][j] == 1:
                final.append((i,j))
                continue
            print("(i,j): ",(i,j))
            visited[i][j] = 1
            if grid[i][j] == 1: #only updating the grid knowledge after agent bumps into a blocked node
                if con[i][j]==-1:
                    dis[i][j] = 1
                    con[i][j] = 1
                    for I in [i-1,i,i+1]:
                        for J in [j-1,j,j+1]:
                            if (I,J) == (i,j) or I>=dim or J>=dim or I<0 or J<0:
                                continue
                            B[I][J] = B[I][J] + 1
                            H[I][J] = H[I][J] - 1
                (si, sj) = parent[i][j]
                final.pop(len(final)-1)
                flag = False
                test(C,B,E,H,N,dim, visited)
                c_in = inference(dis, N, C, B, E, H, visited, con, dim)
                break
            else:
                C[i][j] = sense(i, j, grid)
                if con[i][j]==-1:
                    con[i][j] = 0
                    for I in [i-1,i,i+1]:
                        for J in [j-1,j,j+1]:
                            if (I,J) == (i,j) or I>=dim or J>=dim or I<0 or J<0:
                                continue
                            E[I][J] = E[I][J] + 1
                            H[I][J] = H[I][J] - 1
            c_in = inference(dis, N, C, B, E, H, visited, con, dim)
            test(C,B,E,H,N,dim, visited)
            if c_in != 0:
                if not check_path(path, dis):
                    flag=False
                    (si, sj) = (i,j)
                    #final.pop(len(final)-1)
                    break
            final.append((i, j))

        if flag:
            done = True
    
    stop = timeit.default_timer()
    print("Final visited:")
    for x in visited:
        print(x)
    print("Final con:")
    for x in con:
        print(x)
    
    return(result, final, dis, cells, start, stop) #recording time stamp to measure run time

dim = 5
p = 0.2
grid = gen_grid(dim, p) #generating grid
#grid = [[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 0]]
#grid = [[0, 0, 0], [0, 1, 1], [0, 0, 0]]
grid = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]
#print(grid)
for x in grid:
    print(x)
result, traj, dis, cells_processed, start, stop = agent_3(grid, dim, p, 2)
print("Result: ",result)
print("Trajectory: ",traj)
