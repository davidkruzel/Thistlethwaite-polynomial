# determine if a graph is connected
def is_connected(graph_edges, num_vertices):
  if graph_edges == []:
    return False
  connected_vertices = set()
  connected_vertices = connected_vertices.union(graph_edges[0][2])
  test = 0
  while test < 1:
    for v in connected_vertices:
      for edge in graph_edges:
        if (v in edge[2]) and (edge[2].issubset(connected_vertices) == False):
          connected_vertices = connected_vertices.union(edge[2])
          test += 1
    if test == 0:
      if (len(connected_vertices) < num_vertices):
        return False
      else:
        return True
    else:
      test = 0

# determine if a subgraph is a spanning subtree of a given graph
def is_spanning_tree(num_vertices_of_graph, subgraph_edges):
  if not is_connected(subgraph_edges, num_vertices_of_graph):
    return False
  vertices_in_subgraph = set()
  for edge in subgraph_edges:
    vertices_in_subgraph = vertices_in_subgraph.union(edge[2])
  if ( len(vertices_in_subgraph) == num_vertices_of_graph ) and ( len(subgraph_edges) == (num_vertices_of_graph - 1)):
    return(True)
  else:
    return(False)

# Calculate the tau polynomial of signed graph: graph_edges.
def tau(graph_edges, num_vertices_of_graph, num_edges_of_graph):
  
  # Define a list which will be the end result. 
  total_sum = []

  # Parse all subgraphs of graph_edges.
  for index in range(2 ** num_edges_of_graph ):
    index_binary = str(bin(index))[2:]
    while len(index_binary) < num_edges_of_graph:
      index_binary = '0' + index_binary
    subgraph_edges = []
    for i in range(num_edges_of_graph ):
      if index_binary[i] == '1':
        subgraph_edges.append(graph_edges[i])
    if is_spanning_tree(num_vertices_of_graph, subgraph_edges):
      sign = 1
      power = 0

      # Parse the edges in the graph, determine value of each
      for initial_edge in graph_edges:
        
        # Define the list cut_cyc.
        # If initial_edge in subgraph_edges, then cut_cyc is the list of labels of the edges in cut(initial_edge).
        # If initial_edge not in subgraph_edges, then cut_cyc is the list of labels of the edges in cyc(initial_edge).
        cut_cyc = [initial_edge[0]]
        for different_edge in graph_edges:
          new_subgraph = []
          if initial_edge in subgraph_edges: 
            new_subgraph = [different_edge]
          else:
            new_subgraph = [initial_edge]
          for edge in subgraph_edges:
            if (edge != initial_edge) and (edge != different_edge):
              new_subgraph.append(edge)
          if is_spanning_tree(num_vertices_of_graph, new_subgraph):
            cut_cyc.append(different_edge[0])

        # Determine whether of not initial_edge is active or not. 
        # Define the power and sign of the corresponding 'A' term accordingly. 
        if initial_edge in subgraph_edges:
          power_multiple = 1
        else:
          power_multiple = -1
        if initial_edge[0] == min(cut_cyc):
          sign *= -1
          power += (power_multiple * (-3) * initial_edge[1])
        else:
          power += (power_multiple * initial_edge[1])

      # Correct the total sum. 
      test = 0
      for i in range(len(total_sum)):
        if total_sum[i][1] == power:
          test += 1
          total_sum[i][0] += sign
      if test == 0:
        total_sum.append([sign, power])

  # Correct the total sum if it is empty
  if total_sum == []:
    sum_of_signs = 0
    for edge in graph_edges:
      sum_of_signs += edge[1]
    sign = int((-1) ** sum_of_signs)
    power = 3 * sum_of_signs
    total_sum = [[sign, power]]

  # Turn total_sum into a nice-looking output. 
  powers = []
  for i in range(len(total_sum)):
    powers.append(total_sum[i][1])
  powers.sort()
  solution = ''
  for i in range(len(powers)):
    power = powers[i]
    for term in total_sum:
      if term[1] == power:
        sign = term[0]
    sign = str(sign)
    num = sign
    if sign[0] == '-':
      num = sign[1:]
    power = str(power)
    if num == '1' and power != '0':
      num = ''
    if num == '0':
      pass
    elif sign[0] == '-':
      solution = solution + ' - '
    elif i != 0:
      solution = solution + ' + '
    if num == '0':
      pass
    elif power != '0':
      solution = solution + num + 'A^(' + power + ')'
    else:
      solution = solution + num
  return(solution)

# Turn user-entered graph into a list of edges
def edges_from_graph(graph):
  result = []
  count = 1
  current_sign = None
  vertex_list = []
  index_of_prev_comma = -1
  index_of_prev_sign = None
  for i in range(len(graph)):
    if graph[i] == ',':
      index_of_prev_comma = i
      result.append([count, current_sign, { int(vertex_list[-2]), int(vertex_list[-1]) }])
      count += 1
    elif graph[i] == '+':
      index_of_prev_sign = i
      current_sign = 1
    elif graph[i] == '-':
      index_of_prev_sign = i
      current_sign = -1
    elif (index_of_prev_comma == i - 1) or (index_of_prev_sign == i -1):
      vertex_list.append(graph[i])
    else:
      vertex_list[-1] = vertex_list[-1] + graph[i]
    if i == len(graph) - 1:
      result.append([count, current_sign, { int(vertex_list[-2]), int(vertex_list[-1]) }])
  return result
  
# Determine if a given string is a valid graph. 
def is_valid(input):

  # Counter makes sure that +/- and ',' are alternating in input
  counter = 0
  for i in range(len(input)):
    if not input[i].isnumeric():
      if (input[i] == '+') or (input[i] == '-'):
        if counter != 0:
          return False
        else:
          counter += 1
      elif input[i]  == ',':
        if counter != 1:
          return False
        else:
          counter -= 1
      else:
        return False
  return True
  
# Ask the user to enter a graph
def prompt_user():
  print('Please enter a valid graph or type "quit"')
  prompt = input(': ')
  if prompt == 'quit':
    return False
  if not is_valid(prompt):
    print('This is not a valid input')
    return True
  else:
    input_graph = edges_from_graph(prompt)
    vertices = set()
    for i in input_graph:
      vertices = vertices.union(i[2])
    num_vertices = len(vertices)
    num_edges = len(input_graph)
    if not is_connected(input_graph, num_vertices):
      print('This graph is not connected')
      return True
    print(tau(input_graph, num_vertices, num_edges))
    return True
    
# Start the program
def main():
  while prompt_user():
    pass

main()

  

    
