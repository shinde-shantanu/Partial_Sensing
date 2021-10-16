from Grid_Generator import gen_grid
from A_Star import a_star
from Agent_1 import agent_1
from Agent_2 import agent_2
from Agent_3 import agent_3
from Agent_4 import agent_4
import pandas as pd

#Trajectory length 1,2,3,4
#Number of nodes visited 1,2,3,4
#Final path length through discovered gridworld 1,2,3,4
#Total planning time 1,2,3,4
#Number of bumps encountered 1,2,3,4
#Run time 1,2,3,4
#Number of confirmed nodes - Number of visited nodes 3,4
#Path length in full gridworld
#Density

df = pd.DataFrame(columns=['p',
                           'Trajectory Length 1',
                           'Trajectory Length 2',
                           'Trajectory Length 3',
                           'Trajectory Length 4',
                           'Nodes Visited 1',
                           'Nodes Visited 2',
                           'Nodes Visited 3',
                           'Nodes Visited 4',
                           'FDG Length 1',
                           'FDG Length 2',
                           'FDG Length 3',
                           'FDG Length 4',
                           'Planning Time 1',
                           'Planning Time 2',
                           'Planning Time 3',
                           'Planning Time 4',
                           'Bumps 1',
                           'Bumps 2',
                           'Bumps 3',
                           'Bumps 4',
                           'Run Time 1',
                           'Run Time 2',
                           'Run Time 3',
                           'Run Time 4',
                           'con_vis 3',
                           'con_vis 4',
                           'FG Length'])

def find_path(parent, dim, si, sj): #used to find the path from the parent data structure
    i,j = dim-1, dim-1
    path = [(dim-1, dim-1)]
    while (i, j) != (si, sj):
        path.insert(0, parent[i][j])
        (i, j) = parent[i][j]
    return(path)

p = 0
x = 0

while p<=0.33:

    grid = gen_grid(101, p)

    result, traj, dis, vis1, start, stop, plan_t1, bumps1 = agent_1(grid, 101, p, 2)

    if result == True:
        x = x + 1
        
        traj1 = len(traj)
        result, par = a_star(101, p, dis, 2, 0, 0)
        FDG1 = len(find_path(par,101,0,0))
        rt1 = stop - start

        result, traj, dis, vis2, start, stop, plan_t2, bumps2 = agent_2(grid, 101, p, 2)
        traj2 = len(traj)
        result, par = a_star(101, p, dis, 2, 0, 0)
        FDG2 = len(find_path(par,101,0,0))
        rt2 = stop - start

        result, traj, dis, vis3, start, stop, plan_t3, bumps3, con_vis3 = agent_3(grid, 101, p, 2)
        traj3 = len(traj)
        result, par = a_star(101, p, dis, 2, 0, 0)
        FDG3 = len(find_path(par,101,0,0))
        rt3 = stop - start

        result, traj, dis, vis4, start, stop, plan_t4, bumps4, con_vis4 = agent_4(grid, 101, p, 2)
        traj4 = len(traj)
        result, par = a_star(101, p, dis, 2, 0, 0)
        FDG4 = len(find_path(par,101,0,0))
        rt4 = stop - start

        result, par = a_star(101, p, grid, 2, 0, 0)
        FG = len(find_path(par,101,0,0))

        df1 = pd.DataFrame([[p,traj1,traj2,traj3,traj4,vis1,vis2,vis3,vis4,FDG1,FDG2,FDG3,FDG4,plan_t1,plan_t2,plan_t3,plan_t4,bumps1,bumps2,bumps3,bumps4,rt1,rt2,rt3,rt4,con_vis3,con_vis4,FG]],columns=['p','Trajectory Length 1','Trajectory Length 2','Trajectory Length 3','Trajectory Length 4','Nodes Visited 1','Nodes Visited 2','Nodes Visited 3','Nodes Visited 4','FDG Length 1','FDG Length 2','FDG Length 3','FDG Length 4','Planning Time 1','Planning Time 2','Planning Time 3','Planning Time 4','Bumps 1','Bumps 2','Bumps 3','Bumps 4','Run Time 1','Run Time 2','Run Time 3','Run Time 4','con_vis 3','con_vis 4','FG Length'])
        df = pd.concat([df,df1])

        if x == 30:
            x = 0
            print(p)
            p = p + 0.01
            df.to_csv('data.csv')
