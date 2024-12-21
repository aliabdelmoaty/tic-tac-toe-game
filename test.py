# Algorithm: Depth First Search


# graph ={

#     '1' : ['2','3'],

#     '2' : ['4','5'],

#     '3' : ['6','7'],

#     '4' : ['8','9'],

# }

# visited = []

# def dfs(visited, graph, node):

#     if node not in visited:
#         print (node)

#         visited.append(node)

#         for neighbour in graph[node]:

#             dfs(visited, graph, neighbour)

# print('Following is Depth First Search:')

# dfs(visited, graph, '1')

# Algorithm: Greedy Search (Best First Search)
# graph = {

#     '1' : ['2','3'],

#     '2' : ['4','5'],

#     '3' : ['6','7'],

#     '4' : ['8','9'],

# }

# costs ={

#     '1' : 0,

#     '2' : 1,

#     '3' : 2,

#     '4' : 3

# }

# def execute_greedy_search(graph, h, start):
#     min =math.inf
#     new_node = -1
#     for node in graph[start]:
#         if h[node] < min:
#             min = h[node]
#             new_node = node
#     if new_node == -1:
#         return start
#     else:
#         print(new_node)
#         return execute_greedy_search(graph, h, new_node)

# print('Following is Greedy Search:')
# execute_greedy_search(graph, costs, '1')