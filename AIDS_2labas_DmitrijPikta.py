points = ['s', 'u', 'v', 't']
graph = [[0, 1000, 1000, 0],
         [0, 0, 1, 1000],
         [0, 0, 0, 1000],
         [0, 0, 0, 0]]

graph1 = [[0, 16, 13, 0, 0, 0],
          [0, 0, 10, 12, 0, 0],
          [0, 4, 0, 0, 14, 0],
          [0, 0, 9, 0, 0, 20],
          [0, 0, 0, 7, 0, 4],
          [0, 0, 0, 0, 0, 0]]


def Enter_graph_by_edges() -> list:
    # Entering adges of graph
    data = []
    print("Please enter each graph's edge and it's size. Example: s a 10. To stop entering enter //")
    while True:
        x = input()
        if x == "//":
            break
        try:
            x, y, size = x.split()
            size = int(size)
            edge = [x, y, size]
            data.append(edge)
        except:
            print("Error, try again")

    # Making list of all vertex
    vertex = []
    for i in range(0, len(data)):
        for j in range(0, 2):
            if data[i][j] not in vertex:
                vertex.append(data[i][j])
    
    # Entering source and target vertex
    s, t = None, None
    print("Please enter source and target vertex. Example: s t")
    while True:
        try:
            s, t = input().split()
            break
        except:
            print("Error, try again")

    # Moving source vertex to ahead and target vertex to end
    if s not in vertex:
        vertex.insert(0, s)
    else:
        index = vertex.index(s)
        vertex.pop(index)
        vertex.insert(0, s)
    
    if t not in vertex:
        vertex.append(t)
    else:
        index = vertex.index(t)
        vertex.pop(index)
        vertex.append(t)

    # Making graph matrix
    graph = [[0] * len(vertex) for _ in range(len(vertex))]
    for i in range(0, len(vertex)):
        for j in range(0, len(data)):
            if data[j][0] == vertex[i]:
                graph[i][vertex.index(data[j][1])] += data[j][2]
        
    return graph, vertex


def Get_path(graph) -> list:
    visited = [False] * len(graph)

    queue = []
    parent = {}

    queue.append(0)
    visited[0] = True
    parent[0] = None

    while queue:
        n = queue.pop(0)

        if n == len(graph)-1:
            path = []
            while n is not None:
                path.append(n)
                n = parent[n]
            return path[::-1]
        
        counter = 0
        for i in graph[n]:
            if i != 0 and not visited[counter]:
                queue.append(counter)
                visited[counter] = True
                parent[counter] = n
            counter+=1

    return None


def EdmondsKarp_algorithm(graph) -> int:
    for i in range(0, len(graph)):
        pass
    
    max_flow = 0
    while True:
        path = Get_path(graph)
        # If where are no more grow path in graph, algorothm will finish
        if path is None:
            return max_flow

        # Getting max possible flow for all branch in path    
        flow_in_path = []
        for i in range(0, len(path)-1):
            flow_in_path.append(graph[path[i]][path[i+1]])
        
        # Getting real flow in path 
        flow = min(flow_in_path)

        # Culculating whole flow in graph
        max_flow+= flow 

        # Removing culculated flow from graph
        for i in range(0, len(path)-1):
            graph[path[i]][path[i+1]] -= flow
            graph[path[i+1]][path[i]] += flow



graph2, vertex = Enter_graph_by_edges()
    
print(EdmondsKarp_algorithm(graph2))
            
    
