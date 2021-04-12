import numpy as np
import sys
# import math


# need function to describe convergence
def convergence(graph_top, graph_bottom):
    conv = True
    for key in graph_top.keys():
        list_top = graph_top[key]
        list_bottom = graph_bottom[key]
        list_top.sort()
        list_bottom.sort()
        if list_top != list_bottom:
            conv = False
    return conv


# a function to update the graphs given a list edge and the random variables for each time
def update_edge(edges, random_variables, graph_top, graph_bottom):
    top_copy = graph_top.copy()
    bottom_copy = graph_bottom.copy()
    update_probability = rcm_p
    components_top = connected_components(top_copy)
    components_bottom = connected_components(bottom_copy)
    for y in range(len(uniform_random_variables)):
        rv = random_variables[-y-1]
        edge_choice = edges[-y-1]
        choice_top = glauber_func(rv, edge_choice, top_copy, update_probability, components_top)
        choice_bottom = glauber_func(rv, edge_choice, bottom_copy, update_probability, components_bottom)
        if choice_top:
            top_copy = add_edge(top_copy, edge_choice)
            components_top = components_updates(components_top, edge_choice, "remove", top_copy)
        if choice_bottom:
            bottom_copy = add_edge(bottom_copy, edge_choice)
            components_bottom = components_updates(components_bottom, edge_choice, "remove", bottom_copy)
        if not choice_top:
            top_copy = remove_edge(top_copy, edge_choice)
            components_top = components_updates(components_top, edge_choice, "remove", top_copy)
        if not choice_bottom:
            bottom_copy = remove_edge(bottom_copy, edge_choice)
            components_bottom = components_updates(components_bottom, edge_choice, "remove", bottom_copy)

    return top_copy, bottom_copy


# a function to determine whether an edge should be in a graph or not
def glauber_func(random_variable, edge, graph, prob, connected_comp):
    # part1 = rcm_p / (1 - rcm_p)
    # connected_base = len(connected_components(graph))
    # if edge_in(graph, edge):
    #     update_graph = remove_edge(graph, edge)
    #     connected_joined = len(connected_components(update_graph))
    #     part2 = math.pow(2, connected_base - connected_joined)
    # else:
    #     update_graph = add_edge(graph, edge)
    #     connected_joined = len(connected_components(update_graph))
    #     part2 = math.pow(2, connected_joined - connected_base)
    # out = part1 * part2
    # if out >= random_variable:
    #     return True
    # else:
    #     return False

    # connected_base = len(connected_components(graph))
    connected_base = connected_comp
    if edge_in(graph, edge):
        update_graph = remove_edge(graph, edge)
        # connected_joined = len(connected_components(update_graph))
        new_connected = components_updates(connected_base, edge, "remove", update_graph)
        connected_joined = len(new_connected)
    else:
        update_graph = add_edge(graph, edge)
        # connected_joined = len(connected_components(update_graph))
        new_connected = components_updates(connected_base, edge, "add", update_graph)
        connected_joined = len(new_connected)
    if connected_base == connected_joined:
        if random_variable < prob:
            return True
        else:
            return False
    else:
        out = prob / (prob + 2 * (1-prob))
        if out >= random_variable:
            return True
        else:
            return False


# a function to get the number of connected components in a graph
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


# a function to add an edge to a graph
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


# a function that removes an edge from a graph
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


# a function that checks whether an edge is in a graph or not
def edge_in(graph, edge):
    (vertex1, vertex2) = edge
    list1 = graph[vertex1]
    list2 = graph[vertex2]
    if (vertex2 in list1) and (vertex1 in list2):
        return True
    else:
        return False


# a unction for creating the vertex, edge lists and top and bottom states for Z2 square graphs
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


