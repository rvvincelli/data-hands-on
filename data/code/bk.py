#creates a list (hood_name, unique_id)
def create_lookup(bike_graphs_input_three):
    hoods = list(bike_graphs_input_three.flatMap(lambda x: [x[0], x[1]]).distinct().toLocalIterator())
    return dict(zip(hoods, range(0, len(hoods))))

#creates the adjacency graph for the algorithm
def create_matrix(bike_graphs_input_three, index_lookup):
    #This is not Spark really, if you want to understand why, ask me!
    bgit = list(bike_graphs_input_three.toLocalIterator())
    M = [[0]*len(index_lookup) for i in repeat(None, len(index_lookup))]
    for x in bgit:
        a = x[0]
        b = x[1]
        M[index_lookup[a]][index_lookup[b]] = 1
    return M




#function determines the neighbors of a given vertex
def N(graph, vertex):
    c = 0
    l = []
    for i in graph[vertex]:
        if i is 1 :
         l.append(c)
        c+=1   
    return l 

#the Bron-Kerbosch recursive algorithm
def bronk(graph, r,p,x):
    if len(p) == 0 and len(x) == 0:
        print(r)
        return
    for vertex in p[:]:
        r_new = r[::]
        r_new.append(vertex)
        p_new = [val for val in p if val in N(graph, vertex)] # p intersects N(vertex)
        x_new = [val for val in x if val in N(graph, vertex)] # x intersects N(vertex)
        bronk(graph,r_new,p_new,x_new)
        p.remove(vertex)
        x.append(vertex)


# test with:
#graph = [[0,1,0,0,1,0],[1,0,1,0,1,0],[0,1,0,1,0,0],[0,0,1,0,1,1],[1,1,0,1,0,0],[0,0,0,1,0,0]]
#bronk(graph, [], [0,1,2,3,4,5], [])
