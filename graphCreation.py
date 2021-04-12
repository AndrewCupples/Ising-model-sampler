import numpy as np
import sys


rows = int(sys.argv[1])

num_vertices = rows * rows

vertex_list = np.arange(num_vertices)

graph = np.arange(num_vertices).reshape((rows, rows))

edge_list = []

top_graph = {}
bottom_graph = {}

for i in vertex_list:
    top_graph[i] = []

for i in range(rows):
    for j in range(rows):
        temp = []
        if (i - 1) >= 0:
            temp.append(graph[i-1][j])
        if (j - 1) >= 0:
            temp.append(graph[i][j-1])
        if (j + 1) < rows:
            edge_list.append((graph[i][j], graph[i][j+1]))
            temp.append(graph[i][j+1])
        if (i + 1) < rows:
            edge_list.append((graph[i][j], graph[i+1][j]))
            temp.append(graph[i+1][j])
        bottom_graph[graph[i][j]] = temp


print(vertex_list)
print(edge_list)
print(top_graph)
print(bottom_graph)
