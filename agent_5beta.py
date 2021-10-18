# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 23:02:45 2021

@author: Abhishek
"""
from Grid_Generator import gen_grid
from A_Star import a_star
import timeit
import pandas as pd
from Agent_3 import inference




dim=5


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

prob_node = [[0 for i in range(dim)] for j in range(dim)]
act_prob_node = [[0 for i in range(dim)] for j in range(dim)]

node_whose_neighbour = [[-1 for i in range(dim)] for j in range(dim)]
sense_value_for_node = [[-1 for i in range(dim)] for j in range(dim)]
N = [[count_neighbors(i,j,dim) for j in range(dim)] for i in range(dim)] #Data Structure to store number of neighbors each cells has
    #print("N")
    #for x in N:
        #print(x)

        
        
        
def find_prob(grid,prob_node,dim,i,j):
    
    
    #for i in range(dim):
    #for j in range(dim):
    temp1 = sense(i, j, grid)
    temp2 = temp1/N[i][j]
    #sense_value_for_node= sense(i, j, grid)
    if(N[i][j]==3 and i,j == 0,0):
        
        prob_node[i+1][j],prob_node[i][j+1],prob_node[i+1][j+1]=temp2,temp2,temp2
        
    elif(N[i][j]==3 and i==0 and j== dim-1):
        
        prob_node[i][j-1],prob_node[i+1][j-1],prob_node[i+1][j]=temp2,temp2,temp2
        
        
    elif(N[i][j]==3 and i==dim-1 and j==0):
         
        prob_node[i-1][j],prob_node[i-1][j+1],prob_node[i][j+1]=temp2,temp2,temp2
         
         
        
        
    elif(N[i][j]==5 and i==0 and j!=0):
        
        prob_node[i][j-1],prob_node[i][j+1],prob_node[i+1][j-1],prob_node[i+1][j],prob_node[i+1][j+1]=temp2,temp2,temp2,temp2,temp2
        
    elif(N[i][j]==5 and i!=0 and j==0):
        
        prob_node[i-1][j],prob_node[i+1][j],prob_node[i-1][j+1],prob_node[i][j+1],prob_node[i+1][j+1]=temp2,temp2,temp2,temp2,temp2
    
   
    elif(N[i][j]==5 and i==dim-1 and j!=0):
        
        prob_node[i][j-1],prob_node[i-1][j-1],prob_node[i-1][j],prob_node[i-1][j+1],prob_node[i][j+1]=temp2,temp2,temp2,temp2,temp2
        
    elif(N[i][j]==5 and i!=0 and j==dim-1):
        
        prob_node[i-1][j],prob_node[i-1][j-1],prob_node[i][j-1],prob_node[i+1][j-1],prob_node[i+1][j]=temp2,temp2,temp2,temp2,temp2
        
    elif(N[i][j]==8 ):
        
        prob_node[i-1][j-1],prob_node[i-1][j],prob_node[i-1][j+1],prob_node[i][j-1],prob_node[i][j+1],prob_node[i+1][j-1],prob_node[i+1][j],prob_node[i+1][j+1]=temp2,temp2,temp2,temp2,temp2,temp2,temp2,temp2

            
    return(prob_node) 


    

def update_prob(prob_node,x,y,i,j,dim,grid):
    #temp = find_prob(grid, prob_node, dim, i, j)
    #temp3= prob_node[x][y]
    find_prob(grid, prob_node, dim, i, j)
    
    act_prob_node[x][y]=(act_prob_node[x][y]+prob_node[x][y])-(act_prob_node[x][y]*prob_node[x][y])
        
    return act_prob_node

    


dim = 5
p = 0.2
grid = gen_grid(dim, p)

dis = [[0 for i in range(dim)] for j in range(dim)] #used to represent the gridworld that has been discovered (list of lists)
    

    
visited = [[0 for i in range(dim)] for j in range(dim)] #Data Structure to store whether or not cell has been visited
visited[0][0] = 1
    
con = [[-1 for i in range(dim)] for j in range(dim)] #Data Structure to store whether or not cell has been confirmed empty(0), blocked(1) or unconfirmed(-1)
con[0][0] = 0
con[dim-1][dim-1] = 0



print(find_prob(grid, prob_node, dim, 1, 1))   
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
