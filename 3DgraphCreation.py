import numpy as np
import sys


rows = int(sys.argv[1])

num_vertices = rows * rows * rows

vertex_list = np.arange(num_vertices)

graph = np.arange(num_vertices).reshape((rows, rows, rows))

edge_list = []

top_graph = {}
bottom_graph = {}

for i in vertex_list:
    top_graph[i] = []

for i in range(rows):
    for j in range(rows):
        for k in range(rows):
            temp = []
            if (k - 1) >= 0:
                temp.append(graph[i][j][k-1])
            if (i - 1) >= 0:
                temp.append(graph[i-1][j][k])
            if (j - 1) >= 0:
                temp.append(graph[i][j-1][k])
            if (k + 1) < rows:
                edge_list.append((graph[i][j][k], graph[i][j][k+1]))
                temp.append(graph[i][j][k+1])
            if (j + 1) < rows:
                edge_list.append((graph[i][j][k], graph[i][j+1][k]))
                temp.append(graph[i][j+1][k])
            if (i + 1) < rows:
                edge_list.append((graph[i][j][k], graph[i+1][j][k]))
                temp.append(graph[i+1][j][k])
            bottom_graph[graph[i][j][k]] = temp


print(graph)
print(vertex_list)
print(edge_list)
print(top_graph)
print(bottom_graph)
