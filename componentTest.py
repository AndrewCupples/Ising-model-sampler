import sys
import numpy as np


def graph_construction_2d(rows):
    num_vertices = rows * rows
    vertex_list_create = np.arange(num_vertices)
    graph = np.arange(num_vertices).reshape((rows, rows))
    edge_list_create = []
    top_graph_create = {}
    bottom_graph_create = {}

    for i in vertex_list_create:
        top_graph_create[i] = []

    for i in range(rows):
        for j in range(rows):
            temp = []
            if (i - 1) >= 0:
                temp.append(graph[i - 1][j])
            if (j - 1) >= 0:
                temp.append(graph[i][j - 1])
            if (j + 1) < rows:
                edge_list_create.append((graph[i][j], graph[i][j + 1]))
                temp.append(graph[i][j + 1])
            if (i + 1) < rows:
                edge_list_create.append((graph[i][j], graph[i + 1][j]))
                temp.append(graph[i + 1][j])
            bottom_graph_create[graph[i][j]] = temp

    return vertex_list_create, edge_list_create, top_graph_create, bottom_graph_create, num_vertices


def add_edge(graph, edge):
    (vertex1, vertex2) = edge
    list1 = graph[vertex1]
    list2 = graph[vertex2]
    if vertex2 not in list1:
        list1.append(vertex2)
        list1.sort()
    if vertex1 not in list2:
        list2.append(vertex1)
        list2.sort()
    graph[vertex1] = list1
    graph[vertex2] = list2
    return graph


def remove_edge(graph, edge):
    (vertex1, vertex2) = edge
    list1 = graph[vertex1]
    list2 = graph[vertex2]
    if vertex2 in list1:
        list1.remove(vertex2)
    if vertex1 in list2:
        list2.remove(vertex1)
    graph[vertex1] = list1
    graph[vertex2] = list2
    return graph


def connected_components(graph):
    visited_vertices = [False for i in range(len(vertex_list))]
    connected = []
    for v in range(len(vertex_list)):
        if not visited_vertices[v]:
            temp = []
            visited_vertices, temp = depth_first_search(graph, v, visited_vertices, temp)
            connected.append(temp)
    return connected


# a depth first search function
def depth_first_search(graph, vertex, visited, temp):
    visited[vertex] = True
    stack = [vertex]
    temp.append(vertex)
    # for j in graph[vertex]:
    while len(stack):
        j = stack.pop(-1)
        if not visited[j]:
            visited[j] = True
            temp.append(j)
        for vert in graph[j]:
            if not visited[vert]:
                stack.append(vert)
        # if not visited[j]:
        #     visited, temp = depth_first_search(graph, j, visited, temp)
    return visited, temp


def components_updates(components, edge, update, graph):
    (vertex1, vertex2) = edge
    new_components = []
    if update == "add":
        comp_1 = 0
        comp_2 = 0
        for i in range(len(components)):
            if vertex1 in components[i]:
                comp_1 = i
            if vertex2 in components[i]:
                comp_2 = i
        if comp_1 != comp_2:
            for j in range(len(components)):
                if j != comp_1 and j != comp_2:
                    new_components.append(components[j])
            new_components.append(components[comp_1] + components[comp_2])
    else:
        comp_1 = 0
        comp_2 = 0
        for i in range(len(components)):
            if vertex1 in components[i]:
                comp_1 = i
            if vertex2 in components[i]:
                comp_2 = i
        if comp_1 == comp_2:
            visited_vertices = [False for i in range(len(vertex_list))]
            temp = []
            visited_vertices, temp = depth_first_search(graph, vertex1, visited_vertices, temp)
            if vertex2 in temp:
                new_components = components
            else:
                for j in range(len(components)):
                    if j != comp_1:
                        new_components.append(components[j])
                new_components.append(temp)
                temp = []
                visited_vertices, temp = depth_first_search(graph, vertex2, visited_vertices, temp)
                new_components.append(temp)
    return new_components


row_number = int(sys.argv[1])

vertex_list, edge_list, top_state, bottom_state, vertices_number = \
    graph_construction_2d(row_number)

top_copy = top_state.copy()
bottom_copy = bottom_state.copy()

components_top = connected_components(top_copy)
# components_bottom = connected_components(bottom_copy)

top_copy = add_edge(top_copy, (3, 4))
bottom_copy = remove_edge(bottom_copy, (3, 4))
bottom_copy = remove_edge(bottom_copy, (0, 1))
components_bottom = connected_components(bottom_copy)
bottom_copy = remove_edge(bottom_copy, (6, 7))

print(len(components_top))
components_top = components_updates(components_top, (3, 4), "add", top_copy)
print(len(components_top))
print(components_top)

print(len(components_bottom))
components_bottom = components_updates(components_bottom, (3, 4), "delete", bottom_copy)
print(len(components_bottom))
print(components_bottom)
