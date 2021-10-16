from A_Star import a_star
import timeit

def sense(i, j, grid, dim):
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

def add_rule(I, J, s, con, rules, rec, dim):
    lhs = []
    rhs = s
    ind = len(rules)
    for i in [I-1, I, I+1]:
        for j in [J-1, J , J+1]:
            if (i,j) == (I,J) or i<0 or j<0 or i>=dim or j>=dim:
                continue
            if con[i][j] == -1:
                lhs.append((i,j))
                rec[i][j].append(ind)
            else:
                rhs = rhs - con[i][j]
    rules.append([lhs,rhs])

def update_rules(I, J, con, rec, rules):
    for ind in rec:
        rules[ind][0].remove((I, J))
        rules[ind][1] = rules[ind][1] - con

def inference(rules, con, dis, rec):
    total = 0
    for rule in rules:
        if rule[1] == -1:
            continue
        if rule[1] == 0:
            for (i,j) in rule[0]:
                con[i][j]=0
                dis[i][j]=0
                update_rules(i, j, con[i][j], rec[i][j], rules)
                rec[i][j]=[]
                total = total + 1
            rule[1]=-1
        if rule[1] == len(rule[0]):
            for (i,j) in rule[0]:
                con[i][j]=1
                dis[i][j]=1
                update_rules(i, j, con[i][j], rec[i][j], rules)
                rec[i][j]=[]
                total = total + 1
            rule[1]=-1
    return(total)

def check_path(path, dis):
    for (i, j) in path:
        if dis[i][j] == 1:
            return False
    return True

def con_vis(con, vis, dim):
    c = 0
    for i in range(dim):
        for j in range(dim):
            if con[i][j] != -1:
                c = c + 1
    return c-vis

def agent_4(grid, dim, P, heu):
    
    start = timeit.default_timer() #recording time stamp to measure run time
    
    dis = [[0 for i in range(dim)] for j in range(dim)] #used to represent the gridworld that has been discovered (list of lists)
    
    con = [[-1 for i in range(dim)] for j in range(dim)] #Data Structure to store whether or not cell has been confirmed empty(0), blocked(1) or unconfirmed(-1)
    con[0][0] = 0
    con[dim-1][dim-1] = 0

    s = [[0 for i in range(dim)] for j in range(dim)]
    s[0][0] = sense(0,0,grid,dim)
    
    rules = []
    
    rec = [[[] for i in range(dim)] for j in range(dim)]
    
    result = False
    done = False
    
    si = 0 #Co-ordinates of the start node
    sj = 0
    
    final = [] #Data structure to store final trajectory
    
    vis = 0
    plan_t = 0
    bumps = 0

    add_rule(0, 0, s[0][0], con, rules, rec, dim)
    c_in = inference(rules, con, dis, rec)
    
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

            con[i][j] = grid[i][j]
            dis[i][j] = con[i][j]
            update_rules(i, j, con[i][j], rec[i][j], rules)
            rec[i][j]=[]
            if grid[i][j] == 1: #only updating the grid knowledge after agent bumps into a blocked node
                bumps = bumps + 1
                (si, sj) = parent[i][j]
                final.pop(len(final)-1)
                flag = False
                break
            else:
                s[i][j] = sense(i,j,grid,dim)
                add_rule(i, j, s[i][j], con, rules, rec, dim)
            c_in = inference(rules, con, dis, rec)
            if c_in != 0:
                if not check_path(path, dis):
                    flag=False
                    (si, sj) = (i,j)
                    break
            final.append((i, j))

        if flag:
            done = True
    
    stop = timeit.default_timer()
    
    return(result, final, dis, vis, start, stop, plan_t, bumps, con_vis(con, vis, dim)) #recording time stamp to measure run time