def graph_construction_3d(rows):
    num_vertices = rows * rows * rows
    vertex_list_create = np.arange(num_vertices)
    graph = np.arange(num_vertices).reshape((rows, rows, rows))
    edge_list_create = []
    top_graph_create = {}
    bottom_graph_create = {}

    for i in vertex_list_create:
        top_graph_create[i] = []

    for i in range(rows):
        for j in range(rows):
            for k in range(rows):
                temp = []
                if (k - 1) >= 0:
                    temp.append(graph[i][j][k - 1])
                if (i - 1) >= 0:
                    temp.append(graph[i - 1][j][k])
                if (j - 1) >= 0:
                    temp.append(graph[i][j - 1][k])
                if (k + 1) < rows:
                    edge_list_create.append((graph[i][j][k], graph[i][j][k + 1]))
                    temp.append(graph[i][j][k + 1])
                if (j + 1) < rows:
                    edge_list_create.append((graph[i][j][k], graph[i][j + 1][k]))
                    temp.append(graph[i][j + 1][k])
                if (i + 1) < rows:
                    edge_list_create.append((graph[i][j][k], graph[i + 1][j][k]))
                    temp.append(graph[i + 1][j][k])
                bottom_graph_create[graph[i][j][k]] = temp

    return vertex_list_create, edge_list_create, top_graph_create, bottom_graph_create, num_vertices


def components_updates(components_use, edge, update, graph):
    (vertex1, vertex2) = edge
    new_components = []
    if update == "add":
        comp_1 = 0
        comp_2 = 0
        for i in range(len(components_use)):
            if vertex1 in components_use[i]:
                comp_1 = i
            if vertex2 in components_use[i]:
                comp_2 = i
        if comp_1 != comp_2:
            for j in range(len(components_use)):
                if j != comp_1 and j != comp_2:
                    new_components.append(components_use[j])
            new_components.append(components_use[comp_1] + components_use[comp_2])
    else:
        comp_1 = 0
        comp_2 = 0
        for i in range(len(components_use)):
            if vertex1 in components_use[i]:
                comp_1 = i
            if vertex2 in components_use[i]:
                comp_2 = i
        if comp_1 == comp_2:
            visited_vertices = [False for i in range(len(vertex_list))]
            temp = []
            visited_vertices, temp = depth_first_search(graph, vertex1, visited_vertices, temp)
            if vertex2 in temp:
                new_components = components_use
            else:
                for j in range(len(components_use)):
                    if j != comp_1:
                        new_components.append(components_use[j])
                new_components.append(temp)
                temp = []
                visited_vertices, temp = depth_first_search(graph, vertex2, visited_vertices, temp)
                new_components.append(temp)
    return new_components


row_number = int(sys.argv[1])

edge_rng = np.random.default_rng()     # Sets up the random generator for taking edges
cutoff_rng = np.random.default_rng()   # Sets up the random generator for sampling cutoffs
ising_rng = np.random.default_rng()    # Sets up the random generator for giving spins to vertices

rcm_p = 0.5

uniform_random_variables = []          # a list of the previous uniform random variables
edges_used = []                        # a list of all the edges drawn in order

converge = False                       # sets the converge variable to be false as it is at the start

# setup two starting states
# each vertex is numbered starting from 0 going along the row, then onto the next

vertex_list, edge_list, top_state, bottom_state, vertices_number = \
    graph_construction_3d(row_number)

# run sampling algorithm until convergence

time = 1

top_graph = {}
bottom_graph = {}

while not converge:
    print(time)

    bool_choices_top = []  # used for if an edge should be in a graph or not
    bool_choices_bottom = []
    extra = time - len(edges_used)

    for x in range(extra):
        random_edge_number = int(edge_rng.random() * len(edge_list))
        random_edge = edge_list[random_edge_number]
        edges_used.append(random_edge)

        uniform_rv = cutoff_rng.uniform()
        uniform_random_variables.append(uniform_rv)

    top_graph, bottom_graph = update_edge(edges_used, uniform_random_variables, top_state, bottom_state)

    converge = convergence(top_graph, bottom_graph)
    if not converge:
        time *= 2


# convert sample to Ising and output
components = connected_components(top_graph)
spins = ising_rng.integers(0, 1, len(components), endpoint=True)
output = np.zeros((row_number, row_number, row_number), int)
for x in range(len(components)):
    cc = components[x]
    for t in range(len(cc)):
        output[cc[t] // row_number // row_number][(cc[t] // row_number) % row_number][cc[t] % row_number] = spins[x]
print(output)
print(top_graph)
